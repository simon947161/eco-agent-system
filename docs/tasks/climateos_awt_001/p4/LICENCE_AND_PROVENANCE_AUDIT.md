# P4 许可和来源审计

评估日期：2026-11-24（Australia/Sydney）｜`READ_ONLY`｜`NO_RAW_DATA_DOWNLOADED`

权威：[Issue #164](https://github.com/simon947161/eco-agent-system/issues/164)。这是证据筛查，不是法律意见。所有判断只针对所列公开文档；没有核验原始文件字节或接纳数据。

|候选|许可原文与绑定依据|授权人 / 允许 / 未知|结论|
|---|---|---|---|
|C01|目录 [S02](https://cer.gov.au/markets/reports-and-data/safeguard-data/2024-25-baselines-and-emissions-data)；尝试版权页 [S03](https://cer.gov.au/copyright) 返回工具不可访问，HTTP码未提供|CER是发布者，不据此推定所有第三方权利；再分发、衍生、署名条款、NC限制、保留条件全部UNKNOWN|LICENCE_UNVERIFIED；不下载，不复制表格|
|C02|目录 [S04](https://www.transport.nsw.gov.au/operations/roads-and-waterways/environment-and-heritage/environmental-compliance/environment) 403；[S05](https://www.transport.nsw.gov.au/system/files/media/documents/2025/SPI-Landfill-Gas-Monitoring-March-2025.pdf)仅检索索引，未开PDF|许可授权人、第三方承包者权利、署名/再分发/衍生/NC/保留条件UNKNOWN|LICENCE_UNVERIFIED；公示义务不是开放授权；STOP|
|C03|记录 [S06](https://zenodo.org/records/14165793) [S07](https://zenodo.org/records/14197882) 的Rights标题没有可读许可；[S08](https://zenodo.org/api/records/14197882)不可访问|作者/二手数据来源各自权利未核实；再分发、衍生、署名条件、NC及保留条件UNKNOWN|LICENCE_UNVERIFIED；不能把Zenodo的Open标记当作CC BY|
|C04|Dryad Terms 1(a)、2(a–c) [S10](https://datadryad.org/terms)将其发布数据集置于CC0；[CC0法律原文](https://creativecommons.org/publicdomain/zero/1.0/legalcode.en)；记录 [S09](https://datadryad.org/dataset/doi:10.5061/dryad.ht76hdrtc)|提交者通过Dryad授权。CC0版权层面允许复制、修改、商业及非商业再利用；不强制版权署名，但研究必须保留作者/DOI/版本。第三方隐私、商标、专利和真实性不由CC0保证|CC0_PLATFORM_POLICY_SUPPORTED_NOT_BYTE_VERIFIED；只支持方法候选，未核验文件内例外或完整权属|

## 访问、隐私与保留

没有调用任何数据 API、下载按钮、CSV/XLSX/ZIP/PDF数据文件或数据预览。Zenodo只尝试元数据API一次，工具不可访问后停止；TfNSW403后没有直开PDF、换镜像或重试。CER许可URL不可访问没有当作403或许可拒绝。C04公开网页的本机读取先遇sandbox DNS错误；获工具执行批准后仅同一公开目录HTML返回200，未取得可解析的文件链接。这个本机DNS问题不是远端认证阻挡。全部事件见 [source_register.json](source_register.json)。

没有建立API自动采集、账户或服务条款绕过。C01公开页说明部分商业敏感信息可不予公开；不能反推隐藏值。C02/C03隐私及地理敏感条件UNKNOWN，不能补造。C04明确删除设施身份及坐标；不得利用其他公开资料重新识别匿名场址。CC0未见期限性保留要求，不代表授权任意保存私人信息。当前没有任何原始数据需要保留/销毁。

## 未来取件前检查（未授权执行）

先确认精确记录版本、直接文件URL、许可绑定、预期大小及隐私范围；再由Founder明确批准指定文件和字节上限。届时遇403/429/登录/CAPTCHA或身份敏感内容立即停止。文件内条款与网页不一致时停止，不选更宽松解释。原始字节哈希只能在单独批准实际取得后记录；本轮 null 不得用URL或元数据哈希替代。

全部文件下载可行性维持 NOT_TESTED；C02已在目录层BLOCKED。公开可见与法律可复制、用户授权可获取是三个不同问题。
