import typer
import functools
import yaml
import textwrap

from datetime import datetime
from wasabi import color
from pathlib import Path
from enum import Enum

from maxbot.commands import bot
from maxbot import studio
from maxbot.cli import add_typer, msg, table

app = typer.Typer()

add_typer(app, name="dialog", help="Dialog operations.")


@app.command("list")
def list_(
    bot_name: str = typer.Option(..., '--bot', '-b', help='Bot name.')
):
    """
        List latest dialogs.
    """
    rows = []
    for c in studio.get_cli_dialogs(bot_name):
        rows.append([c['customer_messenger_id'], c['messenger_type'], c['name']])
    table(
        rows,
        header=["ID","Messenger", "Name"],
        aligns = ("r", "l", "l"),
        divider=True,
    )

# TODO:
#   show scenarios
#   slot handlers
#   show slots


@app.command()
def messages(
    dialog_id: int = typer.Argument(..., help='Dialog ID.'),
    show_quick_reply: bool = typer.Option(False, '--show-quick-reply / --hide-quick-reply', help='Show/hide items and buttons for quick_reply/list/pages commands.'),
    show_skills: bool = typer.Option(True, '--show-skills / --hide-skills', help='Show/hide skills.'),
    show_intents: bool = typer.Option(False, '--show-intents / --hide-intents', help='Show/hide intents full info.'),
    show_entities: bool = typer.Option(False, '--show-entities / --hide-entities', help='Show/hide entities full info.'),
    show_nodes: bool = typer.Option(False, '--show-nodes / --hide-nodes', help='Show/hide nodes journal.'),
    show_slot_filling: bool = typer.Option(False, '--show-slot-filling / --hide-slot-filling', help='Show/hide slot filling journal.'),
    show_scenarios: bool = typer.Option(False, '--show-scenarios / --hide-scenarios', help='Show/hide scenarios.'),
    show_all: bool = typer.Option(False, '--show-all', help='Show all info.'),
    turn_id: int = typer.Option(None, '--turn', help='Turn ID.'),
):
    """
        Show messages in a dialog.

        Use "maxbot dialog list --bot <bot_name>" to get DIALOG_ID for this command.
    """
    turns = studio.get_history_turns(dialog_id)

    repo = CompanyRepo()
    # preload cache to show proper progressbar
    repo.preload(turns)

    show_skill_name = len(get_skill_ids(turns)) > 1
    # propogate flags
    if show_slot_filling or show_scenarios:
        show_nodes = True

    f = Formatter(repo, show_all, show_quick_reply, show_skills, show_skill_name, show_intents,
                  show_entities, show_nodes, show_slot_filling, show_scenarios)
    if turn_id:
        turn = next((t for t in turns if t['event']['event_id'] == turn_id))
        print (f.turn(turn))
    else:
        print (f.history(turns))


def get_skill_ids(turns):
    return set(d['skill_id'] for t in turns for d in t.get('detections', []))


NEWLINE = "\n"


def lines(sep=''):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            return sep.join(list(fn(*args, **kwargs)))
        return wrapper
    return decorator


@lines()
def wrap(text):
    for line in text.splitlines(True):
        yield textwrap.fill(line, width=60, break_long_words=False)
        if line.endswith(NEWLINE):
            yield NEWLINE


def indent(text):
    return textwrap.indent(text, '  ')


def block(icon, text):
    text = textwrap.indent(text, '   ')
    text = f'{icon} ' + text[3:]
    return text


def bullet(bullet, text):
    text = textwrap.indent(text, '  ')
    text = f'{bullet} ' + text[2:]
    return text


def bold(text):
    return color(text, bold=True)


def dump(value):
    if value is None:
        return bold('none')
    text = yaml.dump(value, allow_unicode=True, sort_keys=False)
    text = text.rstrip('\n')
    text = text.rstrip('\n...')
    return text

def dump_flow(value):
    text = yaml.dump(value, allow_unicode=True, sort_keys=False, default_flow_style=True)
    text = text.strip().strip('{}')
    return text


