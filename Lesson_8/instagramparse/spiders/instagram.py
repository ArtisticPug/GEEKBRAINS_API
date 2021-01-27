import scrapy
import re
import json
from urllib.parse import urlencode
from copy import deepcopy
from instagramparse.items import InstagramparseItem
from scrapy.http import HtmlResponse


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']

    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = 'THE LOGIN WAS HERE!'
    inst_password = 'THE PASSWORD WAS HERE!'
    parse_users = ['tigerbeer', 'slicebeer', 'mexicalibeer']
    graphql_url = 'https://www.instagram.com/graphql/query/?'
    subscribers_hash = 'c76146de99bb02f6415203be841dd25a'
    subscribed_hash = 'd04b0a864b4b54837c0d870b0e77e076'

    def parse(self, response: HtmlResponse):
        csrf_token = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.user_login,
            formdata={'username': self.inst_login, 'enc_password': self.inst_password},
            headers={'x-csrftoken': csrf_token}
        )

    def user_login(self, response: HtmlResponse):
        j_data = response.json()
        if j_data['authenticated']:
            for user in self.parse_users:
                yield response.follow(
                    f'/{user}',
                    callback=self.user_data_parse,
                    cb_kwargs={'username': user}
                )

    def user_data_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {'id': user_id, 'first': 12}
        url_subscribers = f'{self.graphql_url}query_hash={self.subscribers_hash}&{urlencode(variables)}'
        yield response.follow(
            url_subscribers,
            callback=self.user_subscribers_parse,
            cb_kwargs={
                'username': username,
                'user_id': user_id,
                'variables': deepcopy(variables)
            }
        )

        url_subscribed = f'{self.graphql_url}query_hash={self.subscribed_hash}&{urlencode(variables)}'
        yield response.follow(
            url_subscribed,
            callback=self.user_subscribed_parse,
            cb_kwargs={
                'username': username,
                'user_id': user_id,
                'variables': deepcopy(variables)
            }
        )

    def user_subscribers_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = response.json()
        page_info = j_data.get('data').get('user').get('edge_followed_by').get('page_info')
        if page_info.get('has_next_page'):
            variables['after'] = page_info.get('end_cursor')

            url_subscribers = f'{self.graphql_url}query_hash={self.subscribers_hash}&{urlencode(variables)}'
            yield response.follow(
                url_subscribers,
                callback=self.user_subscribers_parse,
                cb_kwargs={
                    'username': username,
                    'user_id': user_id,
                    'variables': deepcopy(variables)
                }
            )

        subscribers = j_data.get('data').get('user').get('edge_followed_by').get('edges')
        for subscriber in subscribers:
            item = InstagramparseItem(
                _id=subscriber.get('node').get('id'),
                user_name=subscriber.get('node').get('username'),
                user_full_name=subscriber.get('node').get('full_name'),
                user_img=subscriber.get('node').get('profile_pic_url'),
                is_private=subscriber.get('node').get('is_private'),
                subscribed_to={username: user_id}
            )
            yield item

    def user_subscribed_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = response.json()
        page_info = j_data.get('data').get('user').get('edge_follow').get('page_info')
        if page_info.get('has_next_page'):
            variables['after'] = page_info.get('end_cursor')

            url_subscribed = f'{self.graphql_url}query_hash={self.subscribed_hash}&{urlencode(variables)}'
            yield response.follow(
                url_subscribed,
                callback=self.user_subscribed_parse,
                cb_kwargs={
                    'username': username,
                    'user_id': user_id,
                    'variables': deepcopy(variables)
                }
            )

        subscribed = j_data.get('data').get('user').get('edge_follow').get('edges')
        for subscribe in subscribed:
            item = InstagramparseItem(
                _id=subscribe.get('node').get('id'),
                user_name=subscribe.get('node').get('username'),
                user_full_name=subscribe.get('node').get('full_name'),
                user_img=subscribe.get('node').get('profile_pic_url'),
                is_private=subscribe.get('node').get('is_private'),
                subscribed_by={username: user_id}
            )
            yield item

    # Получаем токен для авторизации
    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    # Получаем id желаемого пользователя
    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')
