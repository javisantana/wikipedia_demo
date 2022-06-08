import json
import requests
import os
from sseclient import SSEClient as EventSource

BUFFER_SIZE = 10
url = 'https://stream.wikimedia.org/v2/stream/recentchange'
tb_url = 'https://api.tinybird.co/v0/events?name=edit_events'
buff = []
for event in EventSource(url):
    if event.event == 'message':
        try:
            buff.append(event.data.encode('utf8'))
            if len(buff) > BUFFER_SIZE:
                headers = {
                    'Authorization': f"Bearer {os.getenv('TB_TOKEN_APPEND')}"
                }
                r = requests.post(tb_url, data=b'\n'.join(buff), headers=headers)
                print(r.status_code, len(buff))
                buff = []
        except ValueError:
            pass
