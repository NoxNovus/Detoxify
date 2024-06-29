from app import create_app, socketio
from app.moderator.llm_filter import init_LLMchain

app = create_app(debug=True)

if __name__ == '__main__':
    init_LLMchain()
    socketio.run(app)
