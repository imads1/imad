from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime, timedelta
import json
import os
import psutil
from pathlib import Path
import subprocess
import logging
import threading
import shutil
import time
import asyncio
import aiohttp
import sys
import re
import random
import signal
from functools import wraps
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
import aiofiles
import requests

app = Flask(__name__)
app.secret_key = 'c4_panel_secret_key_2023!@#'

# reCAPTCHA Configuration
RECAPTCHA_SECRET_KEY = '6LcdoYcsAAAAAPuB-uAUj0OuSUzRWZ6922fz12WX'
RECAPTCHA_SITE_KEY = '6LcdoYcsAAAAAJ1dPye8-U8S91xuvATShY541-aQ'

def verify_recaptcha(response_token):
    """التحقق من صحة رمز reCAPTCHA عبر Google API"""
    try:
        payload = {
            'secret': RECAPTCHA_SECRET_KEY,
            'response': response_token
        }
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
        result = response.json()
        return result.get('success', False)
    except Exception as e:
        logger.error(f"Error verifying reCAPTCHA: {e}")
        return False

executor = ThreadPoolExecutor(max_workers=10, thread_name_prefix="worker")
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / 'data'
USER_SERVERS_DIR = BASE_DIR / 'user_servers'
TEMPLATES_DIR = BASE_DIR / 'templates'
FF_BOT_DIR = BASE_DIR / 'FF_BOT'
GENRATOR_DIR = BASE_DIR / 'genrator'

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(USER_SERVERS_DIR, exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)

USERS_FILE = DATA_DIR / 'users.json'
SERVERS_FILE = DATA_DIR / 'servers.json'
TRANSACTIONS_FILE = DATA_DIR / 'transactions.json'

BOT_PRICES = {'friend': 10, 'clan': 10}
USER_ROLES = {'admin': 'مدير النظام', 'owner': 'مالك', 'user': 'مستخدم عادي'}

_data_cache = {}
_cache_lock = threading.Lock()
_cache_timestamps = {}

def cached_load(filepath, ttl=5):
    with _cache_lock:
        now = time.time()
        if str(filepath) in _data_cache and now - _cache_timestamps.get(str(filepath), 0) < ttl:
            return _data_cache[str(filepath)]
    data = load_data(filepath)
    with _cache_lock:
        _data_cache[str(filepath)] = data
        _cache_timestamps[str(filepath)] = now
    return data

def invalidate_cache(filepath=None):
    with _cache_lock:
        if filepath:
            _data_cache.pop(str(filepath), None)
            _cache_timestamps.pop(str(filepath), None)
        else:
            _data_cache.clear()
            _cache_timestamps.clear()

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

def owner_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        users = cached_load(USERS_FILE)
        user = next((u for u in users if u['username'] == session.get('user')), None)
        if not user or user.get('role') != 'owner':
            return jsonify({'success': False, 'message': 'ليس لديك صلاحية المالك'}), 403
        return f(*args, **kwargs)
    return decorated_function