class Formatter(object):

    def __init__(self, repo, show_all, show_quick_reply, show_skills, show_skill_name, show_intents,
                 show_entities, show_nodes, show_slot_filling, show_scenarios):
        self.show_quick_reply = show_quick_reply or show_all
        self.show_skills = show_skills or show_all
        self.show_skill_name = show_skill_name or show_all
        self.show_intents = show_intents or show_all
        self.show_entities = show_entities or show_all
        self.show_nodes = show_nodes or show_all
        self.show_slot_filling = show_slot_filling or show_all
        self.show_scenarios = show_scenarios or show_all
        self.repo = repo

    @lines(2*NEWLINE)
    def history(self, turns):
        for t in turns:
            yield self.turn(t)

    @lines()
    def turn(self, turn):
        dt = self.date(turn['event']['create_date'])
        header = f"#{turn['event']['event_id']}, {dt}"
        yield bold(header)
        yield NEWLINE
        yield self.event(turn['event'])
        for d in turn.get('detections', []):
            if self.show_skills:
                yield NEWLINE
                yield block('🧠', self.detection(d))
            for j in d.get('journals', []):
                for e in j.get('events', []):
                    yield NEWLINE
                    yield(self.event(e))
            if 'broken_flow' in d:
                yield NEWLINE
                yield block('❌', self.broken_flow(d['broken_flow']))

    @lines()
    def detection(self, detection):
        repo = self.repo.get_skill_repo(detection)
        skill = repo.skill
        if self.show_skill_name:
            yield 'skill ' + bold(skill["name"])
            yield NEWLINE
        if 'intent' in detection:
            yield self.intent(detection)
        else:
            yield 'unrecognized intent'
        if 'entities' in detection:
            yield NEWLINE
            yield self.entities(detection)
        if self.show_nodes and 'journals' in detection:
            for j in detection.get('journals', []):
                yield NEWLINE
                yield bullet('*', self.journal_flow(detection, j))

    @lines()
    def intent(self, detection):
        repo = self.repo.get_skill_repo(detection)
        intent = repo.intents[detection['intent']['intent_id']]
        yield bold('intents.' + intent['name'])
        intent_ranking = detection.get('intent_ranking', [])
        if intent_ranking:
            confidence = intent_ranking[0]['confidence']
            yield ' - %.2f' % confidence
        if self.show_intents:
            for i in intent_ranking[1:]:
                name = repo.intents[i['intent_id']]['name']
                yield NEWLINE
                yield 'intents.' + name
                yield ' - %.2f' % i['confidence']

    @lines()
    def journal_flow(self, detection, journal):
        repo = self.repo.get_skill_repo(detection)

        if 'unfocus_node_id' in journal:
            unfocus_node = repo.nodes[journal['unfocus_node_id']]
            yield "unfocus " + bold(unfocus_node['condition'])
            if journal.get('unfocus_reseted'):
                yield " and reset"
            yield NEWLINE

        if 'trigger_node_id' in journal:
            node = repo.nodes[journal['trigger_node_id']]
            yield journal['flow'] + " to " + bold(node['condition'])
        else:
            yield journal['flow']

        if self.show_slot_filling and 'slot_filling' in journal:
            yield NEWLINE
            yield self.journal_slot_filling(detection, journal)
            yield NEWLINE
        else:
            yield ' '

        if 'response' in journal:
            yield 'then response'
            if journal.get('unfocused'):
                yield ' and unfocus'
            if journal.get('reseted'):
                yield ' and reset'
            yield ' and ' + bold(journal['response'])
            if 'focus_node_id' in journal:
                yield ' '

        if 'focus_node_id' in journal:
            focus_node = repo.nodes[journal['focus_node_id']]
            yield "then focus on " + bold(node['condition'])
            yield " with " + bold(journal['transition'])


    @lines(NEWLINE)
    def journal_slot_filling(self, detection, journal):
        repo = self.repo.get_skill_repo(detection)

        for sf in journal.get('slot_filling', []):
            slot = repo.slots[sf['slot_id']]
            if not any(s in sf for s in ['found', 'not_found', 'prompt']):
                yield bullet('-', self.sf_found_simple(slot, sf))
            if 'found' in sf:
                yield bullet('-', self.sf_found(slot, sf))
            if 'not_found' in sf:
                yield bullet('-', self.sf_not_found(slot, sf))
            if 'prompt' in sf:
                yield bullet('-', self.sf_prompt(slot, sf))

    @lines()
    def sf_found_simple(self, slot, sf):
        yield 'found %s ' % self.slot_name(slot)
        yield 'with value '
        yield self.value(sf.get('value'))

    @lines()
    def sf_found(self, slot, sf):
        yield self.sf_found_simple(slot, sf)
        if self.is_multiline(sf.get('value')):
            yield NEWLINE
        else:
            yield ' '
        if sf.get('clear_value'):
            yield 'and clear '
        if not 'prompt' in sf:
            yield self.sf_extras(sf)
        yield 'and ' + sf['found']

    @lines()
    def sf_not_found(self, slot, sf):
        yield 'not_found %s ' % self.slot_name(slot)
        if not 'prompt' in sf:
            yield self.sf_extras(sf)
        yield 'and ' + sf['not_found']

    @lines()
    def sf_prompt(self, slot, sf):
        yield 'prompt %s ' % self.slot_name(slot)
        yield self.sf_extras(sf)
        yield 'and ' + sf['prompt']

    def slot_name(self, slot):
        return bold('slots.' + slot['name'])

    @lines()
    def sf_extras(self, sf):
            if sf.get('focus'):
                yield 'and focus '
            if sf.get('skip'):
                yield 'and skip '

    @lines(NEWLINE)
    def entities(self, detection):
        for e in detection['entities']:
            yield bullet('-', self.entity(detection, e))

    @lines()
    def entity(self, detection, e):
        repo = self.repo.get_skill_repo(detection)
        entity = repo.entities[e['entity_id']]
        yield bold('entities.' + entity['name'])
        yield ' as ' + self.value(e['value'], self.show_entities)
        if self.show_entities:
            data = {}
            if 'literal' in e:
                data = {k:e[k] for k in ['literal', 'start', 'end']}
            if 'extras' in e:
                data['extras'] = e['extras']
                yield NEWLINE
                yield indent(dump(data))
            elif data:
                yield ', '
                yield dump_flow(data)

    def is_multiline(self, value):
        return value and isinstance(value, (list, dict))

    @lines()
    def value(self, value, show_multuline=True):
        if self.is_multiline(value):
            if isinstance(value, list):
                yield 'list'
            if isinstance(value, dict):
                yield 'dictionary'
            if show_multuline:
                yield NEWLINE
                yield indent(dump(value))
            else:
                yield bold('  ...')
        else:
            yield dump(value)

    def date(self, string):
        now = datetime.now()
        dt = datetime.strptime(string, '%Y-%m-%dT%H:%M:%S.%f')
        if dt.year != now.year:
            return dt.strftime('%d %b %Y, %H:%M')
        if dt.month != now.month or dt.day != now.day:
            return dt.strftime('%d %b, %H:%M')
        return dt.strftime('Today, %H:%M')

    @lines()
    def event(self, event):
        if 'text' in event:
            yield block(self.speaker(event), self.text(event))
        elif 'media_type' in event:
            yield block(self.speaker(event), self.media(event))
        elif 'event_type' in event:
            yield block(self.speaker(event), self.thread_event(event))
        elif 'schedule_id' in event:
            yield block('⌛', self.implicit(event, 'Scheduler'))
        elif 'intent' in event:
            if event['intent'] in ['skill_idle', 'system_idle']:
                yield block('✨', self.implicit(event, 'Dialog Support'))
            else:
                yield block('📢', self.implicit(event, 'API Call'))
        else:
            yield yaml.dump(event)

    @lines()
    def implicit(self, event, title):
        yield f"{title} triggers " + bold(event['intent'])
        if 'entities' in event:
            yield NEWLINE
            yield "with"
            yield NEWLINE
            yield self.implicit_arguments(event)

    @lines(NEWLINE)
    def implicit_arguments(self, event):
        for name, value in event['entities'].items():
            text = bold(name) + ' as ' + self.value(value)
            yield bullet('-', text)

    @lines()
    def thread_event(self, event):
        yield f"[{event['event_type']}]"

    @lines()
    def media(self, event):
        yield f"[{event['media_type']}] {event['media_url']}"
        if 'caption' in event:
            yield NEWLINE
            yield wrap(event['caption'])
        if 'file_name' in event:
            yield NEWLINE
            yield wrap(event['file_name'])

    @lines()
    def text(self, event):
        yield wrap(event['text'])
        command = event.get('attachments', {}).get('command', {})
        if not command:
            return
        if self.show_quick_reply:
            yield NEWLINE
            if command == 'quick_reply':
                yield self.command_quick_reply(event)
            elif command == 'list':
                yield self.command_list(event)
            elif command == 'pages':
                yield self.command_pages(event)
        else:
            yield color('  ...', bold=True)

    @lines(NEWLINE)
    def command_quick_reply(self, event):
        for item in event['attachments'].get('items', []):
            yield indent(self.button(item))

    @lines(NEWLINE)
    def command_list(self, event):
        for item in event['attachments'].get('items', []):
            yield bullet('-', self.command_list_item(item))

    @lines()
    def command_list_item(self, item):
        yield wrap(item['title'])
        yield NEWLINE
        if 'subtitle' in item:
            yield wrap(item['subtitle'])
            yield NEWLINE
        yield self.button(item['button'])

    @lines(NEWLINE)
    def command_pages(self, event):
        for item in event['attachments'].get('items', []):
            yield bullet('-', self.command_pages_item(item))

    @lines()
    def command_pages_item(self, item):
        yield wrap(item['title'])
        yield NEWLINE
        if 'subtitle' in item:
            yield wrap(item['subtitle'])
            yield NEWLINE
        for media in item.get('media', []):
            yield f"[{media['media_type']}] {media['media_url']}"
            yield NEWLINE
        yield self.command_pages_item_buttons(item)


    @lines(NEWLINE)
    def command_pages_item_buttons(self, item):
        for button in item.get('buttons', []):
            yield self.button(button)

    def button(self, button):
        return wrap(f"[{button['title']}]")

    def speaker(self, event):
        if event.get('event_type') == 'create' and event.get('thread_creator') == 'customer':
            return '🧑'
        elif event.get('message_type') == 'customer':
            return '🧑'
        elif event.get('operator_id'):
            return '💁'
        elif event.get('message_type') == 'internal':
            return '⚙️ '
        else:
            return '🤖'

    @lines()
    def broken_flow(self, broken_flow):
        yield f"Broken flow by {broken_flow['reason']}"
        yield NEWLINE
        yield wrap(broken_flow['message'])
        if 'xml_document' in broken_flow:
            yield NEWLINE
            yield broken_flow['xml_document']


