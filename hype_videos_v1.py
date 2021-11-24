from time import strptime, localtime

from apiclient.discovery import build
from pprint import PrettyPrinter
from prettytable import PrettyTable

from files.api_key import api_key

base_video_url = 'https://www.youtube.com/watch?v='

youtube = build('youtube', 'v3', developerKey=api_key)
pp = PrettyPrinter()

request = youtube.search().list(
    q='software engineer',
    part='snippet',
    type='video',
    order='viewCount',
    regionCode='US',
    publishedAfter='2021-09-25T00:00:00Z',
    maxResults=50,
)

res = request.execute()

search_results = []
video_ids = []
channel_ids = []

for item in res['items']:
    video_ids.append(item['id']['videoId'])
    channel_ids.append(item['snippet']['channelId'])

    search_results.append(
        {
            'etag': item['etag'],
            'video_id': item['id']['videoId'],
            'channel_id': item['snippet']['channelId'],
            'channel_title': item['snippet']['channelTitle'],
            'publish_time': item['snippet']['publishTime'],
            'published_at': item['snippet']['publishedAt'],
            'title': item['snippet']['title'],
        }
    )


# ========================= get view cont for video ===========================
request = youtube.videos().list(
    part="statistics",
    id=','.join(video_ids)
)
res = request.execute()
views = {i['id']: i['statistics']['viewCount'] for i in res['items']}


# ========================= get subscriber cont for video's channel ============
request = youtube.channels().list(
    part="statistics",
    id=','.join(channel_ids)
)
res = request.execute()
subscribers = {i['id']: i['statistics'].get('subscriberCount') for i in res['items']}


# =================== add numbers and calculate percentage delta ============
for item in search_results:
    view_count = int(views[item['video_id']] or 0)
    subscriber_count = int(subscribers[item['channel_id']] or 0)

    item['view_count'] = view_count
    item['subscriber_count'] = subscriber_count
    item['percentage_delta'] = round((subscriber_count - view_count) / view_count * 100, 2)

results_to_print = sorted(search_results, key=lambda k: k['percentage_delta'])

t = PrettyTable(
    ['view_count', 'subs_count', '%_delta', 'days_ago', 'link', 'title']
)
t.align['link'] = "l"
t.align['title'] = "l"

for item in results_to_print:
    days_ago = localtime().tm_mday - strptime(item['published_at'], '%Y-%m-%dT%H:%M:%SZ').tm_mday
    if days_ago < 0:
        days_ago += 30

    t.add_row(
        [
            item['view_count'],
            item['subscriber_count'],
            item['percentage_delta'],
            days_ago,
            base_video_url + item['video_id'],
            item['title'],
        ]
    )

print(t)