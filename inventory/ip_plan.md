# IP / VLAN Plan

**状态：** 初版规划。实际网段可在路由器方案确定后调整。

## VLANs

| VLAN | Name | Suggested subnet | Devices |
|---:|---|---|---|
| 10 | Trusted | `192.168.10.0/24` | 手机、电脑、RTX 3090、Bedroom2 台式机、未来 NAS |
| 20 | Automation | `192.168.20.0/24` | Home Assistant、MQTT、Zigbee coordinator、RS-485 gateway、ESPHome |
| 30 | IoT | `192.168.30.0/24` | 投影、电视、P2S、扫地机、冰箱、洗衣机 |
| 40 | Security | `192.168.40.0/24` | 门口摄像头/门铃、未来 NVR |
| 50 | Guest | `192.168.50.0/24` | 访客设备 |
| 99 | Management | `192.168.99.0/24` | 路由器、交换机、AP 管理 |

## Static DHCP reservations

| Hostname | VLAN | Suggested IP | Device | Status |
|---|---:|---|---|---|
| `ha-core` | 20 | `192.168.20.10` | Home Assistant / mini PC / Mac mini | planned |
| `mqtt` | 20 | `192.168.20.11` | Mosquitto if split from HA | future |
| `zigbee-coord-01` | 20 | `192.168.20.20` | PoE Zigbee coordinator | planned |
| `rs485-gw-01` | 20 | `192.168.20.30` | 4-port RS-485 gateway | planned |
| `ap-01` | 99 | `192.168.99.11` | AP1 | planned |
| `ap-02` | 99 | `192.168.99.12` | AP2 | planned |
| `switch-core-01` | 99 | `192.168.99.2` | Core managed switch | planned |
| `router-01` | 99 | `192.168.99.1` | Router/firewall | planned |

## Firewall baseline

- IoT cannot initiate access to Trusted.
- Trusted can access Home Assistant and required IoT devices.
- Automation can access DNS, NTP, updates, and required local device ports.
- Security can access NVR/recording services, DNS, NTP, and management endpoints only as needed.
- Management only reachable from trusted admin devices.
- Remote access through WireGuard/VPN; no public Home Assistant/router/camera exposure.
