import os
import sys
import requests
import json
import re
from flask import Flask
from flask import request

app = Flask(__name__)

app.debug = True

USERNAME = 'gitlab'
ICON_URL = 'https://gitlab.com/uploads/project/avatar/13083/gitlab-logo-square.png'
MATTERMOST_WEBHOOK_URL = '' # Paste the Mattermost webhook URL you created here
CHANNEL = '' # Leave this blank to post to the default channel of your webhook
SSL_VERIFY = True

PUSH_EVENT = 'push'
ISSUE_EVENT = 'issue'
TAG_EVENT = 'tag_push'
COMMENT_EVENT = 'note'
MERGE_EVENT = 'merge_request'

REPORT_EVENTS = {
    PUSH_EVENT: False, # On pushes to the repository excluding tags
    ISSUE_EVENT: True, # On creation of a new issue
    TAG_EVENT: False, # On creation of tags
    COMMENT_EVENT: True, # When a new comment is made on commits, merge requests, issues, and code snippets
    MERGE_EVENT: True, # When a merge request is created
}

@app.route('/')
def root():
    """
    Home handler
    """

    return "OK"

@app.route('/new_event', methods=['POST'])
def new_event():
    """
    GitLab event handler, handles POST events from a GitLab project
    """

    if request.json is None:
        print 'Invalid Content-Type'
        return 'Content-Type must be application/json and the request body must contain valid JSON', 400

    data = request.json
    object_kind = data['object_kind']

    text = ''
    base_url = ''

    if REPORT_EVENTS[PUSH_EVENT] and  object_kind == PUSH_EVENT:
        text = '%s pushed %d commit(s) into the `%s` branch for project [%s](%s).' % (
            data['user_name'],
            data['total_commits_count'],
            data['ref'],
            data['repository']['name'],
            data['repository']['homepage']
        )
    elif REPORT_EVENTS[ISSUE_EVENT] and object_kind == ISSUE_EVENT:
        action = data['object_attributes']['action']

        if action == 'open' or action == 'reopen':
            description = add_markdown_quotes(data['object_attributes']['description'])

            text = '#### [%s](%s)\n*[Issue #%s](%s/issues) created by %s in [%s](%s) on [%s](%s)*\n %s' % (
                data['object_attributes']['title'],
                data['object_attributes']['url'],
                data['object_attributes']['iid'],
                data['repository']['homepage'],
                data['user']['username'],
                data['repository']['name'],
                data['repository']['homepage'],
                data['object_attributes']['created_at'],
                data['object_attributes']['url'],
                description
            )

            base_url = data['repository']['homepage']
    elif REPORT_EVENTS[TAG_EVENT] and object_kind == TAG_EVENT:
        text = '%s pushed tag `%s` to the project [%s](%s).' % (
            data['user_name'],
            data['ref'],
            data['repository']['name'],
            data['repository']['homepage']
        )
    elif REPORT_EVENTS[COMMENT_EVENT] and object_kind == COMMENT_EVENT:
        symbol = ''
        type_grammar = 'a'
        note_type = data['object_attributes']['noteable_type'].lower()
        note_id = ''
        parent_title = ''

        if note_type == 'mergerequest':
            symbol = '!'
            note_id = data['merge_request']['iid']
            parent_title = data['merge_request']['title']
            note_type = 'merge request'
        elif note_type == 'snippet':
            symbol = '$'
            note_id = data['snippet']['iid']
            parent_title = data['snippet']['title']
        elif note_type == 'issue':
            symbol = '#'
            note_id = data['issue']['iid']
            parent_title = data['issue']['title']
            type_grammar = 'an'

        subtitle = ''
        if note_type == 'commit':
            subtitle = '%s' % data['commit']['id']
        else:
            subtitle = '%s%s - %s' % (symbol, note_id, parent_title)

        description = add_markdown_quotes(data['object_attributes']['note'])

        text = '#### **New Comment** on [%s](%s)\n*[%s](https://gitlab.com/u/%s) commented on %s %s in [%s](%s) on [%s](%s)*\n %s' % (
            subtitle,
            data['object_attributes']['url'],
            data['user']['username'],
            data['user']['username'],
            type_grammar,
            note_type,
            data['repository']['name'],
            data['repository']['homepage'],
            data['object_attributes']['created_at'],
            data['object_attributes']['url'],
            description
        )

        base_url = data['repository']['homepage']
    elif REPORT_EVENTS[MERGE_EVENT] and object_kind == MERGE_EVENT:
        action = data['object_attributes']['action']

        if action == 'open':
            text_action = 'created a'
        elif action == 'reopen':
            text_action = 'reopened a'
        elif action == 'update':
            text_action = 'updated a'
        elif action == 'merge':
            text_action = 'accepted a'
        elif action == 'close':
            text_action = 'closed a'

        text = '#### [!%s - %s](%s)\n*[%s](https://gitlab.com/u/%s) %s merge request in [%s](%s) on [%s](%s)*' % (
            data['object_attributes']['iid'],
            data['object_attributes']['title'],
            data['object_attributes']['url'],
            data['user']['username'],
            data['user']['username'],
            text_action,
            data['object_attributes']['target']['name'],
            data['object_attributes']['target']['web_url'],
            data['object_attributes']['created_at'],
            data['object_attributes']['url']
        )

        if action == 'open':
            description = add_markdown_quotes(data['object_attributes']['description'])
            text = '%s\n %s' % (
                text,
                description
            )

        base_url = data['object_attributes']['target']['web_url']

    if len(text) == 0:
        print 'Text was empty so nothing sent to Mattermost, object_kind=%s' % object_kind
        return 'OK'

    if len(base_url) != 0:
        text = fix_gitlab_links(base_url, text)

    post_text(text)

    return 'OK'

