# smartHouse 项目资料包（V3.2）

本目录整理当前全屋网络、智能家居、传感器、暖通接入和施工交底资料。

## 当前有效文件

- `docs/current/全屋智能系统总体架构_V3.2.md`：当前总体架构主文档。
- `docs/current/日立中央空调_Modbus接入与调试_V1.md`：日立点表分析、寄存器和调试流程。
- `docs/current/日立室内机房间映射表.md`：现场建立 Y/系统号/地址号与房间映射。
- `docs/current/开源平台选型与自研边界_V1.md`：明确采用 Home Assistant 等开源平台和本项目自研边界。
- `docs/current/实施路线图与仓库结构_V1.md`：从设计、施工到软件实现的阶段计划和目录规划。
- `docs/current/架构审计与首期硬件清单_V1.md`：审计当前方案并给出装修前硬件/布线优先级。
- `docs/current/首期硬件型号与购买链接建议_V1.md`：把首期硬件收敛为具体型号、备选和京东/淘宝搜索链接。
- `docs/current/装修队施工交底清单_V1.md`：面向装修队的布线、点位、隐蔽工程和验收交付清单。
- `docs/current/设计师发送前点位复核_V1.md`：发给设计师/施工队前的点位歧义审查和需上图事项。
- `docs/current/用电功率与插座点位复核_V1.md`：设备功率、插座点位、回路边界、UPS 边界和智能控制禁区复核。
- `docs/current/RS485线路拓扑与米数估算_V1.md`：RS-485 在家中网络拓扑、独立管线和当前户型图下的米数估算。
- `docs/current/新平面图初读与智能点位影响_V1.md`：根据新版平面图识别空间功能、旧基线冲突和点位更新前置问题。
- `docs/current/装修施工交底_网络与智能家居_V2.1.md`：施工基础稿；冲突时以 V3.2 为准。
- `diagrams/06_暖通与加湿_RS485架构.svg`：暖通总线架构。
- `diagrams/07_日立空调_Modbus控制流程.svg`：日立发现与控制状态机。
- `diagrams/08_RS485线路拓扑与米数估算.svg`：RS-485 分通道走线和预留米数图。
- `config/home-assistant/hitachi/`：只读调试 YAML 和 secrets 示例。
- `scripts/generate_hitachi_ha_yaml.py`：按室内机数量生成只读 YAML。
- `references/日立中央空调/`：日立 Modbus 点表原件。
- `references/格恩通信协议列表格式-液晶控制器.xlsx`：格恩中央加湿协议原件。
- `references/newFloorPlan.png`：新版平面布置图，作为后续点位重排依据。
- `software/`、`inventory/`、`commissioning/`、`external/`：后续自研软件、设备清单、现场验收和外部依赖管理工作区。
- `inventory/`：首期采购候选、硬件决策矩阵、装修队布线清单、网络端口、功率/插座点位、IP/VLAN、RS-485 通道/线长和设备清单。

## 当前暖通基线

- 日立多联机 Modbus 点表已取得，当前以日立方案搭建发现、房间映射和安全控制骨架。
- 日立转换器的串口参数、从机地址、功能码和地址偏移仍需安装手册或现场验证。
- 大金 DTA120A611 资料尚未到达，保留为替代方案，不阻塞当前项目。
- 格恩中央加湿已确认 RS-485 / Modbus RTU 9600 8N1；与日立使用独立串口通道。

## 已确认的空间基线

- Bedroom1 为办公室，3090 工作站放 Bedroom1，保留 2×Cat6A。
- Bedroom2 可能放台式机，保留 2×Cat6A。
- Bedroom3 不设固定网口。
- 储物间对应新版平面图中的衣帽间，用作网络与自动化设备间。
- 洗衣机固定在次卫生间。
- 客厅投影仪按新版平面图幕布位置协调。
- P2S 确认放入储物间/新图衣帽间；按独立台面/独立插座/不接机柜 UPS 设计，PLA/PETG 不强制外排，但保留通风或外排条件。
- Balcony2 保留 1 个备用网口。
- 采用 16 口可管理 PoE+ 交换机、两台有线 AP、PoE Zigbee 协调器。

> 注意：`references/newFloorPlan.png` 显示了新的书房、衣帽间、洗衣机和客厅影音布局。上述空间基线在正式施工前需要按 `docs/current/新平面图初读与智能点位影响_V1.md` 重新映射。

## 放入本机项目目录

下载并解压后，在资料包根目录执行：

```bash
bash scripts/copy_to_projects.sh
```

脚本同步到：

```text
~/Projects/smartHouse
```

已有目录中的额外文件不会被主动删除。

## 版本约定

- `docs/current/`：当前采用版本。
- `docs/archive/`：历史草案，仅供追溯。
- `config/`：尚需按实际 IP、从机地址和现场映射调整的部署模板。
- `software/`：自研代码和调试工具，当前先以规划和 README 占位。
- `external/`：只在确需固定外部源码时使用；当前不把 Home Assistant、Zigbee2MQTT、ESPHome 等作为 submodule。
- 任何写控制启用前，必须完成只读验证和原厂线控器对照测试。
