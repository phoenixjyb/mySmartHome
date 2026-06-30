# CHANGELOG

## First-stage hardware model recommendations - 2026-06-30

- 新增 `docs/current/首期硬件型号与购买链接建议_V1.md`，把 UPS、机柜、PDU、交换机、AP、主控、Zigbee 协调器、RS-485 网关、传感器和执行器整理成型号级候选表。
- 每项候选增加京东/淘宝搜索链接、粗略价格区间、推荐/备选关系和下单前确认事项。
- 将 RS-485 网关候选修正为 4 路方向：`ZLAN5443D`/`ZLAN5443A`、Waveshare 4-CH、Moxa NPort 5430I；避免把单路 `ZLAN5143D` 当成 4 路网关。

## P2S storage-room placement confirmed - 2026-06-28

- 记录业主确认：Bambu P2S 放入 storage room/新版平面图衣帽间。
- 将此前“不建议默认放衣帽间”的表述修正为：可放衣帽间，但需独立台面/独立插座、不接机柜 UPS/PDU、与网络机柜和衣物分区，并保留通风或外排条件。
- 更新施工交底、用电点位和 inventory：P2S 点位从阳台候选调整为衣帽间已确认点位；PLA/PETG 不强制外排，ABS/ASA/PC 或气味/热量控制场景建议预留外排。

## New floor plan confirmations - 2026-06-28

- 记录业主确认：`Storage room` 对应新版平面图中的衣帽间，洗衣机固定在次卫生间，客厅投影按新版平面图幕布位置协调。
- 更新新平面图审计、施工交底和用电复核：把次卫洗衣、衣帽间机柜、幕布/投影同图复核纳入当前基线。
- 记录 P2S 放入 storage room/衣帽间的早期风险判断；后续已根据业主实际使用经验修正为已确认点位和条件化施工要求。

## New floor plan initial audit - 2026-06-28

- 新增 `references/newFloorPlan.png`，纳入新版平面布置图作为后续点位重排依据。
- 新增 `docs/current/新平面图初读与智能点位影响_V1.md`，按新图识别书房、衣帽间、洗衣机、客厅影音、P2S 候选和网络设备区等关键变化。
- 标记旧 `Bedroom1/Balcony1/Balcony2/Storage room` 基线需要按新图重新映射，暂不直接覆盖现有 `inventory/` 清单。

## RS-485 topology and cable-length estimate - 2026-06-28

- 新增 `docs/current/RS485线路拓扑与米数估算_V1.md`，明确 RS-485 在家中网络拓扑、日立/格恩独立通道、施工管路和当前户型图下的米数估算。
- 新增 `inventory/rs485_cable_runs.csv`，将 Port 1/2/3/4 的候选路径、估算长度和建议预留长度结构化。
- 新增 `diagrams/08_RS485线路拓扑与米数估算.svg/png` 和 DOT 源文件，用于设计师/施工队快速理解 RS-485 分线和预留米数。
- 更新 `inventory/rs485_channels.md` 和施工交底，强调米数为设计阶段估算，最终以厂家设备位置和正式施工图路径复核为准。

## Power and socket point audit - 2026-06-28

- 新增 `docs/current/用电功率与插座点位复核_V1.md`，把设备功率、插座点位、回路边界、UPS 边界和智能控制禁区纳入设计定稿复核。
- 新增 `inventory/power_socket_points.csv`，记录机柜、3090 工作站、P2S、排风、AV/投影、窗帘、智能开关、水路、暖通和入户设备的供电复核项。
- 更新设计师发送前复核和装修队施工交底，要求强电插座与弱电点位同图复核，并明确 Home Assistant/智能插座不得作为关键设备唯一断电控制。

## Designer pre-send position audit - 2026-06-28

- 新增 `docs/current/设计师发送前点位复核_V1.md`，列出发给设计师前必须落图和仍需业主确认的点位。
- 明确 Zigbee 协调器点位：对外无线连 Zigbee 设备，对内通过 PoE/Ethernet 有线回交换机。
- 将 AP-R 从可选改为至少预留空管和拉线；将客厅影音柜第二根线改为默认预留；将入户低位改为至少空管和拉线。
- 明确日立/格恩 RS-485 在厂家线型未确认前，先做独立弱电管和拉线，确认线型后再穿厂家指定屏蔽线。

## Contractor handoff and hardware decision matrix - 2026-06-26

- 新增 `docs/current/装修队施工交底清单_V1.md`，面向装修队列出储物间、网络点位、RS-485、灯光窗帘、Balcony1、入户门和封墙前检查。
- 新增 `inventory/contractor_wiring_checklist.csv`，把施工点位转为可筛选的 CSV 清单。
- 新增 `inventory/hardware_decision_matrix.md`，记录主控、网络生态、交换机、AP、Zigbee、RS-485 和 UPS 的候选与决策边界。

## Architecture audit and initial inventory - 2026-06-26

- 新增 `docs/current/架构审计与首期硬件清单_V1.md`，审计控制主机、交换机端口、AP、Zigbee、RS-485 和装修队交付边界。
- 新增 `inventory/purchase_candidates.md`，形成首期 P0/P1/P2 采购候选清单。
- 新增 `inventory/network_ports.csv`、`inventory/ip_plan.md`、`inventory/rs485_channels.md`、`inventory/devices.csv`。
- 将首期建议调整为：mini PC/Mac mini 优先、24 口交换机优先评估、PoE/Ethernet Zigbee 协调器、4 路隔离 RS-485 网关。

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
