# RS-485 Channel Plan

**状态：** 初版规划。施工前需由暖通/加湿供应商确认线型、屏蔽、接地和终端电阻。

## Gateway requirement

首期采购 4 路相互隔离的 RS-485 to Ethernet 网关。

Required features:

- 4 independent RS-485 channels.
- Per-channel baud rate, parity, stop bit, timeout.
- Transparent RTU over TCP.
- Modbus RTU to Modbus TCP support preferred.
- Fixed IP / static DHCP.
- Config export.
- DIN rail or wall-mount install.
- Clear A/B/GND, shielding, and termination documentation.

## Channels

| Port | System | Protocol state | Serial settings | Slave ID | Wiring | HA mode | Status |
|---|---|---|---|---|---|---|---|
| 1 | Hitachi VRF Modbus/MiniModbus converter | Point table obtained; install manual needed | TBD | TBD | Dedicated shielded RS-485 from converter to storage room | read-only first | planned |
| 2 | 格恩/Gen central humidifier | Modbus RTU known from workbook | 9600 8N1 known; write details TBD | likely 1; confirm | Dedicated shielded RS-485 from controller to storage room | read-only first | planned |
| 3 | Future meter/water meter | TBD | TBD | TBD | reserve conduit/channel | none | reserve |
| 4 | Future Daikin/other equipment | TBD | TBD | TBD | reserve conduit/channel | none | reserve |

## Cable-length planning

See `docs/current/RS485线路拓扑与米数估算_V1.md` and `inventory/rs485_cable_runs.csv`.

Current reserve guidance:

- Port 1 Hitachi near storage room: reserve 5 m if vendor allows converter near the rack.
- Port 1 Hitachi central ceiling/service hatch: reserve 12 m as baseline.
- Port 1 Hitachi far-right equipment zone: reserve 18 m as contingency.
- Port 2 Gen central humidifier near storage/kitchen/bathroom service zone: reserve 12 m as baseline.
- Port 2 Gen far-right equipment zone: reserve 18 m as contingency.
- Port 3 future water/meter reserve: reserve 12 m conduit/pull string.
- Port 4 future equipment reserve: reserve 18-20 m conduit/pull string.

These are design-stage estimates from the current floor plan. Final lengths must be checked from formal construction drawings and as-built routing before wall/ceiling closure.

## Rules

- Do not share Hitachi and humidifier on one bus.
- Do not assume `RS-485` means `Modbus`.
- Do not enable writes until read-only validation and original-controller cross-checks pass.
- Record every discovered serial setting and register behavior under `commissioning/`.
