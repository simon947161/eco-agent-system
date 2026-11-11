# Issue151 V2：本机定位阶段与公开基线

状态：LOCAL_WINDOWS / LEGACY_METHOD_NOT_FOUND_IN_INSPECTED_SCOPE / COMPARISON_PARTIAL。

主机目录已确认可访问，完成分阶段只读定位。但尚未找到具有身份和代码依据的目标v200“跳跃方法”。没有把其他旧版本或同名非算法目录当作目标，也没有运行私人旧代码。

Founder于2026-11-11明确决定：保持原范围，记录NOT_FOUND。本轮定位到此结束，不访问备用位置，不再等待范围调整或自动扩查。此次定位不足不证明旧算法不存在或不正确，不能用于方法优劣排名。

已完成的独立工作：固定PR152 HEAD `cf91e4a061341bc33d16400bcf4c6a2c2817aa65`，复核65项原测试；预先固定8组公开合成控制，每组三策略、原样重复，48次公开模拟。**这些是新版控制基线，不是8组已完成的旧版/新版对照。**

入口：[公开中文报告](PUBLIC_FOUNDER_REPORT_ZH.md)、[控制协议](PUBLIC_CASE_PROTOCOL.json)、[公共结果](evidence/public_controls.json)、[测试与隐私边界](QA_AND_PRIVACY.md)、[下一步](NEXT_SESSION.md)、[执行状态](EXECUTION_STATUS.json)。完整私人阶段报告和详细定位记录仅留在本机，不提供公开路径或文件清单。

正式科学准入PENDING；旧成果不改；不合并、不部署、不移植旧算法。
