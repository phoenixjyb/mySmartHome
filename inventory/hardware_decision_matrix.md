# Hardware Decision Matrix

**日期：** 2026-06-26  
**状态：** 初版决策矩阵。下单前按国内价格、渠道、保修、机柜尺寸和供应商资料再复核。

## 1. 当前推荐

| 类别 | 当前推荐 | 备选 | 暂不推荐 |
|---|---|---|---|
| 主控 | Apple Silicon Mac mini，16GB RAM 起步，内置 SSD + 外部备份 | mini PC 作为主控备选；Raspberry Pi 5 + NVMe 作为实验/备份 | microSD Pi 长期主控、Home Assistant Green 作为长期平台 |
| 网络生态 | TP-Link Omada 优先评估 | UniFi；OpenWrt/OPNsense + 独立交换机/AP | 只能云管、不能导出配置的方案 |
| 交换机 | 24 口可管理 PoE+ 优先；16 口为最低 | Omada SG3218XP-M2 类、UniFi Pro Max 16 PoE 类 | 不支持 VLAN/PoE 管理的普通交换机 |
| AP | 2 台吸顶 Wi-Fi 6/7，PoE+，2.5G uplink | 后期实测再决定是否补有线 AP | 无线 Mesh 主回程；本轮不预留 AP-R/AP3 |
| Zigbee | Ethernet/PoE coordinator | USB dongle 仅实验/备用 | 协调器放金属机柜内 |
| RS-485 | 4 路隔离型 RS-485 to Ethernet 网关 | 2 路网关但预留扩展 | 日立和格恩共用一条总线 |
| UPS | 1000-1500VA，网络/主控/网关专用 | 更大容量但仍只带弱电设备 | 给 3090/P2S 供电 |

## 2. 主控主机

| 方案 | 优点 | 风险 | 结论 |
|---|---|---|---|
| Mac mini | 做工和稳定性好，适合 VM 和后续服务；Apple Silicon 满足 ARM 偏好 | 成本高；macOS/VM 运维方式要固定；256GB 版本需外部备份盘或 NAS 备份 | 当前主控基线 |
| mini PC N100/N150/N305 类 | NVMe、低功耗、x86 生态、HAOS/虚拟化友好 | 不满足 ARM 偏好；品牌质量差异大，需要选可靠电源/散热 | 主控备选 |
| Raspberry Pi 5 + NVMe | 低成本、生态广、适合实验 | 长期主控余量、散热、电源和存储要额外处理 | 备份/实验/边缘节点 |
| Jetson Orin Nano | ARM + NVIDIA GPU，适合本地视觉/语音/AI 推理 | JetPack/驱动维护复杂；做 HA 主控浪费且不省心 | 未来 AI 节点 |
| Home Assistant Green | 上手快、官方硬件 | 4GB/32GB 级别更适合轻量 HA | 不作为本项目长期主控 |

决策要求：

- 有线 Ethernet；
- NVMe SSD；
- UPS；
- 可备份、可恢复；
- 未来能跑 SmartHouse Core、Modbus tools、InfluxDB/Grafana 或独立 Linux 服务。

## 3. 网络生态

| 方案 | 优点 | 风险 | 适合度 |
|---|---|---|---|
| TP-Link Omada | 国内采购相对容易，性价比高，交换机/AP/网关生态完整 | UI/高级功能不如部分专业方案；具体型号需核对本地固件 | 高 |
| UniFi | 体验统一，管理界面好，生态完整 | 国内渠道、价格、售后和云账户依赖需确认 | 中高 |
| OpenWrt/OPNsense + 独立交换机/AP | 控制力强，透明度高 | 配置复杂，维护成本高 | 中 |
| 普通家用路由 + 傻瓜交换机 | 成本低 | VLAN、隔离、PoE、运维不可控 | 不适合 |

当前倾向：

```text
先评估 Omada 全套：
路由/控制器 + 24口或16口可管理PoE+交换机 + 2台吸顶AP
```

若更看重统一 UI 和可视化，可再对比 UniFi。

## 4. 交换机

最低条件：

- 可管理；
- VLAN；
- 端口隔离或 ACL；
- PoE+；
- PoE 总功率 100W+；
- 至少 2.5G 上联；
- 配置可导出备份；
- 端口可命名/备注。

推荐：

- 24 口优先评估；
- 16 口仅在机柜空间或预算受限时采用；
- 仍使用 24 口配线架。

候选方向：

| 候选 | 说明 | 状态 |
|---|---|---|
| Omada SG3218XP-M2 类 | 16 个 2.5G 口、PoE、10G SFP+ 方向，适合高性能小型核心 | 候选 |
| Omada 24 口可管理 PoE+ 同级 | 端口余量更好 | 优先继续查 |
| UniFi Pro Max 16 PoE 类 | UniFi 生态，2.5G/PoE/管理体验好 | 候选 |
| UniFi 24 口 PoE 同级 | 端口余量更好 | 继续查 |

