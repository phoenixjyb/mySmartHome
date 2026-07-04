# 项目目录说明

```text
smartHouse/
├── README.md
├── CHANGELOG.md
├── docs/current/
│   ├── 全屋智能系统总体架构_V3.2.md
│   ├── 日立中央空调_Modbus接入与调试_V1.md
│   ├── 日立室内机房间映射表.md
│   ├── 开源平台选型与自研边界_V1.md
│   ├── 实施路线图与仓库结构_V1.md
│   ├── 架构审计与首期硬件清单_V1.md
│   ├── 首期硬件型号与购买链接建议_V1.md
│   ├── 传感器分类与取舍决策_V1.md
│   ├── 明日设计师沟通要点_2026-07-05.md
│   ├── 设计师点位参考方案_V1.md
│   ├── 给设计师的点位落图输入_V1.md
│   ├── 周末设计师点位图制作基准与优先级_V1.md
│   ├── 装修队施工交底清单_V1.md
│   ├── 设计师发送前点位复核_V1.md
│   ├── 用电功率与插座点位复核_V1.md
│   ├── RS485线路拓扑与米数估算_V1.md
│   ├── 新平面图初读与智能点位影响_V1.md
│   └── 装修施工交底_网络与智能家居_V2.1.md
├── config/home-assistant/hitachi/
│   ├── README.md
│   ├── hitachi_modbus_readonly.yaml.example
│   └── secrets.yaml.example
├── diagrams/
│   ├── 01…08 PNG/SVG
│   └── sources/*.dot
├── software/
│   ├── smarthouse-core/README.md
│   └── modbus-tools/README.md
├── inventory/
│   ├── README.md
│   ├── purchase_candidates.md
│   ├── hardware_decision_matrix.md
│   ├── contractor_wiring_checklist.csv
│   ├── power_socket_points.csv
│   ├── network_ports.csv
│   ├── ip_plan.md
│   ├── rs485_channels.md
│   ├── rs485_cable_runs.csv
│   └── devices.csv
├── commissioning/README.md
├── external/README.md
├── references/
│   ├── newFloorPlan.png
│   ├── 日立中央空调/*.pdf
│   └── 格恩通信协议列表格式-液晶控制器.xlsx
└── scripts/
    ├── copy_to_projects.sh
    └── generate_hitachi_ha_yaml.py
```
