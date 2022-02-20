import json

from flask import Flask, request, render_template, redirect, flash
from flask_cors import CORS

from forms import SearchForm
from search import YouTubeSearch
from utils import start_of_time_period

app = Flask(__name__)
app.secret_key = '45s768d9fs7867gr56d879'
CORS(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    search = SearchForm(request.form)
    if request.method == 'POST':
        try:
            return search_results(search)
        except Exception:
            return render_template('error.html')
    return render_template('index.html', form=search)


@app.route('/results')
def search_results(search):
    results = [1]
    search_text = search.data['search']
    time_period = search.data['select']

    if search.data['search'] == '' or not results:
        flash('No results found!')
        return redirect('/')
    else:
        payload = {
            'q': search_text,
            'part': 'snippet',
            'type': 'video',
            'order': 'viewCount',
            'regionCode': 'US',
            'publishedAfter': f"{start_of_time_period(time_period)}T00:00:00Z",
            'maxResults': 50,
        }
        yt_search = YouTubeSearch(payload=payload)
        results = yt_search.get_videos_info()
        # results = [
        #     {
        #         'video_id': 'W8lKqS4dXi4',
        #         'title': 'Fun Science Experiments With Food You Can Easily Try At Home',
        #         'published_at': '2021-10-26T03:00:08Z',
        #         'thumbnail_url': 'https://i.ytimg.com/vi/W8lKqS4dXi4/mqdefault.jpg',
        #         'channel_id': 'UC57XAjJ04TY8gNxOWf-Sy0Q',
        #         'channel_title': '5-Minute Crafts PLAY',
        #         'channel_thumbnail_url': 'https://yt3.ggpht.com/ytc/AKedOLT0uSjDSau89wI1FsyddlQcbPNYqcHdIwc9pOE2BA=s88-c-k-c0x00ffffff-no-rj',
        #         'view_count': 1867309,
        #         'subscriber_count': 19500000,
        #         'percentage_delta': 944.28
        #     },
        #     {'video_id': 'yvGvoyWmv3A', 'title': 'Eating ONLY Dollar Store Food for 24 HOURS!!', 'published_at': '2021-10-26T18:03:05Z', 'thumbnail_url': 'https://i.ytimg.com/vi/yvGvoyWmv3A/mqdefault.jpg', 'channel_id': 'UCilwZiBBfI9X6yiZRzWty8Q', 'channel_title': 'FaZe Rug', 'channel_thumbnail_url': 'https://yt3.ggpht.com/ytc/AKedOLTK0jhw3BqFiS7jkmIGUcZxt22SYG1ypCe-i19OdQ=s88-c-k-c0x00ffffff-no-rj', 'view_count': 2282584, 'subscriber_count': 20200000, 'percentage_delta': 784.96},
        #     {'video_id': 'Nd6uefWZRGQ', 'title': 'Fake Food Covers Empty Grocery Store Shelves to Hide Shortages', 'published_at': '2021-11-16T23:10:52Z', 'thumbnail_url': 'https://i.ytimg.com/vi/Nd6uefWZRGQ/mqdefault.jpg', 'channel_id': 'UC9k-yiEpRHMNVOnOi_aQK8w', 'channel_title': 'Inside Edition', 'channel_thumbnail_url': 'https://yt3.ggpht.com/ytc/AKedOLRlSlGlF-qdw4fp6gJ9t-jlzr3fBZLML-nIASO_=s88-c-k-c0x00ffffff-no-rj', 'view_count': 2033921, 'subscriber_count': 9810000, 'percentage_delta': 382.32},
        #     {'video_id': 'BleImokatPo', 'title': 'Wolfoo Plays 100 Layers Food Challenge with Robot Copy - Learn Good Habits for Kids | Wolfoo Channel', 'published_at': '2021-11-16T10:30:05Z', 'thumbnail_url': 'https://i.ytimg.com/vi/BleImokatPo/mqdefault.jpg', 'channel_id': 'UCWGVQIspqW2j9M3-qLQ0HDg', 'channel_title': 'Wolfoo Channel', 'channel_thumbnail_url': 'https://yt3.ggpht.com/ytc/AKedOLTE50KCKCWBZC3CUKzBWj5ZCckgi10LsnxARHGszA=s88-c-k-c0x00ffffff-no-rj', 'view_count': 2158370, 'subscriber_count': 10300000, 'percentage_delta': 377.21},
        #     {'video_id': 'fOFauSAwYkM', 'title': 'Wolfoo Plays Selling Hot vs Cold Food Challenge with Mom - Kids Stories About Family| Wolfoo Channel', 'published_at': '2021-11-13T10:30:03Z', 'thumbnail_url': 'https://i.ytimg.com/vi/fOFauSAwYkM/mqdefault.jpg', 'channel_id': 'UCWGVQIspqW2j9M3-qLQ0HDg', 'channel_title': 'Wolfoo Channel', 'channel_thumbnail_url': 'https://yt3.ggpht.com/ytc/AKedOLTE50KCKCWBZC3CUKzBWj5ZCckgi10LsnxARHGszA=s88-c-k-c0x00ffffff-no-rj', 'view_count': 2184251, 'subscriber_count': 10300000, 'percentage_delta': 371.56},
        #     {'video_id': 'ciFhAPpFz8Q', 'title': 'Miniature Food Cooking Challenge | Tiny Food Cooking Challenge | Hungry Birds', 'published_at': '2021-11-10T07:50:57Z', 'thumbnail_url': 'https://i.ytimg.com/vi/ciFhAPpFz8Q/mqdefault.jpg', 'channel_id': 'UCTLZ1jlmY-VogpQXng48iKQ', 'channel_title': 'Hungry Birds', 'channel_thumbnail_url': 'https://yt3.ggpht.com/ytc/AKedOLS3mxX0Z9veU-LwbequuCQuNgw9phS7sux_1CSE8Q=s88-c-k-c0x00ffffff-no-rj', 'view_count': 1841179, 'subscriber_count': 7510000, 'percentage_delta': 307.89},
        #     {'video_id': 'b-xLhZZZP9A', 'title': 'Hot Food or Cold Food? - Wolfoo Pretend Play Selling with Toy Store | Wolfoo Family Kids Cartoon', 'published_at': '2021-10-30T03:30:45Z', 'thumbnail_url': 'https://i.ytimg.com/vi/b-xLhZZZP9A/mqdefault.jpg', 'channel_id': 'UCoL0M9swO14BT8u9pTn9MvQ', 'channel_title': 'Wolfoo Family', 'channel_thumbnail_url': 'https://yt3.ggpht.com/ytc/AKedOLQIBNS0cztIeG3Mxq4pIqcWvJEbjhsseiePGOpjFw=s88-c-k-c0x00ffffff-no-rj', 'view_count': 2453236, 'subscriber_count': 9680000, 'percentage_delta': 294.58},
        #     {'video_id': 'cy3ji5K84Mg', 'title': 'ЕДА из РАЗНЫХ СТРАН МИРА ЧЕЛЛЕНДЖ !', 'published_at': '2021-11-12T12:26:12Z', 'thumbnail_url': 'https://i.ytimg.com/vi/cy3ji5K84Mg/mqdefault.jpg', 'channel_id': 'UC2tsySbe9TNrI-xh2lximHA', 'channel_title': 'A4', 'channel_thumbnail_url': 'https://yt3.ggpht.com/ytc/AKedOLTme6SooIKAbseOimCk3ioz8SQFKt1N1YWYKJMtaw=s88-c-k-c0x00ffffff-no-rj', 'view_count': 10899522, 'subscriber_count': 35900000, 'percentage_delta': 229.37},
        #     {'video_id': 'BNnHoVoxpAg', 'title': 'American Street Food - LEGENDARY ROAST PORK Lechonera La Piraña New York City', 'published_at': '2021-11-14T13:03:04Z', 'thumbnail_url': 'https://i.ytimg.com/vi/BNnHoVoxpAg/mqdefault.jpg', 'channel_id': 'UCHKVXtT1YBCYUnnr4apqXfg', 'channel_title': 'Travel Thirsty', 'channel_thumbnail_url': 'https://yt3.ggpht.com/ytc/AKedOLS4ui6xx5UkfioMN3LM5ISUDLL9FiV2wwYLpwtfWQ=s88-c-k-c0x00ffffff-no-rj', 'view_count': 2317697, 'subscriber_count': 7190000, 'percentage_delta': 210.22},
        #     {'video_id': 'OOtfYeEVVjQ', 'title': '$5 PIZZA VS $800 PIZZA!! Everything is BIGGER in Texas!!!', 'published_at': '2021-10-27T12:27:59Z', 'thumbnail_url': 'https://i.ytimg.com/vi/OOtfYeEVVjQ/mqdefault.jpg', 'channel_id': 'UCcAd5Np7fO8SeejB1FVKcYw', 'channel_title': 'Best Ever Food Review Show', 'channel_thumbnail_url': 'https://yt3.ggpht.com/ytc/AKedOLSkYQDLrTzUhu7BstCgxsS0wWAgHP_d9N65Vrnw=s88-c-k-c0x00ffffff-no-rj', 'view_count': 2453356, 'subscriber_count': 7540000, 'percentage_delta': 207.33},
        # ]
        return render_template('results.html', results=results, form=search)


@app.route('/search')
def search_video():
    payload = {
        'q': request.args.get('search_text', 'er'),
        'part': 'snippet',
        'type': 'video',
        'order': 'viewCount',
        'regionCode': request.args.get('location', 'US'),
        'publishedAfter': f"{start_of_time_period(request.args.get('upload_date'))}T00:00:00Z",
        'maxResults': 50,
    }
    search = YouTubeSearch(payload=payload)
    result = search.get_videos_info()
    return json.dumps(result)


if __name__ == '__main__':
    app.run()