## 5. AP

要求：

- 吸顶；
- PoE+；
- 至少 2.5G uplink；
- 支持多个 SSID 映射 VLAN；
- 本地管理；
- 配置可备份。

首期：

- AP1：左侧中央走廊；
- AP2：客厅边吊/空调出风口附近可施工区域，允许偏置；
- AP-R/AP3：本轮取消，不预留空管或备用线。

客厅 AP2 不强求几何正中心。新版方案里客厅只有贴近空调出风口和墙边立柜的局部吊顶/可暗线区域，优先保证暗线出线、顶面明装、开放可维护，并避开金属风管、出风口、灯带驱动和投影幕盒。

候选方向：

| 候选 | 说明 |
|---|---|
| Omada Wi-Fi 7 吸顶 AP | 与 Omada 交换机/网关联动 |
| UniFi U7 Pro 类 | 与 UniFi 生态联动 |
| Wi-Fi 6/6E 企业级 AP | 如果价格合适也可接受 |

## 6. Zigbee coordinator

要求：

- Ethernet/PoE；
- Zigbee2MQTT 支持；
- 固定 IP；
- 放中央走廊；
- 不放金属机柜；
- 与 AP 保持距离；
- 首期只跑 Zigbee，Thread 后评估。

候选：

| 候选 | 说明 | 状态 |
|---|---|---|
| SMLIGHT SLZB-06 系列 | PoE/Ethernet/USB/Wi-Fi 方向，Zigbee2MQTT 常见选择 | 候选 |
| ZigStar UZG-01 | PoE/Ethernet coordinator 方向 | 候选 |
| TubesZB 同类 | PoE coordinator 方向 | 备选 |
| Home Assistant Connect ZBT-2 | 官方 USB dongle | 不符合中央走廊 PoE 优先，但可实验 |

## 7. RS-485 网关

要求：

- 4 路相互隔离；
- 每路独立串口参数；
- Ethernet；
- transparent RTU over TCP；
- 支持 Modbus RTU to TCP 更好；
- 配置可导出；
- DIN 导轨或壁挂；
- A/B/GND、屏蔽、终端电阻说明清楚。

候选：

| 候选方向 | 优点 | 风险 |
|---|---|---|
| Moxa NPort / MGate | 工业可靠性、资料完整 | 成本高 |
| ZLAN 4 路隔离网关 | 国内可买、性价比 | 需核对软件、文档和长期稳定性 |
| USR/Waveshare 工业网关 | 采购方便 | 型号较多，必须确认隔离、4 路独立和配置导出 |

## 8. 下单前统一检查

每个候选设备必须记录：

- 型号；
- 官方链接；
- 国内购买链接；
- 价格；
- 尺寸；
- 供电方式；
- 功耗；
- 是否支持本地管理；
- 是否支持配置导出；
- 是否支持 VLAN/PoE/固定 IP；
- 是否可被 Home Assistant / Zigbee2MQTT / ESPHome / Modbus 使用；
- 保修和退换；
- 是否有完整手册；
- 是否需要额外控制器或订阅。

## 9. 当前未决

1. 是否直接选 Omada 生态；
2. 交换机 24 口还是 16 口；
3. AP 是否直接 Wi-Fi 7；
4. RS-485 网关在 Moxa 与国产工业网关之间如何取舍；
5. 门口摄像头/门铃本轮暂不预留；未来如变更再单独评估；
6. 窗帘采用 Zigbee 还是 RS-485；
7. 是否安装电动总水阀。

## 10. 参考来源

- Home Assistant installation: https://www.home-assistant.io/installation/
- Home Assistant Raspberry Pi installation: https://www.home-assistant.io/installation/raspberrypi/
- Zigbee2MQTT supported adapters: https://www.zigbee2mqtt.io/guide/adapters/
- SMLIGHT SLZB-06: https://smlight.tech/product/slzb-06/
- Omada SG3218XP-M2: https://www.omadanetworks.com/us/business-networking/omada-switch-access-pro/sg3218xp-m2/
- UniFi U7 Pro: https://techspecs.ui.com/unifi/wifi/u7-pro
- UniFi Pro Max 16 PoE: https://techspecs.ui.com/unifi/switching/usw-pro-max-16-poe
- Moxa Modbus TCP gateways: https://www.moxa.com/en/products/industrial-edge-connectivity/protocol-gateways/modbus-tcp-gateways
- ZLAN5443D: https://www.zlan-iot.com/products_ZLAN5443D.htm
- ZLAN5443A: https://www.zlmcu.com/en/products_ZLAN5443A.htm
