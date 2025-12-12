import sys
import os
import eventlet
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename
from server.database_manager import DatabaseManager
from common.steganography import LSBSteganography
from common.crypto import DESManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gizli_anahtar_burasi'
app.config['UPLOAD_FOLDER'] = 'server/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

socketio = SocketIO(app, cors_allowed_origins="*")
db = DatabaseManager()
stego = LSBSteganography()
online_users = {}

@app.route('/register', methods=['POST'])
def register():
    if 'image' not in request.files or 'username' not in request.form:
        return jsonify({"status": "error", "message": "Eksik veri"}), 400
    file = request.files['image']
    username = request.form['username']
    if file.filename == '': return jsonify({"status": "error", "message": "Dosya yok"}), 400

    filename = secure_filename(file.filename)
    if not os.path.exists(app.config['UPLOAD_FOLDER']): os.makedirs(app.config['UPLOAD_FOLDER'])
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    extracted_password = stego.extract_password(filepath)
    if not extracted_password: return jsonify({"status": "error", "message": "Şifre bulunamadı!"}), 400

    success = db.add_user(username, extracted_password)
    if success: return jsonify({"status": "success", "message": f"{extracted_password}"}), 200
    else: return jsonify({"status": "error", "message": "Kullanıcı adı alınmış"}), 409

@socketio.on('login')
def handle_login(data):
    username = data['username']
    online_users[username] = request.sid
    print(f"[ONLINE] {username}")
    emit('user_list_update', {'users': db.get_all_users(), 'online': list(online_users.keys())}, broadcast=True)
    
    for sender, msg, ts in db.get_offline_messages(username):
        emit('receive_message', {'sender': sender, 'message': msg, 'is_offline': True}, room=request.sid)

@socketio.on('send_message')
def handle_message(data):
    sender, receiver, encrypted_msg = data['sender'], data['receiver'], data['message']
    
    sender_pass = db.get_user_password(sender)
    receiver_pass = db.get_user_password(receiver)
    
    if sender_pass and receiver_pass:
        # C1 anahtarı ile çöz, C2 anahtarı ile şifrele
        plain_text = DESManager(sender_pass).decrypt(encrypted_msg)
        re_encrypted = DESManager(receiver_pass).encrypt(plain_text)
        
        if receiver in online_users:
            emit('receive_message', {'sender': sender, 'message': re_encrypted}, room=online_users[receiver])
        else:
            db.save_offline_message(sender, receiver, re_encrypted)

@socketio.on('disconnect')
def handle_disconnect():
    for u, s in list(online_users.items()):
        if s == request.sid:
            del online_users[u]
            emit('user_list_update', {'users': db.get_all_users(), 'online': list(online_users.keys())}, broadcast=True)
            break

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)