from flask import session
from flask_socketio import emit, join_room, leave_room
from app.moderator.simple_filter import censor_target_words, DEFAULT_SWEAR_WORDS
from .. import socketio

users = {}  # Dictionary to track users in rooms

@socketio.on('joined', namespace='/chat')
def joined(message):
    room = session.get('room')
    user = session.get('name')

    if room not in users:
        users[room] = []

    if user in users[room]:
        emit('username_taken', {'msg': 'Username already taken. Please choose a different one.'})
        return

    join_room(room)
    users[room].append(user)
    emit('status', {'msg': user + ' has entered the room.'}, room=room)
    emit('user_list', {'users': users[room]}, room=room)

@socketio.on('text', namespace='/chat')
def text(message):
    room = session.get('room')
    raw_msg = message['msg']
    moderated_msg = censor_target_words(raw_msg, DEFAULT_SWEAR_WORDS)
    emit('message', {'user': session.get('name'), 'msg': moderated_msg}, room=room)

@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    user = session.get('name')
    leave_room(room)
    if room in users and user in users[room]:
        users[room].remove(user)
    emit('status', {'msg': user + ' has left the room.'}, room=room)
    emit('user_list', {'users': users[room]}, room=room)