def init_data():
    if not USERS_FILE.exists():
        default_users = [
            {
                "username": "admin", "password": "admin123", "balance": 1000, "points": 100,
                "role": "admin", "servers": [],
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "last_login": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            {
                "username": "owner1", "password": "imad1x", "balance": 999, "points": 999,
                "role": "owner", "servers": [],
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "last_login": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]
        with open(USERS_FILE, 'w') as f:
            json.dump(default_users, f, indent=4)

    if not SERVERS_FILE.exists():
        with open(SERVERS_FILE, 'w') as f:
            json.dump([], f, indent=4)
    
    if not TRANSACTIONS_FILE.exists():
        with open(TRANSACTIONS_FILE, 'w') as f:
            json.dump([], f, indent=4)

def load_data(filepath):
    try:
        if not filepath.exists():
            return [] if 'servers' in str(filepath) or 'transactions' in str(filepath) else {}
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Error loading {filepath}: {str(e)}")
        return [] if 'servers' in str(filepath) or 'transactions' in str(filepath) else {}

def save_data(filepath, data):
    try:
        temp_file = filepath.with_suffix('.tmp')
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        temp_file.replace(filepath)
        invalidate_cache(filepath)
        return True
    except Exception as e:
        logger.error(f"Error saving to {filepath}: {str(e)}")
        return False

def get_user_role(username):
    users = cached_load(USERS_FILE)
    user = next((u for u in users if u['username'] == username), None)
    return user.get('role', 'user') if user else 'user'

def has_sufficient_points(username, bot_type):
    users = cached_load(USERS_FILE)
    user = next((u for u in users if u['username'] == username), None)
    if not user:
        return False
    required_points = BOT_PRICES.get(bot_type, 10)
    return user.get('points', 0) >= required_points

def deduct_points(username, bot_type, amount=None):
    users = load_data(USERS_FILE)
    for user in users:
        if user['username'] == username:
            required_points = amount if amount else BOT_PRICES.get(bot_type, 10)
            if user.get('points', 0) >= required_points:
                user['points'] -= required_points
                if save_data(USERS_FILE, users):
                    log_transaction(username, 'deduct', required_points, f"إنشاء بوت {bot_type}" if not amount else "خصم نقاط")
                    return True
            break
    return False

def add_points(username, amount, reason=""):
    users = load_data(USERS_FILE)
    for user in users:
        if user['username'] == username:
            user['points'] = user.get('points', 0) + amount
            if save_data(USERS_FILE, users):
                log_transaction(username, 'add', amount, reason)
                return True
    return False

def set_points(username, amount, reason=""):
    users = load_data(USERS_FILE)
    for user in users:
        if user['username'] == username:
            user['points'] = amount
            if save_data(USERS_FILE, users):
                log_transaction(username, 'set', amount, reason)
                return True
    return False

def log_transaction(username, action, amount, reason=""):
    transaction = {
        'username': username, 'action': action, 'amount': amount,
        'reason': reason, 'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    transactions = load_data(TRANSACTIONS_FILE)
    transactions.append(transaction)
    save_data(TRANSACTIONS_FILE, transactions)

def update_script_variables(script_path, replacements):
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        for old_value, new_value in replacements.items():
            content = content.replace(old_value, new_value)
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        logger.error(f"Error updating script {script_path}: {str(e)}")
        return False

async def generate_vip_account_async(bot_name, bot_type):
    account_name = f"{bot_name}"
    try:
        logger.info(f"📝 Generating account '{account_name}' from local pool")
        vnom_path = "FF_BOT/vnom.json"
        compiled_path = "FF_BOT/compiledusing.json"

        if not os.path.exists(vnom_path):
            return {'success': False, 'message': "vnom.json file not found"}

        async with aiofiles.open(vnom_path, "r", encoding="utf-8") as f:
            content = await f.read()
            accounts = json.loads(content)

        if not accounts or not isinstance(accounts, list):
            return {'success': False, 'message': "vnom.json is empty or invalid"}

        selected_account = random.choice(accounts)
        uid = str(selected_account.get("uid", ""))
        password = str(selected_account.get("password", ""))

        if not uid or not password:
            return {'success': False, 'message': "Invalid account data selected from vnom.json"}

        change_url = f"http://fi5.bot-hosting.net:22143/change?uid={uid}&password={password}&new_name={account_name}"
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60)) as session:
            async with session.get(change_url) as response:
                if response.status != 200:
                    return {'success': False, 'message': f"Change API returned status {response.status}"}
                data = await response.json()
                if data.get("status") != "success":
                    return {'success': False, 'message': "Change API did not return success status"}

        accounts.remove(selected_account)
        async with aiofiles.open(vnom_path, "w", encoding="utf-8") as f:
            await f.write(json.dumps(accounts, ensure_ascii=False, indent=4))

        used_accounts = []
        if os.path.exists(compiled_path):
            async with aiofiles.open(compiled_path, "r", encoding="utf-8") as f:
                content = await f.read()
                used_accounts = json.loads(content) if content else []
                if not isinstance(used_accounts, list):
                    used_accounts = []

        used_accounts.append(selected_account)
        async with aiofiles.open(compiled_path, "w", encoding="utf-8") as f:
            await f.write(json.dumps(used_accounts, ensure_ascii=False, indent=4))

        return {
            'success': True, 'uid': uid, 'password': password,
            'name': account_name, 'region': '', 'server': '',
            'status': 'registered', 'source': 'local_pool'
        }

    except asyncio.TimeoutError:
        return {'success': False, 'message': "Change API request timed out"}
    except aiohttp.ClientError as e:
        return {'success': False, 'message': f"Change API connection error: {str(e)}"}
    except Exception as e:
        logger.error(f"❌ Unexpected error: {str(e)}", exc_info=True)
        return {'success': False, 'message': f"Unexpected error: {str(e)}"}

def generate_vip_account(bot_name, bot_type):
    return loop.run_until_complete(generate_vip_account_async(bot_name, bot_type))

def create_server_environment(server_type, username, server_name, bot_data):
    try:
        user_dir = USER_SERVERS_DIR / username
        server_dir = user_dir / server_name
        server_dir.mkdir(parents=True, exist_ok=True)
        os.chmod(server_dir, 0o777)
        
        bot_info = {
            'type': server_type, 'name': server_name,
            'data': bot_data, 'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        info_file = server_dir / 'bot_info.json'
        with open(info_file, 'w', encoding='utf-8') as f:
            json.dump(bot_info, f, indent=4)
        
        logger.info(f"✅ Server environment created: {server_dir}")
        return server_dir
    except Exception as e:
        logger.error(f"❌ Error creating server environment: {str(e)}")
        return None

def setup_friend_bot(server_dir, bot_data, account_info):
    try:
        logger.info(f"Setting up FRIEND bot with account: {account_info['uid']}")
        
        files_to_copy = [
            FF_BOT_DIR / 'main.py', FF_BOT_DIR / 'Fo_pb2.py',
            FF_BOT_DIR / 'xTnito.py', FF_BOT_DIR / 'xKEys.py',
            FF_BOT_DIR / 'em.py', FF_BOT_DIR / 'p.py'
        ]
        
        for source_file in files_to_copy:
            if source_file.exists():
                dest_path = server_dir / source_file.name
                shutil.copy(source_file, dest_path)
                os.chmod(dest_path, 0o755)
        
        main_script = server_dir / 'main.py'
        replacements = {
            'BOT_NAME = "DEFAULT_BOT"': f'BOT_NAME = "{bot_data["bot_name"]}"',
            'DEVELOPER_NAME = "DEFAULT_DEV"': f'DEVELOPER_NAME = "{bot_data["developer_name"]}"',
            'CHANNEL_NAME = ""': f'CHANNEL_NAME = "{bot_data["channel_name"]}"',
            "FF_CLient('uid','pas')": f"FF_CLient('{account_info['uid']}','{account_info['password']}')"
        }
        update_script_variables(main_script, replacements)
        
        p_script = server_dir / 'p.py'
        replacements_p = {
            'xid = ""': f'xid = "{account_info["uid"]}"',
            'xpas = ""': f'xpas = "{account_info["password"]}"'
        }
        update_script_variables(p_script, replacements_p)
        
        em_process = None
        try:
            em_process = subprocess.Popen(
                ['python3', str(server_dir / 'em.py')],
                cwd=str(server_dir), stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            time.sleep(2)
        except Exception as e:
            logger.error(f"Error starting em.py: {e}")
        
        bot_process = None
        try:
            bot_process = subprocess.Popen(
                ['python3', str(main_script)], cwd=str(server_dir),
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True
            )
        except Exception as e:
            logger.error(f"Error starting friend bot: {e}")
            return None
        
        panel_process = None
        try:
            panel_process = subprocess.Popen(
                ['python3', str(p_script)], cwd=str(server_dir),
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True
            )
        except Exception as e:
            logger.error(f"Error starting control panel: {e}")
        
        logger.info("✅ Friend bot setup completed")
        return {
            'bot_pid': bot_process.pid,
            'panel_pid': panel_process.pid if panel_process else None,
            'em_pid': em_process.pid if em_process else None
        }
    except Exception as e:
        logger.error(f"❌ Error setting up friend bot: {str(e)}", exc_info=True)
        return None

def setup_clan_bot(server_dir, bot_data, account_info, request_data=None):
    try:
        logger.info(f"Setting up CLAN bot with account: {account_info['uid']}")
        
        only_tag = True
        if request_data and isinstance(request_data, dict):
            only_tag = request_data.get('only_tag', True)
        
        main_file = 'TcP_GuiLd.py' if only_tag else 'TcP_GuiLd-TaG.py'
        logger.info(f"Using: {main_file} (only_tag={only_tag})")
        
        files_to_copy = [
            (FF_BOT_DIR / main_file, server_dir / main_file),
            (FF_BOT_DIR / 'xTnito.py', server_dir / 'xTnito.py'),
            (FF_BOT_DIR / 'xKEys.py', server_dir / 'xKEys.py'),
            (FF_BOT_DIR / 'em.py', server_dir / 'em.py'),
            (FF_BOT_DIR / 'clan.py', server_dir / 'clan.py'),
            (FF_BOT_DIR / 'reqClan_pb2.py', server_dir / 'reqClan_pb2.py')
        ]
        
        for source_file, dest_path in files_to_copy:
            if source_file.exists():
                shutil.copy(source_file, dest_path)
                os.chmod(dest_path, 0o755)
        
        clan_script = server_dir / main_file
        replacements = {
            "owners_id=''": f"owners_id='{bot_data.get('owner_ids', '')}'",
            "bot_name=''": f"bot_name='{bot_data.get('bot_name', '')}'",
            "tag=''": f"tag='{bot_data.get('clan_tag', '')}'",
            "FF_CLient('uid','pas')": f"FF_CLient('{account_info['uid']}','{account_info['password']}')"
        }
        update_script_variables(clan_script, replacements)
        
        clan_req_script = server_dir / 'clan.py'
        replacements_clan = {
            "uid = ''": f"uid = '{account_info['uid']}'",
            "pas = ''": f"pas = '{account_info['password']}'",
            "c_id = 'clan id'": f"c_id = '{bot_data['clan_id']}'",

        }
        update_script_variables(clan_req_script, replacements_clan)
        
        em_script = server_dir / 'em.py'
        replacements_em = {
            "uid = \"\"": f"uid='{account_info['uid']}'",
            "pas = \"\"": f"pas='{account_info['password']}'"
        }
        update_script_variables(em_script, replacements_em)
        
        em_process = None
        try:
            em_process = subprocess.Popen(
                ['python3', str(em_script)], cwd=str(server_dir),
                stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            time.sleep(2)
        except Exception as e:
            logger.error(f"Error starting em.py: {e}")
        
        clan_req_process = None
        try:
            clan_req_process = subprocess.Popen(
                ['python3', str(clan_req_script)], cwd=str(server_dir),
                stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            time.sleep(2)
        except Exception as e:
            logger.error(f"Error starting clan request: {e}")
        
        bot_process = None
        try:
            bot_process = subprocess.Popen(
                ['python3', str(clan_script)], cwd=str(server_dir),
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True
            )
        except Exception as e:
            logger.error(f"Error starting clan bot: {e}")
            return None
        
        logger.info("✅ Clan bot setup completed")
        return {
            'bot_pid': bot_process.pid,
            'em_pid': em_process.pid if em_process else None,
            'clan_req_pid': clan_req_process.pid if clan_req_process else None,
            'only_tag': only_tag
        }
    except Exception as e:
        logger.error(f"❌ Error setting up clan bot: {str(e)}", exc_info=True)
        return None

async def create_server_async_task(server_type, username, server_name, bot_data, request_data):
    try:
        users = load_data(USERS_FILE)
        servers = load_data(SERVERS_FILE)
        
        user = next((u for u in users if u['username'] == username), None)
        if not user:
            return False, "المستخدم غير موجود"

        if any(s['server_name'] == server_name and s['owner'] == username for s in servers):
            return False, "لديك بالفعل سيرفر بهذا الاسم"

        required_points = BOT_PRICES.get(server_type, 10)
        current_points = user.get('points', 0)
        
        if current_points < required_points:
            return False, f"نقاطك غير كافية! لديك {current_points} وتحتاج {required_points}"

        user['points'] = current_points - required_points
        if not save_data(USERS_FILE, users):
            return False, "فشل في حفظ بيانات النقاط"
        
        log_transaction(username, 'deduct', required_points, f"إنشاء بوت {server_type}")

        server_dir = create_server_environment(server_type, username, server_name, bot_data)
        if not server_dir:
            user['points'] += required_points
            save_data(USERS_FILE, users)
            log_transaction(username, 'add', required_points, "استرجاع نقاط - فشل إنشاء المجلد")
            return False, "فشل في إنشاء مجلد السيرفر"

        account_result = await generate_vip_account_async(server_name, server_type)
        if not account_result['success']:
            user['points'] += required_points
            save_data(USERS_FILE, users)
            log_transaction(username, 'add', required_points, "استرجاع نقاط - فشل توليد الحساب")
            if server_dir.exists():
                shutil.rmtree(server_dir, ignore_errors=True)
            return False, account_result['message']

        process_info = None
        if server_type == 'friend':
            process_info = setup_friend_bot(server_dir, bot_data, account_result)
        elif server_type == 'clan':
            if request_data is None:
                request_data = {}
            process_info = setup_clan_bot(server_dir, bot_data, account_result, request_data)
        
        if not process_info:
            user['points'] += required_points
            save_data(USERS_FILE, users)
            log_transaction(username, 'add', required_points, "استرجاع نقاط - فشل إعداد البوت")
            if server_dir.exists():
                shutil.rmtree(server_dir, ignore_errors=True)
            return False, "فشل في إعداد البوت"

        created_at = datetime.now()
        expires_at = created_at + timedelta(days=30)
        only_tag_value = True
        if server_type == 'clan' and request_data and isinstance(request_data, dict):
            only_tag_value = request_data.get('only_tag', True)
        
        server_data = {
            'server_id': str(len(servers) + 1), 'type': server_type,
            'server_name': server_name, 'owner': username,
            'path': str(server_dir), 'status': 'Online',
            'created_at': created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'expires_at': expires_at.strftime("%Y-%m-%d %H:%M:%S"),
            'account_uid': account_result['uid'],
            'account_password': account_result['password'],
            'process_info': process_info, 'points_spent': required_points,
            **bot_data
        }
        
        if server_type == 'clan':
            server_data['only_tag'] = only_tag_value
        
        servers.append(server_data)
        user['servers'].append(server_name)
        
        save_data(SERVERS_FILE, servers)
        save_data(USERS_FILE, users)

        return True, "تم إنشاء البوت بنجاح"
    except Exception as e:
        logger.error(f"❌ Error in create_server_async: {str(e)}", exc_info=True)
        try:
            users = load_data(USERS_FILE)
            user = next((u for u in users if u['username'] == username), None)
            if user:
                user['points'] = user.get('points', 0) + required_points
                save_data(USERS_FILE, users)
                log_transaction(username, 'add', required_points, "استرجاع نقاط - خطأ غير متوقع")
        except:
            pass
        return False, str(e)

def create_server_async(server_type, username, server_name, bot_data, request_data):
    return loop.run_until_complete(create_server_async_task(server_type, username, server_name, bot_data, request_data))

def refresh_server_files(server, server_dir):
    try:
        account_info = {
            'uid': server.get('account_uid', ''),
            'password': server.get('account_password', '')
        }
        
        if server['type'] == 'friend':
            files_to_copy = {
                'main.py': FF_BOT_DIR / 'main.py',
                'Fo_pb2.py': FF_BOT_DIR / 'Fo_pb2.py',
                'xTnito.py': FF_BOT_DIR / 'xTnito.py',
                'xKEys.py': FF_BOT_DIR / 'xKEys.py',
                'em.py': FF_BOT_DIR / 'em.py',
                'p.py': FF_BOT_DIR / 'p.py'
            }
            
            for dest_name, source_path in files_to_copy.items():
                if source_path.exists():
                    dest_path = server_dir / dest_name
                    shutil.copy(source_path, dest_path)
                    os.chmod(dest_path, 0o755)
            
            main_script = server_dir / 'main.py'
            bot_data = {
                'bot_name': server.get('bot_name', ''),
                'developer_name': server.get('developer_name', ''),
                'channel_name': server.get('channel_name', '')
            }
            replacements = {
                'BOT_NAME = "DEFAULT_BOT"': f'BOT_NAME = "{bot_data["bot_name"]}"',
                'DEVELOPER_NAME = "DEFAULT_DEV"': f'DEVELOPER_NAME = "{bot_data["developer_name"]}"',
                'CHANNEL_NAME = ""': f'CHANNEL_NAME = "{bot_data["channel_name"]}"',
                "FF_CLient('uid','pas')": f"FF_CLient('{account_info['uid']}','{account_info['password']}')"
            }
            update_script_variables(main_script, replacements)
            
            p_script = server_dir / 'p.py'
            replacements_p = {
                'xid = ""': f'xid = "{account_info["uid"]}"',
                'xpas = ""': f'xpas = "{account_info["password"]}"'
            }
            update_script_variables(p_script, replacements_p)
            
        elif server['type'] == 'clan':
            only_tag = server.get('only_tag', True)
            main_file = 'TcP_GuiLd.py' if only_tag else 'TcP_GuiLd-TaG.py'
            
            files_to_copy = [
                (FF_BOT_DIR / main_file, server_dir / main_file),
                (FF_BOT_DIR / 'xTnito.py', server_dir / 'xTnito.py'),
                (FF_BOT_DIR / 'xKEys.py', server_dir / 'xKEys.py'),
                (FF_BOT_DIR / 'em.py', server_dir / 'em.py'),
                (FF_BOT_DIR / 'clan.py', server_dir / 'clan.py'),
                (FF_BOT_DIR / 'reqClan_pb2.py', server_dir / 'reqClan_pb2.py')
            ]
            
            for source_file, dest_path in files_to_copy:
                if source_file.exists():
                    shutil.copy(source_file, dest_path)
                    os.chmod(dest_path, 0o755)
            
            clan_script = server_dir / main_file
            bot_data = {
                'bot_name': server.get('bot_name', ''),
                'owner_ids': server.get('owner_ids', ''),
                'clan_tag': server.get('clan_tag', ''),
                'clan_id': server.get('clan_id', '')
            }
            replacements = {
                "owners_id=''": f"owners_id='{bot_data['owner_ids']}'",
                "bot_name=''": f"bot_name='{bot_data['bot_name']}'",
                "tag=''": f"tag='{bot_data['clan_tag']}'",
                "FF_CLient('uid','pas')": f"FF_CLient('{account_info['uid']}','{account_info['password']}')"
            }
            update_script_variables(clan_script, replacements)
            
            clan_req_script = server_dir / 'clan.py'
            replacements_clan = {
                "uid = ''": f"uid = '{account_info['uid']}'",
                "pas = ''": f"pas = '{account_info['password']}'",
                "c_id = 'clan id'": f"c_id = '{bot_data['clan_id']}'",
            }
            update_script_variables(clan_req_script, replacements_clan)
            
            em_script = server_dir / 'em.py'
            replacements_em = {
                "uid = \"\"": f"uid='{account_info['uid']}'",
                "pas = \"\"": f"pas='{account_info['password']}'"
            }
            update_script_variables(em_script, replacements_em)
        
        logger.info(f"✅ Refreshed files for server {server['server_id']}")
        return True
    except Exception as e:
        logger.error(f"❌ Error refreshing files for server {server['server_id']}: {e}")
        return False

def restart_all_servers():
    logger.info("🔄 Restarting all servers with fresh files...")
    servers = load_data(SERVERS_FILE)
    
    for server in servers:
        try:
            server_dir = Path(server['path'])
            if not server_dir.exists():
                continue
            
            if server.get('status') == 'Online' and 'process_info' in server:
                for key, pid in list(server['process_info'].items()):
                    if pid and key != 'only_tag':
                        try:
                            os.kill(pid, signal.SIGTERM)
                            time.sleep(0.5)
                            try:
                                os.kill(pid, 0)
                                os.kill(pid, signal.SIGKILL)
                            except ProcessLookupError:
                                pass
                        except:
                            pass
            
            refresh_server_files(server, server_dir)
            
            if server['type'] == 'friend':
                process_info = start_friend_bot_processes(server_dir)
            elif server['type'] == 'clan':
                bot_data = {
                    'bot_name': server.get('bot_name', ''),
                    'owner_ids': server.get('owner_ids', ''),
                    'clan_tag': server.get('clan_tag', ''),
                    'clan_id': server.get('clan_id', '')
                }
                request_data = {'only_tag': server.get('only_tag', True)}
                process_info = start_clan_bot_processes(server_dir, bot_data, {
                    'uid': server.get('account_uid', ''),
                    'password': server.get('account_password', '')
                }, request_data)
            
            if process_info:
                server['status'] = 'Online'
                server['process_info'] = process_info
                logger.info(f"✅ Restarted server {server['server_id']}")
            else:
                server['status'] = 'Offline'
                server['process_info'] = {}
                logger.error(f"❌ Failed to restart server {server['server_id']}")
                
        except Exception as e:
            logger.error(f"❌ Error restarting server {server.get('server_id')}: {e}")
            server['status'] = 'Offline'
            server['process_info'] = {}
    
    save_data(SERVERS_FILE, servers)
    logger.info("✅ Server restart process completed")

def monitor_bots_status():
    try:
        servers = load_data(SERVERS_FILE)
        updated = False
        
        for server in servers:
            if server.get('status') == 'Online' and 'process_info' in server:
                is_running = False
                running_processes = 0
                
                for key, pid in server['process_info'].items():
                    if pid and key != 'only_tag':
                        try:
                            process = psutil.Process(pid)
                            if process.is_running() and process.status() != psutil.STATUS_ZOMBIE:
                                is_running = True
                                running_processes += 1
                        except (psutil.NoSuchProcess, psutil.AccessDenied, ProcessLookupError):
                            continue
                        except Exception as e:
                            logger.error(f"Error checking process {pid}: {e}")
                            continue
                
                if not is_running or running_processes == 0:
                    server['status'] = 'Offline'
                    server['process_info'] = {}
                    updated = True
                    logger.warning(f"⚠️ Bot {server['server_id']} ({server['server_name']}) marked as OFFLINE")
        
        if updated:
            save_data(SERVERS_FILE, servers)
            logger.info("✅ Updated bots status - some bots marked as offline")
    except Exception as e:
        logger.error(f"Error monitoring bots status: {str(e)}", exc_info=True)

def start_status_monitor():
    logger.info("🔄 Starting bots status monitor...")
    while True:
        time.sleep(10)
        monitor_bots_status()

monitor_thread = threading.Thread(target=start_status_monitor, daemon=True)
monitor_thread.start()

def check_server_expiry():
    try:
        servers = load_data(SERVERS_FILE)
        expired_servers = []
        
        for server in servers:
            if 'expires_at' in server:
                expires_at = datetime.strptime(server['expires_at'], "%Y-%m-%d %H:%M:%S")
                if datetime.now() > expires_at:
                    if 'process_info' in server:
                        for key, pid in server['process_info'].items():
                            if pid:
                                try:
                                    os.kill(pid, signal.SIGTERM)
                                except:
                                    pass
                    
                    server_path = Path(server['path'])
                    if server_path.exists():
                        try:
                            shutil.rmtree(server_path)
                        except:
                            pass
                    
                    expired_servers.append(server['server_id'])
        
        if expired_servers:
            servers = [s for s in servers if s['server_id'] not in expired_servers]
            save_data(SERVERS_FILE, servers)
            logger.info(f"🗑️ تم حذف {len(expired_servers)} بوت منتهي الصلاحية")
    except Exception as e:
        logger.error(f"Error checking expiry: {str(e)}")

def manage_friend_bot(server_id, action, uid=None, days=None):
    try:
        servers = load_data(SERVERS_FILE)
        server = next((s for s in servers if s['server_id'] == server_id), None)
        
        if not server:
            return {'success': False, 'message': 'السيرفر غير موجود'}
        
        server_dir = Path(server['path'])
        p_script = server_dir / 'p.py'
        
        if not p_script.exists():
            return {'success': False, 'message': 'سكربت الإدارة غير موجود'}
        
        bot_uid = server.get('account_uid', '')
        bot_password = server.get('account_password', '')
        
        if not bot_uid or not bot_password:
            return {'success': False, 'message': 'بيانات الحساب غير متوفرة'}
        
        if action == 'add' and uid and days:
            cmd = ['python3', str(p_script), 'add', str(uid), str(days), '--bot-uid', bot_uid, '--bot-password', bot_password]
        elif action == 'remove' and uid:
            cmd = ['python3', str(p_script), 'remove', str(uid), '--bot-uid', bot_uid, '--bot-password', bot_password]
        elif action == 'list':
            cmd = ['python3', str(p_script), 'show', '--bot-uid', bot_uid, '--bot-password', bot_password]
        else:
            return {'success': False, 'message': 'الإجراء غير معروف'}
        
        process = subprocess.Popen(cmd, cwd=str(server_dir), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate(timeout=30)
        
        if action == 'list':
            friends = []
            lines = stdout.strip().split('\n')
            for line in lines:
                if 'ID:' in line:
                    parts = line.split('ID:')
                    if len(parts) > 1:
                        friend_id = parts[1].strip()
                        name = "غير معروف"
                        for l in lines:
                            if friend_id in l and 'Name:' in l:
                                name_parts = l.split('Name:')
                                if len(name_parts) > 1:
                                    name = name_parts[1].strip()
                                    break
                        friends.append({'id': friend_id, 'name': name})
            return {'success': True, 'friends': friends, 'count': len(friends)}
        
        if process.returncode == 0:
            try:
                result = json.loads(stdout)
                return {'success': True, 'message': 'تم تنفيذ الإجراء بنجاح', 'data': result}
            except:
                return {'success': True, 'message': 'تم تنفيذ الإجراء بنجاح', 'output': stdout}
        else:
            return {'success': False, 'message': f'فشل في تنفيذ الإجراء: {stderr or stdout}'}
    except subprocess.TimeoutExpired:
        return {'success': False, 'message': 'انتهى الوقت المخصص للعملية'}
    except Exception as e:
        return {'success': False, 'message': str(e)}

def stop_server(server, servers, server_id, save=True):
    try:
        logger.info(f"Stopping server {server_id}...")
        
        if 'process_info' in server and server['process_info']:
            for key, pid in list(server['process_info'].items()):
                if pid and key != 'only_tag':
                    try:
                        os.kill(pid, signal.SIGTERM)
                        time.sleep(0.5)
                        try:
                            os.kill(pid, 0)
                            os.kill(pid, signal.SIGKILL)
                        except ProcessLookupError:
                            pass
                    except ProcessLookupError:
                        pass
                    except Exception as e:
                        logger.error(f"Error stopping {key} (PID: {pid}): {e}")
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cwd']):
                try:
                    proc_cwd = proc.info.get('cwd')
                    if proc_cwd and str(server['path']) in str(proc_cwd):
                        proc.terminate()
                        try:
                            proc.wait(timeout=2)
                        except:
                            proc.kill()
                except:
                    pass
        except Exception as e:
            logger.error(f"Error cleaning orphaned processes: {e}")
        
        server['status'] = 'Offline'
        server['process_info'] = {}
        
        if save:
            save_data(SERVERS_FILE, servers)
        
        return jsonify({'success': True, 'message': 'تم إيقاف السيرفر بنجاح'})
    except Exception as e:
        logger.error(f"Error stopping server: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

def start_server(server, servers, server_dir, server_id):
    try:
        logger.info(f"Starting server {server_id}...")
        
        if not server_dir.exists():
            return jsonify({'success': False, 'message': 'مجلد السيرفر غير موجود'}), 404
        
        refresh_server_files(server, server_dir)
        
        account_info = {'uid': server.get('account_uid', ''), 'password': server.get('account_password', '')}
        
        if server['type'] == 'friend':
            process_info = start_friend_bot_processes(server_dir)
        elif server['type'] == 'clan':
            bot_data = {
                'bot_name': server.get('bot_name', ''),
                'owner_ids': server.get('owner_ids', ''),
                'clan_tag': server.get('clan_tag', ''),
                'clan_id': server.get('clan_id', '')
            }
            request_data = {'only_tag': server.get('only_tag', True)}
            process_info = start_clan_bot_processes(server_dir, bot_data, account_info, request_data)
        
        if process_info:
            server['status'] = 'Online'
            server['process_info'] = process_info
            save_data(SERVERS_FILE, servers)
            return jsonify({'success': True, 'message': 'تم تشغيل السيرفر بنجاح'})
        else:
            server['status'] = 'Offline'
            server['process_info'] = {}
            save_data(SERVERS_FILE, servers)
            return jsonify({'success': False, 'message': 'فشل في تشغيل السيرفر'}), 500
    except Exception as e:
        logger.error(f"Error starting server: {e}")
        server['status'] = 'Offline'
        save_data(SERVERS_FILE, servers)
        return jsonify({'success': False, 'message': str(e)}), 500

def start_friend_bot_processes(server_dir):
    try:
        main_script = server_dir / 'main.py'
        p_script = server_dir / 'p.py'
        em_script = server_dir / 'em.py'
        
        processes = {}
        
        if em_script.exists():
            try:
                proc = subprocess.Popen(
                    ['python3', str(em_script)], cwd=str(server_dir),
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True
                )
                processes['em_pid'] = proc.pid
                time.sleep(2)
            except Exception as e:
                logger.error(f"Error starting em.py: {e}")
        
        if main_script.exists():
            try:
                proc = subprocess.Popen(
                    ['python3', str(main_script)], cwd=str(server_dir),
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True
                )
                processes['bot_pid'] = proc.pid
            except Exception as e:
                logger.error(f"Error starting main bot: {e}")
                return None
        
        if p_script.exists():
            try:
                proc = subprocess.Popen(
                    ['python3', str(p_script)], cwd=str(server_dir),
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True
                )
                processes['panel_pid'] = proc.pid
            except Exception as e:
                logger.error(f"Error starting panel: {e}")
        
        return processes if processes else None
    except Exception as e:
        logger.error(f"Error starting friend bot processes: {e}")
        return None

def start_clan_bot_processes(server_dir, bot_data, account_info, request_data):
    try:
        only_tag = request_data.get('only_tag', True)
        main_file = 'TcP_GuiLd.py' if only_tag else 'TcP_GuiLd-TaG.py'
        
        clan_script = server_dir / main_file
        clan_req_script = server_dir / 'clan.py'
        em_script = server_dir / 'em.py'
        
        processes = {'only_tag': only_tag}
        
        if em_script.exists():
            try:
                proc = subprocess.Popen(
                    ['python3', str(em_script)], cwd=str(server_dir),
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True
                )
                processes['em_pid'] = proc.pid
                time.sleep(2)
            except Exception as e:
                logger.error(f"Error starting em.py: {e}")
        
        if clan_req_script.exists():
            try:
                proc = subprocess.Popen(
                    ['python3', str(clan_req_script)], cwd=str(server_dir),
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
                processes['clan_req_pid'] = proc.pid
                time.sleep(2)
            except Exception as e:
                logger.error(f"Error starting clan request: {e}")
        
        if clan_script.exists():
            try:
                proc = subprocess.Popen(
                    ['python3', str(clan_script)], cwd=str(server_dir),
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True
                )
                processes['bot_pid'] = proc.pid
            except Exception as e:
                logger.error(f"Error starting clan bot: {e}")
                return None
        
        return processes if 'bot_pid' in processes else None
    except Exception as e:
        logger.error(f"Error starting clan bot processes: {e}")
        return None

def update_friend_bot_files(server):
    try:
        server_dir = Path(server['path'])
        main_script = server_dir / 'main.py'
        
        if main_script.exists():
            replacements = {
                'DEVELOPER_NAME = ".*?"': f'DEVELOPER_NAME = "{server.get("developer_name", "")}"',
                'CHANNEL_NAME = ".*?"': f'CHANNEL_NAME = "{server.get("channel_name", "")}"',
                'WELCOME_MSG = ".*?"': f'WELCOME_MSG = "{server.get("welcome_msg", "")}"'
            }
            
            with open(main_script, 'r', encoding='utf-8') as f:
                content = f.read()
            
            for pattern, replacement in replacements.items():
                content = re.sub(pattern, replacement, content)
            
            with open(main_script, 'w', encoding='utf-8') as f:
                f.write(content)
        return True
    except Exception as e:
        logger.error(f"Error updating friend bot files: {e}")
        return False

def update_clan_bot_files(server):
    try:
        server_dir = Path(server['path'])
        only_tag = server.get('only_tag', True)
        main_file = 'TcP_GuiLd.py' if only_tag else 'TcP_GuiLd-TaG.py'
        clan_script = server_dir / main_file
        
        if clan_script.exists():
            replacements = {
                "owners_id='.*?'": f"owners_id='{server.get('owner_ids', '')}'",
                "tag='.*?'": f"tag='{server.get('clan_tag', '')}'"
            }
            
            with open(clan_script, 'r', encoding='utf-8') as f:
                content = f.read()
            
            for pattern, replacement in replacements.items():
                content = re.sub(pattern, replacement, content)
            
            with open(clan_script, 'w', encoding='utf-8') as f:
                f.write(content)
        return True
    except Exception as e:
        logger.error(f"Error updating clan bot files: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    recaptcha_response = request.form.get('g-recaptcha-response')

    # التحقق من reCAPTCHA
    if not verify_recaptcha(recaptcha_response):
        return render_template('index.html', error="يرجى إكمال التحقق من أنك لست روبوت")
    
    users = cached_load(USERS_FILE)
    user = next((u for u in users if u['username'] == username), None)
    
    if not user:
        return render_template('index.html', error="اسم المستخدم غير موجود")
    
    if user['password'] != password:
        return render_template('index.html', error="كلمة المرور غير صحيحة")
    
    user['last_login'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_data(USERS_FILE, users)
    
    session['user'] = username
    session['role'] = user.get('role', 'user')
    
    if username == 'admin':
        session['admin'] = True
    
    return redirect(url_for('user_dashboard'))

@app.route('/user-dashboard')
def user_dashboard():
    if 'user' not in session:
        return redirect(url_for('index'))
    
    users = cached_load(USERS_FILE)
    user = next((u for u in users if u['username'] == session['user']), None)
    
    if not user:
        session.clear()
        return redirect(url_for('index'))
    
    check_server_expiry()
    
    servers = cached_load(SERVERS_FILE)
    user_servers = [s for s in servers if s['owner'] == session['user']]
    
    for server in user_servers:
        if server['type'] == 'friend':
            friends_result = manage_friend_bot(server['server_id'], 'list')
            if friends_result['success']:
                server['friends'] = friends_result['friends']
            else:
                server['friends'] = []
    
    return render_template('user-dashboard.html',
                         username=user['username'],
                         balance=user['balance'],
                         points=user.get('points', 0),
                         role=user.get('role', 'user'),
                         role_name=USER_ROLES.get(user.get('role', 'user'), 'مستخدم'),
                         servers=user_servers,
                         bot_prices=BOT_PRICES)

@app.route('/create-server', methods=['POST'])
def create_server():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'غير مصرح'}), 401
    
    try:
        data = request.get_json()
        server_type = data.get('type')
        server_name = data.get('server_name')

        if server_type not in ['friend', 'clan']:
            return jsonify({'success': False, 'message': 'نوع البوت غير صحيح'}), 400

        if not server_name:
            return jsonify({'success': False, 'message': 'اسم السيرفر مطلوب'}), 400

        if not has_sufficient_points(session['user'], server_type):
            return jsonify({'success': False, 'message': f'نقاطك غير كافية! تحتاج {BOT_PRICES[server_type]} نقاط'}), 400

        if server_type == 'friend':
            bot_data = {
                'bot_name': data.get('bot_name') or data.get('friend_bot_name', 'Friend Bot'),
                'developer_name': data.get('developer_name') or data.get('friend_developer_name', 'C4 Team'),
                'channel_name': data.get('channel_name') or data.get('friend_channel_name', '@C4Team'),
                'welcome_msg': data.get('welcome_msg') or data.get('friend_welcome_msg', 'مرحباً بك صديقي!')
            }
            if not all([server_name, bot_data['bot_name'], bot_data['developer_name']]):
                return jsonify({'success': False, 'message': 'الرجاء ملء جميع الحقول المطلوبة لبوت الصديق'}), 400
                
        elif server_type == 'clan':
            bot_data = {
                'bot_name': data.get('bot_name') or data.get('clan_bot_name', 'Clan Bot'),
                'owner_ids': data.get('owner_ids') or data.get('clan_owner_ids', ''),
                'clan_tag': data.get('clan_tag') or data.get('clan_tag', 'CLAN'),
                'clan_id': data.get('clan_id') or data.get('clan_id', ''),
                'welcome_msg': data.get('welcome_msg') or data.get('clan_welcome_msg', 'مرحباً بك في الكلان!')
            }
            if not all([server_name, bot_data['bot_name'], bot_data['clan_id']]):
                return jsonify({'success': False, 'message': 'الرجاء ملء جميع الحقول المطلوبة لبوت الكلان'}), 400

        future = executor.submit(create_server_async, server_type, session['user'], server_name, bot_data, data)
        
        try:
            success, message = future.result(timeout=45)
        except FutureTimeoutError:
            return jsonify({'success': False, 'message': 'انتهى الوقت المخصص لإنشاء البوت'}), 504

        if success:
            users = cached_load(USERS_FILE)
            user = next((u for u in users if u['username'] == session['user']), None)
            
            return jsonify({
                'success': True,
                'message': f'✅ تم إنشاء بوت {server_type} بنجاح وخصم {BOT_PRICES[server_type]} نقاط',
                'server': {
                    'id': str(len(cached_load(SERVERS_FILE))),
                    'name': server_name, 'type': server_type, 'status': 'Online',
                    'expires_at': (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
                },
                'remaining_points': user.get('points', 0) if user else 0
            })
        else:
            return jsonify({'success': False, 'message': f'❌ {message}'}), 500

    except Exception as e:
        return jsonify({'success': False, 'message': f'حدث خطأ: {str(e)}'}), 500

@app.route('/manage-friend', methods=['POST'])
def manage_friend():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'غير مصرح'}), 401
    
    try:
        data = request.get_json()
        server_id = data.get('server_id')
        action = data.get('action')
        uid = data.get('uid')
        days = data.get('days')
        
        if not server_id or not action:
            return jsonify({'success': False, 'message': 'بيانات ناقصة'}), 400
        
        servers = cached_load(SERVERS_FILE)
        server = next((s for s in servers if s['server_id'] == server_id and s['owner'] == session['user']), None)
        
        if not server:
            return jsonify({'success': False, 'message': 'السيرفر غير موجود أو ليس لديك صلاحية'}), 404
        
        if server['type'] != 'friend':
            return jsonify({'success': False, 'message': 'هذا السيرفر ليس بوت صديق'}), 400
        
        result = manage_friend_bot(server_id, action, uid, days)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/owner/login')
def owner_login_page():
    return render_template('owner-login.html')

@app.route('/owner/login', methods=['POST'])
def owner_login():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    
    users = cached_load(USERS_FILE)
    user = next((u for u in users if u['username'] == username), None)
    
    if not user:
        return render_template('owner-login.html', error="اسم المستخدم غير موجود")
    
    if user['password'] != password:
        return render_template('owner-login.html', error="كلمة المرور غير صحيحة")
    
    if user.get('role') != 'owner':
        return render_template('owner-login.html', error="ليس لديك صلاحية المالك")
    
    user['last_login'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_data(USERS_FILE, users)
    
    session['user'] = username
    session['role'] = 'owner'
    session['owner'] = True
    
    return redirect(url_for('owner_dashboard'))

@app.route('/owner/dashboard')
def owner_dashboard():
    if 'owner' not in session:
        return redirect(url_for('owner_login_page'))
    
    users = cached_load(USERS_FILE)
    servers = cached_load(SERVERS_FILE)
    
    stats = {
        'total_users': len(users), 'total_servers': len(servers),
        'friend_bots': len([s for s in servers if s.get('type') == 'friend']),
        'clan_bots': len([s for s in servers if s.get('type') == 'clan']),
        'online_servers': len([s for s in servers if s.get('status') == 'Online']),
        'total_points': sum(u.get('points', 0) for u in users)
    }
    
    return render_template('owner-dashboard.html', users=users, servers=servers, stats=stats)

@app.route('/owner/manage-points', methods=['POST'])
@owner_required
def manage_points():
    try:
        data = request.get_json()
        target_user = data.get('username')
        action = data.get('action')
        amount = int(data.get('amount', 0))
        reason = data.get('reason', '')
        
        if not target_user or not action or amount <= 0:
            return jsonify({'success': False, 'message': 'بيانات غير صحيحة'}), 400
        
        users = load_data(USERS_FILE)
        target = next((u for u in users if u['username'] == target_user), None)
        
        if not target:
            return jsonify({'success': False, 'message': 'المستخدم غير موجود'}), 404
        
        if action == 'add':
            success = add_points(target_user, amount, reason)
            message = f'تم إضافة {amount} نقطة للمستخدم {target_user}'
        elif action == 'deduct':
            if target.get('points', 0) < amount:
                return jsonify({'success': False, 'message': 'نقاط المستخدم غير كافية'}), 400
            success = deduct_points(target_user, 'manual', amount)
            message = f'تم خصم {amount} نقطة من المستخدم {target_user}'
        elif action == 'set':
            success = set_points(target_user, amount, reason)
            message = f'تم تحديد نقاط المستخدم {target_user} إلى {amount}'
        else:
            return jsonify({'success': False, 'message': 'الإجراء غير معروف'}), 400
        
        if success:
            updated_user = next((u for u in users if u['username'] == target_user), None)
            return jsonify({
                'success': True, 'message': message,
                'user': {'username': updated_user['username'], 'points': updated_user.get('points', 0), 'role': updated_user.get('role', 'user')}
            })
        else:
            return jsonify({'success': False, 'message': 'فشل في تنفيذ العملية'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/owner/users', methods=['GET'])
@owner_required
def get_users():
    users = cached_load(USERS_FILE)
    filtered_users = []
    for user in users:
        if user['role'] != 'owner':
            filtered_users.append({
                'username': user['username'], 'points': user.get('points', 0),
                'role': user.get('role', 'user'), 'servers_count': len(user.get('servers', [])),
                'created_at': user.get('created_at'), 'last_login': user.get('last_login')
            })
    return jsonify({'success': True, 'users': filtered_users, 'count': len(filtered_users)})

@app.route('/owner/transactions', methods=['GET'])
@owner_required
def get_transactions():
    transactions = load_data(TRANSACTIONS_FILE)
    transactions.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    return jsonify({'success': True, 'transactions': transactions[:50], 'count': len(transactions)})

@app.route('/owner/create-admin', methods=['POST'])
@owner_required
def create_admin():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        points = data.get('points', 100)
        
        users = load_data(USERS_FILE)
        
        if any(u['username'] == username for u in users):
            return jsonify({'success': False, 'message': 'اسم المستخدم موجود مسبقاً'}), 400
        
        new_admin = {
            "username": username, "password": password, "balance": 0, "points": points,
            "role": "admin", "servers": [],
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_login": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        users.append(new_admin)
        save_data(USERS_FILE, users)
        
        return jsonify({'success': True, 'message': f'تم إنشاء الأدمن {username} بنجاح'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/owner/change-role', methods=['POST'])
@owner_required
def change_role():
    try:
        data = request.get_json()
        username = data.get('username')
        new_role = data.get('role')
        
        users = load_data(USERS_FILE)
        
        for user in users:
            if user['username'] == username:
                user['role'] = new_role
                save_data(USERS_FILE, users)
                action = "تمت ترقية المستخدم إلى أدمن" if new_role == 'admin' else "تم إزالة صفة الأدمن"
                return jsonify({'success': True, 'message': f'{action} {username}'})
        
        return jsonify({'success': False, 'message': 'المستخدم غير موجود'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/manage-server', methods=['POST'])
def manage_server():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'غير مصرح'}), 401
    
    data = request.get_json()
    server_id = data.get('server_id')
    action = data.get('action')
    
    if not server_id or not action:
        return jsonify({'success': False, 'message': 'بيانات ناقصة'}), 400
    
    servers = load_data(SERVERS_FILE)
    server = next((s for s in servers if s['server_id'] == server_id and s['owner'] == session['user']), None)
    
    if not server:
        return jsonify({'success': False, 'message': 'السيرفر غير موجود أو ليس لديك صلاحية'}), 404
    
    try:
        server_dir = Path(server['path'])
        
        if action == 'stop':
            return stop_server(server, servers, server_id)
        elif action == 'start':
            return start_server(server, servers, server_dir, server_id)
        elif action == 'restart':
            stop_server(server, servers, server_id, save=False)
            time.sleep(2)
            return start_server(server, servers, server_dir, server_id)
        
        return jsonify({'success': False, 'message': 'الإجراء غير معروف'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/delete-server', methods=['POST'])
def delete_server():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'غير مصرح'}), 401
    
    try:
        data = request.get_json()
        server_id = data.get('server_id')
        
        if not server_id:
            return jsonify({'success': False, 'message': 'معرف السيرفر مطلوب'}), 400
        
        servers = load_data(SERVERS_FILE)
        users = load_data(USERS_FILE)
        
        server_index = next((i for i, s in enumerate(servers) if s['server_id'] == server_id and s['owner'] == session['user']), None)
        
        if server_index is None:
            return jsonify({'success': False, 'message': 'السيرفر غير موجود أو ليس لديك صلاحية'}), 404
        
        server = servers[server_index]
        
        try:
            if 'process_info' in server:
                for key, pid in server['process_info'].items():
                    if pid:
                        try:
                            os.kill(pid, signal.SIGTERM)
                            time.sleep(1)
                            try:
                                os.kill(pid, 0)
                                os.kill(pid, signal.SIGKILL)
                            except ProcessLookupError:
                                pass
                        except ProcessLookupError:
                            pass
                        except Exception as e:
                            logger.error(f"Error killing process {pid}: {e}")
        except Exception as e:
            logger.error(f"Error stopping processes: {e}")
        
        server_path = Path(server['path'])
        if server_path.exists():
            try:
                shutil.rmtree(server_path, ignore_errors=False)
            except Exception as e:
                logger.error(f"Error deleting server directory {server_path}: {str(e)}")
                try:
                    import stat
                    def remove_readonly(func, path, _):
                        os.chmod(path, stat.S_IWRITE)
                        func(path)
                    shutil.rmtree(server_path, onerror=remove_readonly)
                except Exception as e2:
                    logger.error(f"Force delete failed: {e2}")
        
        deleted_server = servers.pop(server_index)
        save_data(SERVERS_FILE, servers)
        
        user = next((u for u in users if u['username'] == session['user']), None)
        if user and deleted_server['server_name'] in user.get('servers', []):
            user['servers'].remove(deleted_server['server_name'])
            save_data(USERS_FILE, users)
        
        return jsonify({'success': True, 'message': 'تم حذف السيرفر وملفاته بنجاح'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'حدث خطأ غير متوقع: {str(e)}'}), 500

@app.route('/api/bot-info/<server_id>', methods=['GET'])
def get_bot_info(server_id):
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'غير مصرح'}), 401
    
    servers = cached_load(SERVERS_FILE)
    server = next((s for s in servers if s['server_id'] == server_id and s['owner'] == session['user']), None)
    
    if not server:
        return jsonify({'success': False, 'message': 'البوت غير موجود'}), 404
    
    if server['type'] == 'friend':
        data = {
            'bot_name': server.get('bot_name', ''),
            'developer_name': server.get('developer_name', ''),
            'channel_name': server.get('channel_name', ''),
            'welcome_msg': server.get('welcome_msg', '')
        }
    else:
        data = {
            'bot_name': server.get('bot_name', ''),
            'owner_ids': server.get('owner_ids', ''),
            'clan_tag': server.get('clan_tag', ''),
            'welcome_msg': server.get('welcome_msg', '')
        }
    
    return jsonify({'success': True, 'data': data, 'type': server['type']})

@app.route('/api/update-bot/<server_id>', methods=['POST'])
def update_bot_api(server_id):
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'غير مصرح'}), 401
    
    try:
        data = request.get_json()
        servers = load_data(SERVERS_FILE)
        server = next((s for s in servers if s['server_id'] == server_id and s['owner'] == session['user']), None)
        
        if not server:
            return jsonify({'success': False, 'message': 'البوت غير موجود'}), 404
        
        bot_type = server['type']
        updated = False
        
        if bot_type == 'friend':
            if 'developer_name' in data:
                server['developer_name'] = data['developer_name']
                updated = True
            if 'channel_name' in data:
                server['channel_name'] = data['channel_name']
                updated = True
            if 'welcome_msg' in data:
                server['welcome_msg'] = data['welcome_msg']
                updated = True
        elif bot_type == 'clan':
            if 'owner_ids' in data:
                server['owner_ids'] = data['owner_ids']
                updated = True
            if 'clan_tag' in data:
                server['clan_tag'] = data['clan_tag']
                updated = True
            if 'welcome_msg' in data:
                server['welcome_msg'] = data['welcome_msg']
                updated = True
        
        if updated:
            save_data(SERVERS_FILE, servers)
            server_dir = Path(server['path'])
            if server_dir.exists():
                refresh_server_files(server, server_dir)
                if server.get('status') == 'Online':
                    stop_server(server, servers, server_id, save=False)
                    time.sleep(1)
                    start_server(server, servers, server_dir, server_id)
            return jsonify({'success': True, 'message': 'تم التحديث بنجاح وإعادة تشغيل البوت'})
        else:
            return jsonify({'success': False, 'message': 'لا توجد تغييرات'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/admin')
def admin_login():
    return render_template('admin/login.html')

@app.route('/admin/auth', methods=['POST'])
def admin_auth():
    if request.form.get('admin_key') == "ximad":
        session['admin'] = True
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/login.html', error="Tnak Key Not Found")

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    users = cached_load(USERS_FILE)
    servers = cached_load(SERVERS_FILE)
    
    stats = {
        'total_users': len(users), 'total_servers': len(servers),
        'friend_bots': len([s for s in servers if s.get('type') == 'friend']),
        'clan_bots': len([s for s in servers if s.get('type') == 'clan']),
        'online_servers': len([s for s in servers if s.get('status') == 'Online']),
        'total_points': sum(u.get('points', 0) for u in users)
    }
    
    return render_template('admin/dashboard.html', users=users, servers=servers, stats=stats)

@app.route('/admin/add-user', methods=['POST'])
@admin_required
def admin_add_user():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        points = data.get('points', 0)
        
        if not username or not password:
            return jsonify({'success': False, 'message': 'اسم المستخدم وكلمة المرور مطلوبان'}), 400
        
        users = load_data(USERS_FILE)
        
        if any(u['username'] == username for u in users):
            return jsonify({'success': False, 'message': 'اسم المستخدم موجود مسبقاً'}), 400
        
        new_user = {
            "username": username, "password": password, "balance": 0, "points": points,
            "role": "user", "servers": [],
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_login": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        users.append(new_user)
        save_data(USERS_FILE, users)
        
        return jsonify({'success': True, 'message': f'تم إنشاء المستخدم {username} بنجاح', 'user': {'username': username, 'points': points, 'role': 'user'}})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/admin/update-user', methods=['POST'])
@admin_required
def admin_update_user():
    try:
        data = request.get_json()
        username = data.get('username')
        points = data.get('points')
        password = data.get('password')
        
        if not username:
            return jsonify({'success': False, 'message': 'اسم المستخدم مطلوب'}), 400
        
        users = load_data(USERS_FILE)
        
        for user in users:
            if user['username'] == username:
                if points is not None:
                    user['points'] = points
                if password:
                    user['password'] = password
                save_data(USERS_FILE, users)
                return jsonify({'success': True, 'message': 'تم تحديث بيانات المستخدم بنجاح', 'user': {'username': username, 'points': user['points']}})
        
        return jsonify({'success': False, 'message': 'المستخدم غير موجود'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/admin/delete-user', methods=['POST'])
@admin_required
def admin_delete_user():
    try:
        data = request.get_json()
        username = data.get('username')
        
        if not username:
            return jsonify({'success': False, 'message': 'اسم المستخدم مطلوب'}), 400
        
        if username == 'admin':
            return jsonify({'success': False, 'message': 'لا يمكن حذف حساب الأدمن الرئيسي'}), 403
        
        users = load_data(USERS_FILE)
        servers = load_data(SERVERS_FILE)
        
        user_servers = [s for s in servers if s['owner'] == username]
        for server in user_servers:
            if 'process_info' in server:
                for key, pid in server['process_info'].items():
                    if pid:
                        try:
                            os.kill(pid, signal.SIGTERM)
                        except:
                            pass
            server_path = Path(server['path'])
            if server_path.exists():
                try:
                    shutil.rmtree(server_path)
                except:
                    pass
            servers.remove(server)
        
        users = [u for u in users if u['username'] != username]
        
        save_data(USERS_FILE, users)
        save_data(SERVERS_FILE, servers)
        
        return jsonify({'success': True, 'message': f'تم حذف المستخدم {username} و جميع بوتاته بنجاح'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/admin/add-points', methods=['POST'])
@admin_required
def admin_add_points():
    try:
        data = request.get_json()
        username = data.get('username')
        amount = data.get('amount')
        
        if not username or not amount:
            return jsonify({'success': False, 'message': 'اسم المستخدم والمبلغ مطلوبان'}), 400
        
        users = load_data(USERS_FILE)
        
        for user in users:
            if user['username'] == username:
                user['points'] = user.get('points', 0) + amount
                save_data(USERS_FILE, users)
                log_transaction(username, 'add', amount, f"إضافة من الأدمن: {session.get('user')}")
                return jsonify({'success': True, 'message': f'تم إضافة {amount} نقطة للمستخدم {username}'})
        
        return jsonify({'success': False, 'message': 'المستخدم غير موجود'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/test-connection')
def test_connection():
    return jsonify({
        'success': True, 'message': 'الاتصال يعمل بشكل صحيح',
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_data()
    os.chmod(USER_SERVERS_DIR, 0o777)
    check_server_expiry()
    
    logger.info("="*50)
    logger.info("🚀 C4 Panel Started Successfully!")
    logger.info(f"📁 Data directory: {DATA_DIR}")
    logger.info(f"📁 User servers directory: {USER_SERVERS_DIR}")
    logger.info(f"💰 Bot prices: {BOT_PRICES}")
    logger.info("="*50)
    
    restart_all_servers()
    
    app.run(host='0.0.0.0', port=15540, debug=True, threaded=True)