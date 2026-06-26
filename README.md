# smartHouse 项目资料包（V3.2）

本目录整理当前全屋网络、智能家居、传感器、暖通接入和施工交底资料。

## 当前有效文件

- `docs/current/全屋智能系统总体架构_V3.2.md`：当前总体架构主文档。
- `docs/current/日立中央空调_Modbus接入与调试_V1.md`：日立点表分析、寄存器和调试流程。
- `docs/current/日立室内机房间映射表.md`：现场建立 Y/系统号/地址号与房间映射。
- `docs/current/开源平台选型与自研边界_V1.md`：明确采用 Home Assistant 等开源平台和本项目自研边界。
- `docs/current/实施路线图与仓库结构_V1.md`：从设计、施工到软件实现的阶段计划和目录规划。
- `docs/current/架构审计与首期硬件清单_V1.md`：审计当前方案并给出装修前硬件/布线优先级。
- `docs/current/装修施工交底_网络与智能家居_V2.1.md`：施工基础稿；冲突时以 V3.2 为准。
- `diagrams/06_暖通与加湿_RS485架构.svg`：暖通总线架构。
- `diagrams/07_日立空调_Modbus控制流程.svg`：日立发现与控制状态机。
- `config/home-assistant/hitachi/`：只读调试 YAML 和 secrets 示例。
- `scripts/generate_hitachi_ha_yaml.py`：按室内机数量生成只读 YAML。
- `references/日立中央空调/`：日立 Modbus 点表原件。
- `references/格恩通信协议列表格式-液晶控制器.xlsx`：格恩中央加湿协议原件。
- `software/`、`inventory/`、`commissioning/`、`external/`：后续自研软件、设备清单、现场验收和外部依赖管理工作区。
- `inventory/`：首期采购候选、网络端口、IP/VLAN、RS-485 通道和设备清单。

## 当前暖通基线

- 日立多联机 Modbus 点表已取得，当前以日立方案搭建发现、房间映射和安全控制骨架。
- 日立转换器的串口参数、从机地址、功能码和地址偏移仍需安装手册或现场验证。
- 大金 DTA120A611 资料尚未到达，保留为替代方案，不阻塞当前项目。
- 格恩中央加湿已确认 RS-485 / Modbus RTU 9600 8N1；与日立使用独立串口通道。

## 已确认的空间基线

- Bedroom1 为办公室，3090 工作站放 Bedroom1，保留 2×Cat6A。
- Bedroom2 可能放台式机，保留 2×Cat6A。
- Bedroom3 不设固定网口。
- Balcony1 放 P2S，使用 Wi-Fi，保留 1 个备用网口及简化外排。
- Balcony2 保留 1 个备用网口。
- 储物间为网络与自动化设备间。
- 采用 16 口可管理 PoE+ 交换机、两台有线 AP、PoE Zigbee 协调器。

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