class CompanyRepo:

    def __init__(self):
        self.repos = {}

    @functools.cached_property
    def skills(self):
        return {s['skill_id']:s for s in studio.get_skills()}

    def get_skill_repo(self, detection):
        key = (detection['skill_id'], detection['snapshot_id'])
        skill = self.skills[detection['skill_id']]
        return self.repos.setdefault(key, SkillRepo(skill, detection['snapshot_id']))

    def preload(self, turns):
        for t in turns:
            for d in t.get('detections', []):
                self.get_skill_repo(d)
        repos = self.repos.values()
        label = 'Preloading %s snapshots of %s skills' % (len(repos), len(get_skill_ids(turns)))
        with typer.progressbar(repos, label=label) as progress:
            for repo in progress:
                repo.intents and repo.entities and repo.slots and repo.nodes


class SkillRepo:

    def __init__(self, skill, snapshot_id):
        self.skill, self.snapshot_id = skill, snapshot_id

    @functools.cached_property
    def intents(self):
        return {i['intent_id']:i for i in studio.get_intents(self.skill['skill_id'], self.snapshot_id)}

    @functools.cached_property
    def entities(self):
        return {i['entity_id']:i for i in studio.get_entities(self.skill['skill_id'], self.snapshot_id)}

    @functools.cached_property
    def slots(self):
        return {i['slot_id']:i for i in studio.get_slots(self.skill['skill_id'], self.snapshot_id)}

    @functools.cached_property
    def nodes(self):
        nodes = studio.get_dialog_nodes(self.skill['skill_id'], self.snapshot_id) + \
            studio.get_silent_nodes(self.skill['skill_id'], self.snapshot_id) + \
            studio.get_urgent_nodes(self.skill['skill_id'], self.snapshot_id)
        return {n['node_id']:n for n in self._flatten_nodes(nodes)}

    def _flatten_nodes(self, nodes):
        yield from nodes
        for n in nodes:
            yield from self._flatten_nodes(n.get('followup', []))
