import requests
import typer
import textwrap
import json

from wasabi import msg, table

from maxbot.cli import read_api_config_or_fail, STATE, memory


session = requests.Session()


def _fail_for_status(resp):
    if STATE['verbose']:
        req = resp.request
        msg.divider()
        msg.text(f'{req.method} {req.url}')
        if req.body:
            msg.text(req.body.decode())
        msg.text(f'HTTP {resp.status_code} {resp.reason}')
        try:
            print(json.dumps(resp.json(), ensure_ascii=False, indent=2))
        except requests.exceptions.JSONDecodeError:
            print(resp.text)
    if not resp.ok:
        try:
            detail = resp.json().get('detail')
            parts = detail.split('\n')
            title = parts[0] # workaround long and ugly swagger errors
            text = textwrap.shorten("\n".join(parts[1:]), width=1000)
            msg.fail(f'Error: {title}', text, exits=1)
        except requests.exceptions.JSONDecodeError:
            msg.fail(f'HTTP {resp.status_code} {resp.reason}', resp.text, exits=1)


def post(path, json):
    cfg = read_api_config_or_fail()
    resp = session.post(f"{cfg['api_url']}{path}", json=json, headers={
        'Authorization': f"Bearer {cfg['api_key']}"
    })
    _fail_for_status(resp)
    return resp.json()


def put(path, json):
    cfg = read_api_config_or_fail()
    resp = session.put(f"{cfg['api_url']}{path}", json=json, headers={
        'Authorization': f"Bearer {cfg['api_key']}"
    })
    _fail_for_status(resp)
    return resp.json()


def get(path, params=None):
    cfg = read_api_config_or_fail()
    resp = session.get(f"{cfg['api_url']}{path}", params=params, headers={
        'Authorization': f"Bearer {cfg['api_key']}"
    })
    _fail_for_status(resp)
    return resp.json()


def delete(path):
    cfg = read_api_config_or_fail()
    resp = session.delete(f"{cfg['api_url']}{path}", headers={
        'Authorization': f"Bearer {cfg['api_key']}"
    })
    _fail_for_status(resp)
    return resp.json()


def get_cli_bots():
    return get('/v1/cli/bots').get('bots')


def post_cli_bots(data):
    return post('/v1/cli/bots', json=data)


def put_cli_bots(name, data):
    return put(f'/v1/cli/bots/{name}', json=data)


def delete_cli_bots(name):
    delete(f"/v1/cli/bots/{name}")


def get_cli_dialogs(bot):
    return get(f'/v1/cli/dialogs?bot={bot}').get('dialogs')


def get_history_turns(customer_messenger_id):
    return get(f'/v1/history/{customer_messenger_id}/turns').get('turns')


def post_cli_login(api_url, phone_number, password):
    resp = requests.post(f"{api_url}/v1/cli/login", json={'phone_number': phone_number, 'password': password})
    _fail_for_status(resp)
    return resp.json().get('api_key')


def get_skills():
    return get('/v1/skills').get('skills')


@memory.cache
def get_intents(skill_id, snapshot_id):
    return get(f'/v1/skills/{skill_id}/intents?snapshot_id={snapshot_id}').get('intents')


@memory.cache
def get_entities(skill_id, snapshot_id):
    return get(f'/v1/skills/{skill_id}/entities?snapshot_id={snapshot_id}').get('entities')


@memory.cache
def get_slots(skill_id, snapshot_id):
    return get(f'/v1/skills/{skill_id}/slots?snapshot_id={snapshot_id}').get('slots')


@memory.cache
def get_dialog_nodes(skill_id, snapshot_id):
    return get(f'/v1/skills/{skill_id}/nodes?snapshot_id={snapshot_id}').get('nodes')


@memory.cache
def get_urgent_nodes(skill_id, snapshot_id):
    return get(f'/v1/skills/{skill_id}/urgent_nodes?snapshot_id={snapshot_id}').get('nodes')


@memory.cache
def get_silent_nodes(skill_id, snapshot_id):
    return get(f'/v1/skills/{skill_id}/silent_nodes?snapshot_id={snapshot_id}').get('nodes')
