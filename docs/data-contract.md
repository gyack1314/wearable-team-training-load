# 业务资料契约

所有人物、家庭、设备、供应商和交易均为本地合成资料。金额使用整数分，时长字段的单位写在列说明中。时间戳含时区，起止区间均为左闭右开。空值表示未观察或未提供，数值零保留其真实含义。

activity 是设备测得的区间，来源不同的相交片段不预先去重。participation 记录教练通知与实际出席，不用于覆盖个人设备事实。强度等级1到3为该营内部相对等级。没有设备记录不表示没有运动。

## people.csv

人员主档。第一列是物理记录的唯一键。

- `person` 表示人员编号，类型为 str。
- `household` 表示登记家庭编号，类型为 str。
- `segment` 表示长期客群，类型为 str。
- `home_zone` 表示常居时区，类型为 str。
## activity.csv

设备观测到的活动区间。第一列是物理记录的唯一键。

- `record` 表示记录，类型为 str。
- `person` 表示队员，类型为 str。
- `device` 表示来源设备，类型为 str。
- `session` 表示来源活动，类型为 str。
- `sport` 表示运动类型，类型为 str。
- `start` 表示开始，类型为 datetime。
- `end` 表示结束，类型为 datetime。
- `distance_m` 表示距离米，类型为 float，允许空值。
- `mean_hr` 表示平均心率，类型为 float，允许空值。
- `hr_coverage` 表示心率覆盖比例，类型为 float。
- `received` 表示收到时间，类型为 datetime。
## feedback.csv

队员主观用力及疲劳反馈。第一列是物理记录的唯一键。

- `record` 表示反馈，类型为 str。
- `person` 表示队员，类型为 str。
- `date` 表示活动日，类型为 date。
- `rpe` 表示主观用力1到10，类型为 int，允许空值。
- `fatigue` 表示疲劳1到10，类型为 int，允许空值。
- `received` 表示接收，类型为 datetime。
## classes.csv

团课候选与来源已通知活动。第一列是物理记录的唯一键。

- `class` 表示团课，类型为 str。
- `sport` 表示类型，类型为 str。
- `start` 表示开始，类型为 datetime。
- `end` 表示结束，类型为 datetime。
- `coach` 表示教练，类型为 str。
- `venue` 表示场地，类型为 str。
- `intensity` 表示强度等级，类型为 int。
- `minimum` 表示最低人数，类型为 int。
- `capacity` 表示最多人数，类型为 int。
- `status` 表示状态，类型为 str。
## participation.csv

参与意向、通知及出席事实。第一列是物理记录的唯一键。

- `record` 表示记录，类型为 str。
- `class` 表示团课，类型为 str。
- `person` 表示队员，类型为 str。
- `mode` 表示参与方式，类型为 str。
- `status` 表示事实类型，类型为 str。
## availability.csv

队员可参加窗口。第一列是物理记录的唯一键。

- `record` 表示窗口，类型为 str。
- `person` 表示队员，类型为 str。
- `start` 表示开始，类型为 datetime。
- `end` 表示结束，类型为 datetime。
- `max_intensity` 表示允许的最高强度，类型为 int。
## resources.csv

教练与场地的资源窗口。第一列是物理记录的唯一键。

- `record` 表示记录，类型为 str。
- `resource` 表示资源，类型为 str。
- `start` 表示开始，类型为 datetime。
- `end` 表示结束，类型为 datetime。
- `capacity` 表示同时容纳活动数，类型为 int。

数值条款、可调整范围及业务枚举见 data/terms.json。数据契约定义来源记录和已存在的协议，分析方法及内部实现由项目使用者按业务需求选择。