def post_text(text):
    """
    Mattermost POST method, posts text to the Mattermost incoming webhook URL
    """

    data = {}
    data['text'] = text
    if len(USERNAME) > 0:
        data['username'] = USERNAME
    if len(ICON_URL) > 0:
        data['icon_url'] = ICON_URL
    if len(CHANNEL) > 0:
        data['channel'] = CHANNEL

    headers = {'Content-Type': 'application/json'}
    if SSL_VERIFY:
        r = requests.post(MATTERMOST_WEBHOOK_URL, headers=headers, data=json.dumps(data))
    else:
        r = requests.post(MATTERMOST_WEBHOOK_URL, headers=headers, data=json.dumps(data), verify=False)

    if r.status_code is not requests.codes.ok:
        print 'Encountered error posting to Mattermost URL %s, status=%d, response_body=%s' % (MATTERMOST_WEBHOOK_URL, r.status_code, r.json())

def fix_gitlab_links(base_url, text):
    """
    Fixes gitlab upload links that are relative and makes them absolute
    """

    matches = re.findall('(\[[^]]*\]\s*\((/[^)]+)\))', text)

    for (replace_string, link) in matches:
        new_string = replace_string.replace(link, base_url + link)
        text = text.replace(replace_string, new_string)

    return text

def add_markdown_quotes(text):
    """
    Add Markdown quotes around a piece of text
    """

    if len(text) == 0:
        return ''

    split_desc = text.split('\n')

    for index, line in enumerate(split_desc):
        split_desc[index] = '> ' + line

    return '\n'.join(split_desc)

if __name__ == "__main__":
    MATTERMOST_WEBHOOK_URL = os.environ.get('MATTERMOST_WEBHOOK_URL', '')
    CHANNEL = os.environ.get('CHANNEL', CHANNEL)
    USERNAME = os.environ.get('USERNAME', USERNAME)
    ICON_URL = os.environ.get('ICON_URL', ICON_URL)
    SSL_VERIFY = os.environ.get('SSL_VERIFY', 'True') == 'True'

    REPORT_EVENTS[PUSH_EVENT] = os.environ.get('PUSH_TRIGGER', str(REPORT_EVENTS[PUSH_EVENT])) == 'True'
    REPORT_EVENTS[ISSUE_EVENT] = os.environ.get('ISSUE_TRIGGER', str(REPORT_EVENTS[ISSUE_EVENT])) == 'True'
    REPORT_EVENTS[TAG_EVENT] = os.environ.get('TAG_TRIGGER', str(REPORT_EVENTS[TAG_EVENT])) == 'True'
    REPORT_EVENTS[COMMENT_EVENT] = os.environ.get('COMMENT_TRIGGER', str(REPORT_EVENTS[COMMENT_EVENT])) == 'True'
    REPORT_EVENTS[MERGE_EVENT] = os.environ.get('MERGE_TRIGGER', str(REPORT_EVENTS[MERGE_EVENT])) == 'True'

    if len(MATTERMOST_WEBHOOK_URL) == 0:
        print 'MATTERMOST_WEBHOOK_URL must be configured. Please see instructions in README.md'
        sys.exit()

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
