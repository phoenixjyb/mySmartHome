# Software Workspace

This directory is reserved for the software side of `mySmartHome`.

Planned areas:

- `smarthouse-core/`: guarded control service for HVAC, humidifier, and house-specific policies.
- `modbus-tools/`: commissioning scripts for read-only scans, register checks, room mapping, and acceptance evidence.

Rules:

- Start with read-only tooling before write controls.
- Keep Home Assistant as the platform layer, not as the project name.
- Put dangerous writes behind SmartHouse Core or explicit protected scripts.
- Do not commit secrets, real LAN tokens, VPN keys, or unreviewed site-generated configs.
