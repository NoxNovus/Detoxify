from flask import session
from flask_socketio import emit, join_room, leave_room
from app.moderator.llm_filter import LLM_moderate
from app.moderator.simple_filter import censor_target_words, DEFAULT_SWEAR_WORDS
from .. import socketio

MAX_USERNAME_LENGTH = 32
users = {}  # Dictionary to track users in rooms

@socketio.on('joined', namespace='/chat')
def joined(message):
    room = session.get('room')
    user = session.get('name')

    if len(user) > MAX_USERNAME_LENGTH:
        emit('username_invalid', {'msg': f'Username cannot be longer than {MAX_USERNAME_LENGTH} characters.'})
        return

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
    moderated_msg = LLM_moderate('msg')
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
