# CHANGELOG

## Repository planning - 2026-06-26

- 新增 `开源平台选型与自研边界_V1.md`，明确 Home Assistant、Mosquitto、Zigbee2MQTT、ESPHome、SmartHouse Core 的分工。
- 新增 `实施路线图与仓库结构_V1.md`，把项目拆为设计冻结、装修布线、核心平台、只读集成、受保护写控制和自动化优化阶段。
- 新增 `software/`、`inventory/`、`commissioning/`、`external/` 工作区 README。
- 明确当前不把 Home Assistant、Zigbee2MQTT、ESPHome 等大型上游项目作为 Git submodule；仅在需要锁定外部源码时才使用 `external/`。

## V3.2 - 2026-06-25

- 将日立多联机 Modbus 点表纳入当前暖通基线。
- 新增 4998/4997/4999 连接和发现状态机。
- 新增每台室内机 91 寄存器的地址模型及主要状态/控制点位。
- 标记 B+85、B+87 在点表中的读写属性矛盾，首期禁用写入。
- 新增日立只读 Home Assistant 配置生成器和 4 室内机示例。
- 新增日立现场房间映射表。
- 更新传感器、硬件、交互、软件和 RS-485 架构图。
- 更新施工交底至 V2.1：3090 在 Bedroom1、P2S 在 Balcony1、储物间仅保留网络设备。
- 大金 DTA120A611 调整为等待资料的替代方案。
- 保留格恩中央加湿独立 RS-485 通道。
