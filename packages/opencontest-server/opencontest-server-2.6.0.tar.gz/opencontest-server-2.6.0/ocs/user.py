from secrets import token_hex
from hashlib import pbkdf2_hmac
from requests import post

from ocs.db import con, cur


# TODO: Periodically clear out unused tokens
tokens = {}  # Create tokens object


def hash(password, salt):
    """Hash password with salt"""

    return salt + pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)


def check_password(username, password):
    """Check if a password is correct"""

    users = cur.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchall()
    if len(users) == 0:
        return 404  # Username not found
    if users[0][3] == hash(password, users[0][3][:32]):
        return 200
    return 403  # Incorrect password


def create_user(name, email, username, password):
    """Create a new user in the database"""

    cur.execute('INSERT INTO users VALUES (?, ?, ?, ?)', (name, email, username, hash(password, os.urandom(32))))
    con.commit()


def modify_user(name, email, username, password):
    """Modify user account information"""    

    if name != '':   
        cur.execute('UPDATE users SET name = ? where username = ?', (name,  username))
    if email != '':
        cur.execute('UPDATE users SET email = ? where username = ?', (email,  username))
    if password != '':
        cur.execute('UPDATE users SET password = ? where username = ?', (hash(password, os.urandom(32)),  username))
    con.commit()


def delete_user(name, email, username, password):
    """Delete a user from the database"""

    cur.execute('DELETE FROM users where username = ?', (username,))
    con.commit()


def make_token(username, server):
    """Create and return a token"""

    token = token_hex(32)
    for s in server.split():
        post(('https://' if s.find('://') == -1 else '') + s, json={
            'type': 'authorize', 'username': username, 'token': token})
    return token


def save_token(username, token):
    """Save token"""

    if username not in tokens:
        tokens[username] = set()
    tokens[username].add(token)


def check_token(username, token):
    """Check if a token is valid"""
    
    if username in tokens and token in tokens[username]:
        tokens[username].remove(token)
        return True
    return False
