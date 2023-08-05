import datetime
import json
import pandas as pd


class Text:
    def __init__(self, raw):
        # 将传入的字符串用json解析
        # self.content可直接以字典与列表组合的形式访问
        self.content = json.loads(raw)
        # 以后这里可以加一些别的格式的输入，然后进行统一格式，比如eval()


class CompetitionSeasonsText(Text):
    def __init__(self, raw):
        super().__init__(raw=raw)

    def get_season_id(self, season_name):
        """
        关于 next(item["season_id"] for item in self.content if item["season_name"] == season_name) 的解释：
        self.content是一个列表，item是列表中的元素，同时item本身是一个字典，有名为"season_name"的键
        for item in self.content if item["season_name"] == season_name 就是在依据season_name挑选item
        item["season_id"] 则是返回满足条件的item的"season_id"键的值，这将被存在一个列表中
        next()返回迭代器的第一个值，在这里就是将for-if的列表转为字典，因为有且只可能有一个值满足条件
        next()还可以指定默认值，如果迭代器耗尽，则返回默认值，这在MatchLineupText中使用以处理没有特定键值对的情况
        """
        return next(item["season_id"] for item in self.content if item["season_name"] == season_name)

class MatchDetailText(Text):
    def __init__(self, raw):
        super().__init__(raw=raw)

    def get_competition_name(self):
        return self.content["matchSample"]["competition_name"]

    def get_group_name(self):
        return self.content["matchSample"]["group_name"]

    def get_score(self):
        score = {"team_A": self.content["matchSample"]["as_A"],
                 "team_B": self.content["matchSample"]["as_B"], }
        return score

    def get_start_play(self):
        return datetime.datetime.fromisoformat(self.content["matchSample"]["start_play"])

    def get_team_a_name(self):
        return self.content["matchSample"]["team_A_name"]

    def get_team_b_name(self):
        return self.content["matchSample"]["team_B_name"]

    def get_team_names(self):
        team_names = {"team_A": self.content["matchSample"]["team_A_name"],
                      "team_B": self.content["matchSample"]["team_B_name"]}
        return team_names


class MatchLineupText(Text):
    def __init__(self, raw):
        super().__init__(raw=raw)

        # 储存个人比赛数据的字典
        # 格式为 {"key1": [value1, value2...], "key2": [value1, value2...] ... }
        personal_data = {}

        for team in ["team_A", "team_B"]:
            for person in self.content["persons"][team]["lineups"]:
                # 如果字典里没有"team_name"这个键，那么创建此键，初始默认值为空列表，这样第一个值才能使用append添加
                # 如果已经有，那么直接append
                personal_data.setdefault("team_name", []).append(self.content["persons"][team]["team_name"])

                personal_data.setdefault("person_id", []).append(person["person_id"])
                personal_data.setdefault("person_name", []).append(person["person"])
                personal_data.setdefault("shirt_number", []).append(person["shirtnumber"])
                personal_data.setdefault("position", []).append(person["position"])

                # keys：关键数据
                keys = person["statistics"]["keys"]
                """"[{"type": "出场时间", "data": "90'"},
                     {"type": "扑救", "data": "1"},
                     {"type": "进球/助攻","data": "0/0"},
                     {"type": "红牌/黄牌","data": "0/0"}]"""

                personal_data.setdefault("playing_time", []).append(
                    next((item["data"] for item in keys if item["type"] == "出场时间"), None))
                personal_data.setdefault("goal", []).append(
                    next((item["data"] for item in keys if item["type"] == "进球"), None))
                personal_data.setdefault("assist", []).append(
                    next((item["data"] for item in keys if item["type"] == "助攻"), None))
                personal_data.setdefault("goalkeeping", []).append(
                    next((item["data"] for item in keys if item["type"] == "扑救"), None))
                red_yellow = next((item["data"] for item in keys if item["type"] == "红牌/黄牌"),
                                  None)  # 获取 "红牌/黄牌" 字段的数据
                personal_data.setdefault("red_card", []).append(red_yellow.split("/")[0])
                personal_data.setdefault("yellow_card", []).append(red_yellow.split("/")[1])

        self.personal_df = pd.DataFrame(personal_data)

    def get_personal_df(self):
        return self.personal_df

    def get_personal(self, *args):
        return self.personal_df[list(args)]


class ScheduleText(Text):
    def __init__(self, raw):
        super().__init__(raw=raw)
        self.rounds = self.content["content"]["rounds"]
        self.matches = self.content["content"]["matches"]

    def get_round_id(self):
        return self.rounds[1]["params"]["round_id"]

    def get_gameweeks(self):
        gameweeks = [item["params"]["gameweek"] for item in self.rounds]
        return gameweeks

    def get_matches_ids(self):
        matches_ids = [item["match_id"] for item in self.matches]
        return matches_ids