from time import strptime, localtime

from apiclient.discovery import build
from pprint import PrettyPrinter
from prettytable import PrettyTable

from files.api_key import api_key

base_video_url = 'https://www.youtube.com/watch?v='

youtube = build('youtube', 'v3', developerKey=api_key)
pp = PrettyPrinter()


# ======================== define all search parameters =========================
payload_for_video_search = {
    'q': 'as a software engineer',
    'part': 'snippet',
    'type': 'video',
    'order': 'viewCount',
    'regionCode': 'US',
    'publishedAfter': '2020-10-01T00:00:00Z',
    'maxResults': 50,
}

number_of_videos_to_analyse = 200


# ========================== get videos from search =============================
all_items = []
for i in range(int(number_of_videos_to_analyse / 50)):
    if i != 0:
        if not res.get('nextPageToken'):
            print(f'total videos analysed: {i * 50}')
            break
        payload_for_video_search['pageToken'] = res['nextPageToken']

    request = youtube.search().list(**payload_for_video_search)
    res = request.execute()
    all_items += res['items']


search_results = []
video_ids = []
channel_ids = []

for item in all_items:
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
            'thumbnail_url': item['snippet']['thumbnails'].get('medium', {}).get('url'),
        }
    )


# ========================= get view cont for videos ===========================
all_videos = []
video_ids_count = len(video_ids)
while video_ids_count > 0:
    if video_ids_count >= 50:
        video_ids_count -= 50
        ids_for_req, video_ids = video_ids[:50], video_ids[50:]
    elif 0 < video_ids_count < 50:
        video_ids_count = 0
        ids_for_req = video_ids

    request = youtube.videos().list(
        part="statistics",
        id=','.join(ids_for_req)
    )

    res = request.execute()
    all_videos += res['items']


views = {i['id']: i['statistics'].get('viewCount', 0) for i in all_videos}


# ==================== get subscriber cont for video's channels ================
all_channels = []
ids_for_req = []
channel_ids_count = len(channel_ids)
while channel_ids_count > 0:
    if channel_ids_count >= 50:
        channel_ids_count -= 50
        ids_for_req, channel_ids = channel_ids[:50], channel_ids[50:]
    elif 0 < channel_ids_count < 50:
        channel_ids_count = 0
        ids_for_req = channel_ids

    request = youtube.channels().list(
        part="snippet,statistics",
        id=','.join(ids_for_req)
    )

    res = request.execute()
    all_channels += res['items']

subscribers = {i['id']: i['statistics'].get('subscriberCount') for i in all_channels}


# =================== add numbers and calculate percentage delta ===============
for item in search_results:
    view_count = int(views[item['video_id']] or 0)
    if view_count == 0:
        view_count = 1

    subscriber_count = int(subscribers[item['channel_id']] or 0)

    item['view_count'] = view_count
    item['subscriber_count'] = subscriber_count
    item['percentage_delta'] = round((subscriber_count - view_count) / view_count * 100, 2)


# ====================== sort results and print them ============================
results_to_print = sorted(search_results, key=lambda k: k['percentage_delta'], reverse=True)

t = PrettyTable(
    ['view_count', 'subs_count', '%_delta', 'days_ago', 'link', 'title']
)
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
            base_video_url+item['video_id'],
            item['title'],
        ]
    )

print(t)