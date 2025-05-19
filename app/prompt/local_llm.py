from app.prompt.cohere import INetworkLLM
import requests
import json
import logging

logger = logging.getLogger(__name__)

LMSTUDIO_CHAT_URL = "api/v1/chat/completions"
LMSTUDIO_SERVER_URL = "host.docker.internal"


class LocalLMStudioLLM(INetworkLLM):
    def __init__(self, model, port):
        self._model = model
        self._port = port

    def ask_question(self, user_input, context, temperature=1.0, max_tokens=-1):
        full_prompt = (f"Contesta <question> teniendo como contexto la informacion en <context>."
                       f"<context>{context}</context>"
                       f"<question>{user_input}</question>"
                       )
        response = self.__send_request(full_prompt, temperature, max_tokens)
        answer = self.__parse_response(response)

        return answer

    def __send_request(self, content: str, temperature, max_tokens):
        url = f"http://{LMSTUDIO_SERVER_URL}:{self._port}/{LMSTUDIO_CHAT_URL}"
        logger.info(url)
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "model": self._model,
            "messages": [
                {"role": "user", "content": content}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"LocalLMStudioLLM Request Error: {e}")
            return None

    @staticmethod
    def __parse_response(response):
        return response['choices']['message']['content']
