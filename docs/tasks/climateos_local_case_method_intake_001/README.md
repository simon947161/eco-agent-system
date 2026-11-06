# CLIMATEOS-LOCAL-CASE-METHOD-INTAKE-001

中文成果：[离线报告](REPORT_ZH.html) · [Markdown报告](REPORT_ZH.md) · [来源台账](evidence/source-ledger.csv) · [最新交接](NEXT_SESSION.md)。

2026-11-06：A WITH_GAPS；B RAW_DATA_AUDIT_PASSED_WITH_LIMITS。有限方法核查完成，不能升级为真实设施排放验证。D3 DATA_NOT_READY；P1-A PENDING。

## 复算

Python3.12，openpyxl3.x；生成报告额外需要matplotlib3.x。

原件放入仓库根目录`runtime_data/local_case_method_intake`。精确文件名、原始公开URL、发布者MD5与本轮SHA-256见`evidence/acquisition.json`。`acquire_selected.py`是本轮一次性获取脚本；已有收据时拒绝重复执行。不要为复算重试已停止入口。优先复用同SHA原件。

```powershell
python docs/tasks/climateos_local_case_method_intake_001/validate_intake.py
python docs/tasks/climateos_local_case_method_intake_001/test_intake.py
python docs/tasks/climateos_local_case_method_intake_001/build_report.py
```

`AUDIT.ipynb`提供同一只读核查入口。未执行上游MATLAB/SeweX，未做真实设施拟合/反演或ACCU/AWT。原始ZIP不入Git、不改写。离线包内的许可允许再分发文件是原件副本，不增加独立样本数。EPA照片PDF、论文正文及专有软件不随包分发。

## 原始数据署名

Jiuling Li (2025), **Sewer CH4**, version1, Zenodo, DOI [10.5281/zenodo.17718964](https://doi.org/10.5281/zenodo.17718964), [CC BY4.0](https://creativecommons.org/licenses/by/4.0/)。原件ZIP未修改。派生转录、统计和图由本任务计算，不能归作作者新增现场测量。作者论文：Sharma等，Nature Water4,196–205(2026)，DOI10.1038/s44221-025-00574-w。
