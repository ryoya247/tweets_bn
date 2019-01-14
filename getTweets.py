import json, os
from requests_oauthlib import OAuth1Session

CK = os.environ['CONSUMER_KEY']
CS = os.environ['CONSUMER_SECRET']
AT = os.environ['ACCESS_TOKEN']
ATS = os.environ['ACCESS_TOKEN_SECRET']

twitter = OAuth1Session(CK, CS, AT, ATS)

url = "https://api.twitter.com/1.1/statuses/user_timeline.json"

def get_tweets(screen_name):
    timelines = []
    append_timelines = []
    max_id = None
    new_max_id = None
    params = {
        'count': 200,
        'screen_name': screen_name,
        'exclude_replies': True,
        'include_rts': False
    }

    res = twitter.get(url, params=params)

    if res.status_code == 200:
        timelines = json.loads(res.text)
        max_id = timelines[-1]['id']
        for i in range(16):
            params = {
                'count': 200,
                'screen_name': screen_name,
                'max_id': max_id,
                'exclude_replies': True,
                'include_rts': False
            }
            nres = twitter.get(url, params=params)

            if nres.status_code == 200:
                append_timelines = json.loads(nres.text)
                new_max_id = append_timelines[-1]['id']

                if max_id != new_max_id:
                    timelines = timelines + append_timelines
                    max_id = new_max_id
                else:
                    break
            else:
                break
        return timelines
    else:
        return False
