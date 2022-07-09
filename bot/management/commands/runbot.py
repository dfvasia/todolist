import os
from typing import Any

from django.core.management import BaseCommand
from django.core.cache import cache
from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message
from todolist import settings


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient(settings.BOT_TOKEN)

    @staticmethod
    def _generate_verification_code() -> str:
        return os.urandom(12).hex()

    def handle_user_verification(self, msg: Message, tg_user: TgUser):
        code: str = self._generate_verification_code()
        cache.set(code, tg_user.username, timeout=60 * 3)

        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text=f'[verification code] {code}'
        )

    def handle_message(self, msg: Message):
        tg_user, created = TgUser.objects.get_or_create(
            chat_id=msg.chat.id,
            defaults={
                'username': msg.from_.username
            },
        )
        if created:
            self.tg_client.send_message(chat_id=msg.chat.id, text='[hello]')
        elif not tg_user.user:
            self.handle_user_verification(msg=msg, tg_user=tg_user)
        else:
            # self.handle_verified_user(msg=msg, tg_user=tg_user)
            ...

    def handle(self, *args: Any, **options: Any):
        offset = 0
        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                print(item.message)
                # self.tg_client.send_message(chat_id=item.message.chat.id, text=item.message.text)
                self.handle_message(msg=item.message)
