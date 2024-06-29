from app import create_app, socketio
from app.moderator.llm_filter import LLMChain

llm_chain = LLMChain()
app = create_app(debug=True)

if __name__ == '__main__':
    llm_chain.init_LLMchain()
    socketio.run(app)
