import json, config
from requests_oauthlib import OAuth1Session

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
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
        print('最初のリクエスト', max_id)
        timelines = json.loads(res.text)
        max_id = timelines[-1]['id']
        for i in range(9):
            print('%d番目のリクエスト' % i, max_id)
            params = {
                'count': 200,
                'screen_name': screen_name,
                'max_id': max_id,
                'exclude_replies': True,
                'include_rts': False
            }
            res = twitter.get(url, params=params)
            append_timelines = json.loads(res.text)
            new_max_id = append_timelines[-1]['id']

            if max_id != new_max_id:
                timelines = timelines + append_timelines
                max_id = new_max_id
            else:
                break
        print('取得ツイート数', len(timelines))
        return timelines
    else:
        return False
