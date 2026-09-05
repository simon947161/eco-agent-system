# CRP Harvest — GGG v0.3

- **核心知识点：** OpenAPI 与 MCP 可以通过同一 canonical validator 保持语义一致。
- **想法点：** 先用本机回环验证真实传输边界，再考虑身份、签名和生产注册表。
- **愿望点：** ClimateOS、BuildingOS、ECOChain 等系统能够传递证据而不漂白权威。
- **推理点：** 接口打通不等于生产可信；负向门控与幂等冲突更能证明治理有效。
- **关键决策：** 仅监听 `127.0.0.1`；仅接受 `SYNTHETIC`；继续复用 v0.2 合同。
- **未解决问题：** 身份认证、数字签名、DID/VC、可靠重试、生产注册表。
- **下一步行动：** Founder Review；未授权前不启动 v0.4。
- **项目关联关键词：** `GGG` `ClimateOS` `MCP` `OpenAPI` `Loopback Adapter` `Trust Runtime` `Evidence Governance`。
