# import uuid
# import re
# from datetime import datetime

# from database import save_message, get_messages
# from llm.chains import ask_llm, ask_llm_stream, reset_chat, generate_image , load_history

# class ChatManager:
#     def __init__(self):
#         self.chat_history = []
#         self.session_id = str(uuid.uuid4())

#     def _format(self, text):
#         return re.sub(r'\*+', '', text).replace('\n', '<br>')

#     def _save(self, role, content):
#         self.chat_history.append({
#             "role": role,
#             "content": content
#         })
#         save_message(self.session_id, role, content)

#     def chat(self, message):
#         if not message:
#             return {"error": "empty message"}

#         self._save("user", message)

#         try:
#             response = ask_llm(message)
#             response = self._format(response)
#         except Exception as e:
#             response = str(e)

#         self._save("assistant", response)

#         return {"role": "assistant", "content": response}

#     def chat_stream(self, message):
#         self._save("user", message)          
#         full_response = []  

#         def generate():
#             for chunk in ask_llm_stream(message):
#                 full_response.append(chunk)  
#                 yield f"data: {chunk}\n\n"
            
#             complete = "".join(full_response).replace('<br>', '\n')
#             self._save("assistant", complete) 
#             yield "data: [DONE]\n\n"

#         return generate

#     def new_session(self):
#         self.chat_history.clear()
#         self.session_id = str(uuid.uuid4())
#         return self.session_id

#     def set_session(self, session_id):
#         self.session_id = session_id
#         self.chat_history = get_messages(session_id)
#         load_history(self.chat_history)
#         return self.chat_history

#     def clear(self):
#         self.chat_history.clear()
#         reset_chat()

#     def generate_image(self, prompt):
#         return generate_image(prompt)











import uuid
import re
from langchain_core.messages import HumanMessage, AIMessage
from database import save_message, get_messages
from llm.chains import ChatBot, generate_image


class ChatManager:
    def __init__(self):
        self.chat_history = []
        self.session_id = str(uuid.uuid4())
        self.bots = {}
        self.bots[self.session_id] = ChatBot()

    def _get_bot(self):
        if self.session_id not in self.bots:
            self.bots[self.session_id] = ChatBot()
        return self.bots[self.session_id]

    def _format(self, text):
        return re.sub(r'\*+', '', text).replace('\n', '<br>')

    def _save(self, role, content):
        self.chat_history.append({"role": role, "content": content})
        save_message(self.session_id, role, content)

    def chat_stream(self, message):
        self._save("user", message)
        full_response = []
        bot = self._get_bot()

        def generate():
            for chunk in bot.ask_stream(message):
                full_response.append(chunk)
                yield f"data: {chunk}\n\n"
            complete = "".join(full_response).replace('<br>', '\n')
            self._save("assistant", complete)
            yield "data: [DONE]\n\n"

        return generate

    def new_session(self):
        self.chat_history.clear()
        self.session_id = str(uuid.uuid4())
        self.bots[self.session_id] = ChatBot()
        return self.session_id

    def set_session(self, session_id):
        self.session_id = session_id
        self.chat_history = get_messages(session_id)

        if session_id not in self.bots:
            bot = ChatBot()
            for m in self.chat_history:
                if m["role"] == "user":
                    bot.history.append(HumanMessage(content=m["content"]))
                elif m["role"] == "assistant":
                    bot.history.append(AIMessage(content=m["content"]))
            self.bots[session_id] = bot

        return self.chat_history

    def clear(self):
        self.chat_history.clear()
        if self.session_id in self.bots:
            self.bots[self.session_id].reset()

    def generate_image(self, prompt):
        return generate_image(prompt)