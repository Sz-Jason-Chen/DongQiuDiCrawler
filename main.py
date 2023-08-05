import time
from connector import Connector
from multiprocessing.dummy import Pool
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
    print(match_detail_text.get_team_a_name())
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
    print(f"使用单线程获取所有场次的match_id，需要访问{len(gameweeks)}次")
    start = time.time()
    all_match_ids = []
    for gameweek in gameweeks:
        gameweek_schedule = ScheduleText(
            raw=Connector.schedule(season_id=season_id, round_id=round_id, gameweek=gameweek))
        all_match_ids.extend(gameweek_schedule.get_matches_ids())
    print(all_match_ids)
    end = time.time()
    spend = end - start
    print(f"总耗时{spend}秒， 平均每单元耗时{spend / len(gameweeks)}秒")

    # 获取所有场次的team_names
    print(f"使用多线程获取所有场次的队伍名，需要访问{len(all_match_ids)}次")
    start = time.time()

    # match_texts列表存放MatchDetailText的实例
    match_texts = []
    # 建立线程池，设置线程数为100
    pool = Pool(100)

    # 将单个线程执行的任务封装为函数
    # 接收一个match_id，将获取的文本实例化并append
    def single_thread(match_id):
        raw = Connector.match_detail(match_id=match_id)
        match_detail_text = MatchDetailText(raw=raw)
        match_texts.append(match_detail_text)

    # 将all_match_ids的元素分配给single_thread函数，并多线程执行
    pool.map(single_thread, all_match_ids)

    # 由于网速浮动，比赛信息虽然是按序访问，但并不是按序写入，所以对Text实例按比赛开始的时间进行排序
    sorted_match_texts = sorted(match_texts, key=lambda text: text.get_start_play())
    # 打印结果
    for text in sorted_match_texts:
        print(f"{text.get_start_play()}: {text.get_team_a_name()} vs {text.get_team_b_name()}")

    end = time.time()
    spend = end - start
    print(f"耗时{spend}秒，平均每单元耗时{spend / len(all_match_ids)}秒")


if __name__ == "__main__":
    main()
