import os
import requests
import dotenv
import json
import logging
from datetime import datetime
from get_log import Logger

class Notion:
    def __init__(self, json_path):
        with open(json_path, 'r') as file:
            self.db_json = json.load(file)

        self._notion_api_key = os.environ.get("NOTION_API_KEY")
        self._headers = {
            "Authorization": "Bearer " + self._notion_api_key,
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

        # for logging
        self.logger = Logger().get_logger()
    
    def create_db(self, page_id, title):
        post_url = 'https://api.notion.com/v1/databases/'
        
        self.db_json['parent']['page_id'] = page_id
        self.db_json['title'] = [{
            "type": "text",
            "text": {
                "content": title
            }
        }]

        # 요청 전송
        response = requests.post(post_url, headers=self._headers, json=self.db_json)
        
        if response.status_code == 200:
            return response.json()
        else:
            return response.text
    
    def update_db(self, text, url):
        post_url = 'https://api.notion.com/v1/pages/'

        # 오늘 날짜 받아오기
        date = datetime.today().strftime('%Y-%m-%d')

        # title과 description 받아오기
        title, description = self.parse_input(text)

        self.db_json['properties']['title']['title'][0]['text']['content'] = title
        self.db_json['properties']['Description']['rich_text'][0]['text']['content'] = description
        self.db_json['properties']['Date']['date']['start'] = date
        self.db_json['properties']['URL']['url'] = url

        # 요청 전송
        response = requests.post(post_url, headers=self._headers, json=self.db_json)

        if response.status_code == 200:
            return response.json()
        else:
            logging.error("Request failed")
            return response.text

    def parse_input(self, input_str):
        try:
            title_part = input_str.split('title:')[1].split('context:')[0].strip()
            context_part = input_str.split('context:')[1].strip()
        except IndexError:
            raise ValueError("Input string is not in the expected format: 'title: <title> context: <context>'")

        return title_part, context_part










