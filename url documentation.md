# 懂球帝api
### 注：
1. 在以下所有的url中，"api.dongqiudi.com/" 可以替换为 "www.dongqiudi.com/api/", 或者 "sport-data.dongqiudi.com/"，这三个没有任何差别（或者我没发现差别）
2. 懂球帝的api并不止这些，下面仅列举项目用到的和未来可能有用的url


## 赛事信息
### 单个赛事
该赛事所有赛季的积分、射手榜、助攻榜、赛程、历史的url，重点是season_id  
https://sport-data.dongqiudi.com/soccer/biz/data/seasons?competition_id=4  

该赛事在特定赛季（season_id）特定比赛周（gameweek）的赛程，如果无round_id和gameweek，则默认第一周  
https://sport-data.dongqiudi.com/soccer/biz/data/schedule?season_id=19915&round_id=214680&gameweek=2&app=dqd&platform=&version=0


## 球队信息
球队的id、名字、位置、主场、成立时间等
https://api.dongqiudi.com/soccer/biz/dqd/team/detail/50122489  

球队的人员名单，包含球员的简单个人数据（但是没有教练）  
https://sport-data.dongqiudi.com/soccer/biz/dqd/team/member/50122489


## 单场比赛信息：
该场比赛的基础信息，包括比赛时间、双方进球和有关url，以及双方的首发和替补阵容  
https://api.dongqiudi.com/data/detail/match/53504440  

该场球员的详细数据，有进攻防守传球失误各方面的指标  
https://api.dongqiudi.com/soccer/biz/dqd/v1/match/lineup/53504440  

比赛双方的近期战绩和预测（小有差别）  
https://api.dongqiudi.com/data/match/pre_analysis_v1/53504440
https://api.dongqiudi.com/data/match/pre_analysis/53504440

赛前用户投票预测结果  
https://api.dongqiudi.com/v2/vote/result/match/53504440

文字概述  
https://api.dongqiudi.com/v4/imserver/baidu/Chatroom/rooms?match_id=53504440


## 其他
从相关文章到积分榜，基本上各种数据都能在api找到，这里姑且列举一些以备后用  
https://api.dongqiudi.com/catalogs  
https://api.dongqiudi.com/v3/archive/app/channel/feeds?id=50004485  
https://sport-data.dongqiudi.com/soccer/biz/data/seasons?competition_id=5542&app=dqd&version=0&platform=web&language=zh-cn  
https://sport-data.dongqiudi.com/soccer/biz/data/standing?season_id=21394&app=dqd&platform=web&version=0&lang=zh-cn  
https://sport-data.dongqiudi.com/soccer/biz/data/standing?app=dqd&lang=zh-cn&season_id=20984  
https://www.dongqiudi.com/api/v3/archive/app/channel/feeds?id=50122489  
https://www.dongqiudi.com/api/data/detail/match/53593293  
https://www.dongqiudi.com/api/v2/config/data_menu?mark=gif&platform=web&version=0&a=4  
https://sport-data.dongqiudi.com/soccer/biz/data/standing?season_id=10267&app=dqd&platform=web&version=0&lang=zh-cn  
