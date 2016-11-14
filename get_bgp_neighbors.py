#!/isan/bin/python

from cli import *
import time
import os

peers = {}

bgp_states = {
    '1': 'IDLE',
    '2': 'Connect',
    '3': 'Active',
    '4': 'OpenSent',
    '5': 'OpenConfirm',
    '6': 'Established'
}

def message_deliver(text):
    webhook_url = # WEBHOOK URL
    username = "gabriele"
    icon_emoji = ":panda_face:"
    channel = "general"

    body = {
        'username': username,
        'icon_emoji': icon_emoji,
        'text': '[{0}] {1}'.format(hostname, text),
        'channel': channel
    }

    command = '''
    curl -i -k -H "Content-Type: application/x-www-form-urlencoded" -X POST <webhook_url> --data '{0}'
    '''.format(str(body).replace("'", '"'))
    os.system(command)

hostname = json.loads(clid('show hostname'))['hostname']

while True:
    sessions = clid('show bgp sessions vrf management')
    sessions = json.loads(sessions)["TABLE_vrf"]["ROW_vrf"]["TABLE_neighbor"]["ROW_neighbor"]
    print sessions
    if isinstance(sessions, dict):
        sessions = [sessions]

    for session in sessions:
        temp = {}
        neighbor = session["neighbor-id"]
        state = session["state"]

        if peers:
            for key, value in peers.iteritems():
                if key == neighbor and value != state:
                    text = "The BGP peer {0} changed its state from {1} to {2}".format(
                           neighbor, value, state)
                    message_deliver(text)
                    peers[key] = state
                else:
                    peers[neighbor] = state
        else:
            peers[neighbor] = state

    time.sleep(30)