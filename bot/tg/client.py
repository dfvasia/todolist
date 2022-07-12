import requests

from bot.tg.dc import GetUpdatesResponse, SendMessageResponse


class TgClient:
    def __init__(self, token):
        self.token = token

    def get_url(self, method: str):
        return f"https://api.telegram.org/bot{self.token}/{method}"

    @staticmethod
    def __re_key(inp_dict):
        keys_replace = {'edited_message': 'message'}
        return {keys_replace.get(k, k): v for k, v in inp_dict.items()}

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        url = self.get_url('getUpdates')
        resp = requests.get(url, params={'offset': offset, 'timeout': timeout}).json()
        if resp['result'] != [] and 'edited_message' in resp['result'][0]:
            r_p = self.__re_key(resp['result'][0])
            resp['result'].pop(0)
            resp['result'].insert(0, r_p)
        return GetUpdatesResponse(**resp)

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        url = self.get_url('sendMessage')
        resp = requests.get(url, params={'chat_id': chat_id, 'text': text})
        return SendMessageResponse(**resp.json())
