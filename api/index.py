from flask import Flask, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# 対戦部屋の一覧を取得する
@app.route('/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello, World!'})

# クライアントが接続したとき
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)

@socketio.on('leave')
def on_leave(data):
    room = data['room']
    leave_room(room)

# メッセージを受信
@socketio.on('diff_player')
def handle_diff_player_event(data):
    room = data['room']
    print(f'Received message: {data}')
    # 別のクライアントにブロードキャスト
    emit('diff_player', "diff_player", broadcast=True, to=room)

# メッセージを受信
@socketio.on('start_event')
def handle_start_event(data):
    room = data['room']
    print(f'Received message: {data}')
    # 別のクライアントにブロードキャスト
    emit('start_event', "game_start", broadcast=True, to=room)

# メッセージを受信
@socketio.on('kill_event')
def handle_kill_event(data):
    room = data['room']
    print(f'Received message: {data}')
    # 別のクライアントにブロードキャスト
    emit('kill_event', data, broadcast=True, to=room)

if __name__ == '__main__':
    # socketio.run(app, host='0.0.0.0', port=5000, ssl_context=('./cert.pem', './key.pem'))
    socketio.run(app, port=5000)

