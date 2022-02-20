import apiclient.discovery as apc
from files.api_key import api_key
import timeago, datetime

from utils import human_format


class YouTubeSearch:
    def __init__(self, payload):
        self.base_video_url = 'https://www.youtube.com/watch?v='
        self.number_of_videos_to_analyse = 250
        self.youtube = apc.build('youtube', 'v3', developerKey=api_key)
        self.payload = payload

    def get_videos_info(self):
        all_items = []
        for i in range(int(self.number_of_videos_to_analyse / 50)):
            if i != 0:
                if not res.get('nextPageToken'):
                    break
                self.payload['pageToken'] = res['nextPageToken']

            request = self.youtube.search().list(**self.payload)
            res = request.execute()
            all_items += res['items']

        video_ids = []
        channel_ids = []

        for item in all_items:
            video_ids.append(item['id']['videoId'])
            channel_ids.append(item['snippet']['channelId'])

            item.pop('etag')
            item.pop('kind')

            item['video_id'] = item['id']['videoId']
            item.pop('id')
            item['title'] = item['snippet']['title']
            item['published_at'] = item['snippet']['publishedAt']
            item['thumbnail_url'] = item['snippet']['thumbnails'].get('medium', {}).get('url')
            item['channel_id'] = item['snippet']['channelId']
            item['channel_title'] = item['snippet']['channelTitle']

            item.pop('snippet')

        all_videos = self.get_view_count_for_videos(video_ids)
        views = {i['id']: i['statistics'].get('viewCount', 0) for i in all_videos}

        all_channels = self.get_channels_info(channel_ids)
        channels_info = {
            i['id']: {
                'subs_count': i['statistics'].get('subscriberCount'),
                'thumbnail_url': i['snippet']['thumbnails'].get('default', {}).get('url')
            }
            for i in all_channels
        }

        for item in all_items:
            # we are dividing by view_count when calculating percentage_delta
            # we can not divide by zero
            view_count = int(views[item['video_id']] or 1)

            # sometimes for some reasons channel is not available
            # so there is no channel with such channel id in channels_info
            # subscriber_count = 1000000000 => video will appear in the end of the list
            try:
                subscriber_count = int(channels_info[item['channel_id']]['subs_count'] or 1000000000)
                item['channel_thumbnail_url'] = channels_info[item['channel_id']]['thumbnail_url']
            except KeyError:
                subscriber_count = 1000000000
                item['channel_thumbnail_url'] = None

            item['video_url'] = self.base_video_url + item['video_id']
            item['time_ago'] = timeago.format(
                datetime.datetime.strptime(item['published_at'], '%Y-%m-%dT%H:%M:%SZ'),
                now=datetime.datetime.now()
            )

            item['view_count'] = human_format(view_count)
            item['subscriber_count'] = human_format(subscriber_count)
            item['percentage_delta'] = round((subscriber_count - view_count) / view_count * 100, 2) * -1

        return sorted(all_items, key=lambda k: k['percentage_delta'], reverse=True)[:50]

    def get_videos_from_search(self):
        pass

    def get_view_count_for_videos(self, video_ids):
        all_videos = []
        video_ids_count = len(video_ids)
        while video_ids_count > 0:
            if video_ids_count >= 50:
                video_ids_count -= 50
                ids_for_req, video_ids = video_ids[:50], video_ids[50:]
            elif 0 < video_ids_count < 50:
                video_ids_count = 0
                ids_for_req = video_ids

            request = self.youtube.videos().list(
                part="statistics",
                id=','.join(ids_for_req)
            )

            res = request.execute()
            all_videos += res['items']

        return all_videos

    def get_channels_info(self, channel_ids):
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

            request = self.youtube.channels().list(
                part="snippet,statistics",
                id=','.join(ids_for_req)
            )

            res = request.execute()
            all_channels += res['items']

        return all_channels
