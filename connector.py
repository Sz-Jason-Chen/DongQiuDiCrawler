import random
import requests
from retrying import retry


class Connector:
    @staticmethod
    def competition_seasons(competition_id):
        # 拼接url
        url = f"https://api.dongqiudi.com/soccer/biz/data/seasons?competition_id={competition_id}"
        # 创建连接，使用get方法访问
        resp = requests.get(url=url)
        # 提取text，获得字符串
        text = resp.text
        # 关闭连接
        resp.close()
        # 返回字符串
        return text

    @staticmethod
    def schedule(**kwargs):
        url = f"https://api.dongqiudi.com/soccer/biz/data/schedule?"
        for key, value in kwargs.items():
            url += f"{key}={value}&"
        resp = requests.get(url=url)
        text = resp.text
        resp.close()
        return text


    @staticmethod
    # @retry(wait_fixed=1000)
    def match_detail(match_id):
        url = f"https://api.dongqiudi.com/data/detail/match/{match_id}"
        resp = requests.get(url=url)
        text = resp.text
        resp.close()
        return text

    @staticmethod
    def match_lineup(match_id):
        url = f"https://api.dongqiudi.com/soccer/biz/dqd/v1/match/lineup/{match_id}"
        resp = requests.get(url=url)
        text = resp.text
        resp.close()
        return text
