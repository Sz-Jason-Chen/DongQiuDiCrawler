from connector import Connector
from text import *


def main():
    # 样例代码
    # 使用Connector访问，返回未经处理的字符串
    raw_text = Connector.match_detail(match_id=53504440)
    # 将字符串塞进Text类
    match_detail_text = MatchDetailText(raw=raw_text)
    # 用get系列函数获取格式化数据
    print(match_detail_text.get_competition_name())
    print(match_detail_text.get_group_name())
    print(match_detail_text.get_start_play())
    print(match_detail_text.get_team_names())
    print(match_detail_text.get_team_a_names())
    print(match_detail_text.get_score())

    # 另一个示例
    raw_text = Connector.match_lineup(match_id=53504440)
    match_lineup_text = MatchLineupText(raw=raw_text)
    # 这个是pandas包的dataframe格式
    print(match_lineup_text.get_personal_df())
    print(match_lineup_text.get_personal("person_id", "person_name"))

    # 以下部分是一个综合示例：在一个赛事（英超）的一个赛季（2022-23）中批量获取每一场比赛的对阵双方

    # 获取这个赛事的所有赛季
    competition_seasons_text = CompetitionSeasonsText(raw=Connector.competition_seasons(competition_id=4))
    # 获得22/23这一赛季的season_id
    season_id = competition_seasons_text.get_season_id(season_name="22/23")
    print(season_id)

    # 获取每周详细赛程，需要round_id，故先获取这一赛季共有的round_id
    season_schedule = ScheduleText(raw=Connector.schedule(season_id=season_id))
    round_id = season_schedule.get_round_id()
    # 获取所有比赛周（gameweek所有可用的值，超出范围会默认返回第一周的赛程)
    gameweeks = season_schedule.get_gameweeks()
    print(round_id, gameweeks)

    # 获取所有场次的match_id
    all_match_ids = []
    for gameweek in gameweeks:
        gameweek_schedule = ScheduleText(raw=Connector.schedule(season_id=season_id, round_id=round_id, gameweek=gameweek))
        all_match_ids.extend(gameweek_schedule.get_matches_ids())
    print(all_match_ids)

    # 获取所有场次的team_names
    for match_id in all_match_ids:
        raw = Connector.match_detail(match_id=match_id)
        match_detail_text = MatchDetailText(raw=raw)
        print(match_detail_text.get_team_names())



if __name__ == "__main__":
    main()
