// Custom Alert System
function showAlert(type, title, message, duration = 3000) {
    const alert = document.getElementById('customAlert');
    const alertIcon = document.getElementById('customAlertIcon');
    const alertTitle = document.getElementById('customAlertTitle');
    const alertMessage = document.getElementById('customAlertMessage');
    
    alert.className = `custom-alert custom-alert-${type}`;
    alertTitle.textContent = title;
    alertMessage.textContent = message;
    
    if (type === 'success') {
        alertIcon.textContent = '✓';
    } else if (type === 'error') {
        alertIcon.textContent = '✗';
    } else if (type === 'warning') {
        alertIcon.textContent = '⚠';
    }
    
    alert.classList.add('show');
    
    setTimeout(() => {
        alert.classList.remove('show');
    }, duration);
}

function showConfirm(title, message, isDelete = false) {
    return new Promise((resolve) => {
        const overlay = document.getElementById('confirmOverlay');
        const confirmTitle = document.getElementById('confirmTitle');
        const confirmMessage = document.getElementById('confirmMessage');
        const confirmOk = document.getElementById('confirmOk');
        const confirmCancel = document.getElementById('confirmCancel');
        const confirmDelete = document.getElementById('confirmDelete');
        
        confirmTitle.textContent = title;
        confirmMessage.textContent = message;
        
        if (isDelete) {
            confirmOk.style.display = 'none';
            confirmDelete.style.display = 'block';
        } else {
            confirmOk.style.display = 'block';
            confirmDelete.style.display = 'none';
        }
        
        overlay.classList.add('active');
        
        const cleanUp = () => {
            overlay.classList.remove('active');
            confirmOk.onclick = null;
            confirmCancel.onclick = null;
            confirmDelete.onclick = null;
        };
        
        confirmOk.onclick = () => {
            cleanUp();
            resolve('confirm');
        };
        
        confirmDelete.onclick = () => {
            cleanUp();
            resolve('delete');
        };
        
        confirmCancel.onclick = () => {
            cleanUp();
            resolve('cancel');
        };
    });
}

function hideForm() {
    document.getElementById('serverForm').style.display = 'none';
}

document.getElementById('createServerForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        server_name: document.getElementById('serverName').value,
        server_id: document.getElementById('serverId').value,
        type: document.getElementById('serverType').value,
        password: document.getElementById('serverPassword').value,
        welcome_msg: document.getElementById('welcomeMessage').value,
        welcome_msg2: document.getElementById('welcomeMessage2').value,
        team_name: document.getElementById('teamName').value,
        owner_id: document.getElementById('ownerId').value,
        emoji: document.getElementById('welcomeEmoji').value || '🎉'
    };
    
    // Add panel config only for friend servers
    if (formData.type === 'friend') {
        formData.bot_token = document.getElementById('botToken').value;
        formData.chat_id = document.getElementById('chatId').value;
        formData.owner_chat_id = document.getElementById('ownerChatId').value;
    }
    
    // Add clan tag if it's a clan server
    if (formData.type === 'clan') {
        formData.clan_tag = document.getElementById('clanTag').value;
    }
    
    // Validate server ID is numbers only
    if (!/^\d+$/.test(formData.server_id)) {
        showAlert('error', 'Invalid Server ID', 'Server ID must contain numbers only');
        return;
    }
    
    try {
        const response = await fetch('/create-server', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert('success', 'Server Created!', `Server "${formData.server_name}" created successfully!`);
            setTimeout(() => {
                window.location.reload();
            }, 1500);
        } else {
            showAlert('error', 'Creation Failed', result.message || 'Failed to create server');
        }
    } catch (error) {
        showAlert('error', 'Network Error', error.message || 'Failed to connect to server');
    }
});

function editServer(serverId) {
    const editForm = document.getElementById(`editForm-${serverId}`);
    editForm.style.display = editForm.style.display === 'none' ? 'block' : 'none';
    
    if (editForm.style.display === 'block') {
        editForm.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
}

async function updateServer(event, serverId) {
    event.preventDefault();
    
    const data = {
        welcome_msg: document.getElementById(`editWelcome-${serverId}`).value,
        welcome_msg2: document.getElementById(`editWelcome2-${serverId}`).value,
        team_name: document.getElementById(`editTeamName-${serverId}`).value,
        owner_id: document.getElementById(`editOwnerId-${serverId}`).value,
        emoji: document.getElementById(`editEmoji-${serverId}`).value || '🎉'
    };
    
    // Add panel config only for friend servers
    const serverType = document.getElementById('serverType').value;
    if (serverType === 'friend') {
        data.bot_token = document.getElementById(`editBotToken-${serverId}`).value;
        data.chat_id = document.getElementById(`editChatId-${serverId}`).value;
        data.owner_chat_id = document.getElementById(`editOwnerChatId-${serverId}`).value;
    }
    
    // Add clan tag if it exists
    const clanTagInput = document.getElementById(`editClanTag-${serverId}`);
    if (clanTagInput) {
        data.clan_tag = clanTagInput.value;
    }
    
    try {
        const response = await fetch(`/update-server/${serverId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert('success', 'Updated!', 'Server settings updated successfully!');
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            showAlert('error', 'Error', result.message || 'Failed to update server');
        }
    } catch (error) {
        showAlert('error', 'Network Error', error.message);
    }
}

async function confirmManageServer(serverId, currentStatus, serverName) {
    const action = currentStatus === 'Online' ? 'stop' : 'start';
    const result = await showConfirm(
        'Confirm Action', 
        `Are you sure you want to ${action} server "${serverName}"?`
    );
    
    if (result === 'confirm') {
        try {
            const response = await fetch('/manage-server', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    server_id: serverId,
                    action: action
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                showAlert('success', 'Success!', `Server has been ${action}ed`);
                setTimeout(() => {
                    window.location.reload();
                }, 1500);
            } else {
                showAlert('error', 'Error', result.message || `Failed to ${action} server`);
            }
        } catch (error) {
            showAlert('error', 'Network Error', error.message || 'Failed to connect to server');
        }
    }
}

async function confirmDeleteServer(serverId, serverName) {
    const result = await showConfirm(
        'Delete Server', 
        `Are you sure you want to permanently delete server "${serverName}"? This action cannot be undone!`,
        true
    );
    
    if (result === 'delete') {
        try {
            const response = await fetch('/delete-server', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    server_id: serverId
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                showAlert('success', 'Deleted!', 'Server has been deleted successfully');
                setTimeout(() => {
                    window.location.reload();
                }, 1500);
            } else {
                showAlert('error', 'Error', result.message || 'Failed to delete server');
            }
        } catch (error) {
            showAlert('error', 'Network Error', error.message || 'Failed to connect to server');
        }
    }
}

// Initialize form controls
document.addEventListener('DOMContentLoaded', function() {
    const formControls = document.querySelectorAll('.form-control');
    formControls.forEach(control => {
        control.addEventListener('focus', function() {
            this.style.boxShadow = '0 0 0 2px var(--primary)';
        });
        
        control.addEventListener('blur', function() {
            this.style.boxShadow = 'none';
        });
    });
});