// Custom Alert System
function showAlert(type, title, message, duration = 3000) {
    const alert = document.getElementById('customAlert');
    const alertIcon = document.getElementById('customAlertIcon');
    const alertTitle = document.getElementById('customAlertTitle');
    const alertMessage = document.getElementById('customAlertMessage');
    
    alert.className = `custom-alert custom-alert-${type}`;
    alertTitle.textContent = title;
    alertMessage.textContent = message;
    
    // Set appropriate icon
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

// دالة عرض نافذة التأكيد المخصصة
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

// Add new user
document.getElementById('addUserForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const userData = {
        username: document.getElementById('newUsername').value,
        password: document.getElementById('newPassword').value,
        balance: document.getElementById('newBalance').value
    };
    
    try {
        const response = await fetch('/admin/add-user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert('success', 'User Added!', 'User created successfully!');
            setTimeout(() => {
                window.location.reload();
            }, 1500);
        } else {
            showAlert('error', 'Error', result.message || 'Failed to add user');
        }
    } catch (error) {
        showAlert('error', 'Network Error', error.message || 'Failed to connect to server');
    }
});

// Edit User Functions
function openEditUserModal(username, balance) {
    document.getElementById('editUsername').value = username;
    document.getElementById('editUsernameTitle').textContent = username;
    document.getElementById('editBalance').value = balance;
    document.getElementById('editPassword').value = '';
    document.getElementById('editUserModal').classList.add('active');
}

function closeEditUserModal() {
    document.getElementById('editUserModal').classList.remove('active');
}

document.getElementById('editUserForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const userData = {
        username: document.getElementById('editUsername').value,
        balance: document.getElementById('editBalance').value,
        password: document.getElementById('editPassword').value || null
    };
    
    try {
        const response = await fetch('/admin/update-user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert('success', 'User Updated!', 'User information updated successfully!');
            closeEditUserModal();
            setTimeout(() => {
                window.location.reload();
            }, 1500);
        } else {
            showAlert('error', 'Error', result.message || 'Failed to update user');
        }
    } catch (error) {
        showAlert('error', 'Network Error', error.message || 'Failed to connect to server');
    }
});

// Delete user
async function confirmDeleteUser(username) {
    const result = await showConfirm(
        'Delete User', 
        `Are you sure you want to delete user "${username}"? This will also delete all their servers!`,
        true
    );
    
    if (result === 'delete') {
        try {
            const response = await fetch('/admin/delete-user', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                showAlert('success', 'Deleted!', 'User has been deleted successfully');
                setTimeout(() => {
                    window.location.reload();
                }, 1500);
            } else {
                showAlert('error', 'Error', result.message || 'Failed to delete user');
            }
        } catch (error) {
            showAlert('error', 'Network Error', error.message || 'Failed to connect to server');
        }
    }
}

// Server management functions
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