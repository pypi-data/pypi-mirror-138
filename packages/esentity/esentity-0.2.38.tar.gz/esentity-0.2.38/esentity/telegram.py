#coding: utf-8
import requests
from loguru import logger
from base64 import b64encode
from esentity.models import TelegramBot


def telegram_api(token, method, json={}):
    r = requests.post(f'https://api.telegram.org/bot{token}/{method}', json=json)
    if r.status_code == 200:
        _res = r.json()
        logger.info(f'Telegram {method} response: {_res}')
        return _res
    else:
        logger.info(f'Telegram {method} response code: {r.status_code}')
    return {}


def telegram_getMe(token):
    res = telegram_api(token, 'getMe')
    if res['ok']:
        return {
            'bot_id': res['result']['id'],
            'first_name': res['result']['first_name'],
            'username': res['result']['username'],
            'can_join': res['result']['can_join_groups'],
            'can_read': res['result']['can_read_all_group_messages'],
        }                
    return {}


def telegram_setWebhook(token, url):
    res = telegram_api(token, 'setWebhook', {'url': url, 'drop_pending_updates': True})


def telegram_getChatAdministrators(token, chat):
    res = telegram_api(token, 'getChatAdministrators', {'chat_id': chat})
    if 'ok' in res and res['ok']:
        return [str(item['user']['id']) for item in res['result'] if item['user']['is_bot']]
    return []


def telegram_getChat(token, chat):
    res = telegram_api(token, 'getChat', {'chat_id': chat})
    if res.get('ok'):
        _res = {
            'chat_id': res['result']['id'],
            'title': res['result']['title'],
            'type': res['result']['type'],
            'linked_chat': res['result'].get('linked_chat_id'),
        }
        if 'permissions' in res['result']:
            _res['can_send'] = res['result']['permissions']['can_send_messages']
            _res['can_invite'] = res['result']['permissions']['can_invite_users']
        if 'photo' in res['result']:
            res_photo = telegram_api(token, 'getFile', {'file_id': res['result']['photo']['small_file_id']})
            if res_photo.get('ok'):
                r = requests.get(f"https://api.telegram.org/file/bot{token}/{res_photo['result']['file_path']}")
                if r.status_code == 200:
                    _res['photo'] = b64encode(r.content).decode()
        return _res                
    return {}


def telegram_checkChat(_doc):
    _res = {}
    _err = {}
    bots, found = TelegramBot.get(username=_doc['bot_admin'])
    if found == 1:
        bot = bots.pop()

        chat_id = f"@{_doc['username']}"
        _admins = telegram_getChatAdministrators(bot.token, chat_id)
        if bot.bot_id in _admins:
            telegram_api(bot.token, 'setChatTitle', {'chat_id': chat_id, 'title': _doc['title']})
            telegram_api(bot.token, 'setChatDescription', {'chat_id': chat_id, 'description': _doc['description'] or ''})
            telegram_api(bot.token, 'setChatPermissions', {'chat_id': chat_id, 'permissions': {
                'can_send_messages': _doc['can_send'],
                'can_invite_users': _doc['can_invite'],
            }})
            _res = telegram_getChat(bot.token, chat_id)
            _res.update(telegram_getChatMemberCount(bot.token, chat_id))
        else:
            _err = {
                'username': 'No access to chat'
            }
    else:
        _err = {
            'bot_admin': 'Bot not found'
        }
    return _res, _err


def telegram_getChatMemberCount(token, chat):
    res = telegram_api(token, 'getChatMemberCount', {'chat_id': chat})
    if 'ok' in res and res['ok']:
        _res = {
            'count': res['result'],
        }
        return _res                
    return {}