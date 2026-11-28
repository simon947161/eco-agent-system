# 挪威鱼加工厂分时负荷

Eirik S. Svendsen、Kristina N. Widell、Håkon Selvnes、Alexis Sevault、Armin Hafner、Tom Ståle Nordtvedt，2022，版本 v1。数据及说明由作者按 CC BY 4.0 发布。source/ 下为两份未经改写的原文件，已核对发布者 MD5。cleaned.csv 是本项目转换的派生表。[数据与归属](https://doi.org/10.5281/zenodo.6563580) · [许可](https://creativecommons.org/licenses/by/4.0/)

2021-01-05 00:00 至 01-14 23:00，作者已将传感器数据整理为制冷系统 1 与电锅炉的分时电功率。时间保留来源时钟，未给时区。本次解码制表符、十进制逗号，统一成 ISO 格式，仅检查完整连续小时并保留原精度。240 行、无重复、无插值。按制冷电功率排序比较最高与最低各 60 小时；边界没有同值。算术均值的单位为 kW。窗口限于十天，可能同时受加工班表、锅炉控制和储水量影响。

下载路径：Zenodo 记录 6563580 下的 files/00_README_file.txt 和 files/04_hourly_energy_data.txt。原始小时表的 MD5 为 0efd66fb0300e1c2bc9554ad0a831913，说明文件为 2521e433cfec94060c94e286eb171688。可运行 python replay.py 指定输出 CSV 路径，标准输出为可重复计算的 JSON。

只有电表同时存在。最高制冷负荷组的锅炉平均 22.82 kW，最低组为 217.53 kW。不能由制冷电功率得出可回收热量，锅炉电功率也不能代表同期所有热用户的需求。储罐可作为候选；热源温度、流量、供水温级、已有储量及同批产品服务需另行取得。
