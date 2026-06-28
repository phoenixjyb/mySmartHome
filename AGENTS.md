# AGENTS.md

Guidance for Codex or other coding/design agents working in this project.

## Project Scope

This is a smart-home and renovation planning package for an approximately 100 m2 apartment with three bedrooms, one living room, one kitchen, two bathrooms, and two balconies.

The project is not only software. It combines renovation construction handoff, network and low-voltage wiring, Home Assistant architecture, Zigbee sensor planning, HVAC/humidifier Modbus integration, diagrams, reference PDFs/images, and vendor protocol evidence.

The current phase is planning and design. Once the design is stable, this repository is expected to grow into the implementation home for a self-built smart-home system: Home Assistant configuration, local adapters, Modbus tooling, dashboards, automations, tests, deployment notes, and operating runbooks.

The current design direction is:

- Wired backbone, wireless endpoints.
- Local-first control where practical.
- Original manufacturer controllers remain available.
- Critical safety functions must not depend on Home Assistant, cloud services, or one vendor platform.
- The owner manages the system directly.

## Source Of Truth

Use these files first:

- `README.md` for the current package summary and version conventions.
- `PROJECT_TREE.md` for package inventory.
- `CHANGELOG.md` for what changed in the V3.2 bundle.
- `docs/current/全屋智能系统总体架构_V3.2.md` as the main architecture baseline.
- `docs/current/装修施工交底_网络与智能家居_V2.1.md` as the construction handoff baseline. If it conflicts with V3.2 architecture, V3.2 wins.
- `docs/current/日立中央空调_Modbus接入与调试_V1.md` for Hitachi Modbus commissioning.
- `docs/current/日立室内机房间映射表.md` for site mapping during HVAC commissioning.
- `docs/current/开源平台选型与自研边界_V1.md` for open-source platform adoption versus self-built boundaries.
- `docs/current/实施路线图与仓库结构_V1.md` for phases, repo structure, and submodule policy.
- `docs/current/架构审计与首期硬件清单_V1.md` for current architecture audit and initial hardware choices.
- `docs/current/装修队施工交底清单_V1.md` for contractor-facing wiring, conduit, photo, and acceptance requirements.
- `docs/current/设计师发送前点位复核_V1.md` for pre-send ambiguity checks and points that must be drawn into designer/contractor plans.
- `docs/current/用电功率与插座点位复核_V1.md` for power-load, socket-position, UPS-boundary, and smart-plug control-boundary checks.
- `docs/current/RS485线路拓扑与米数估算_V1.md` for RS-485 topology, separate conduit routing, and cable-length estimates.
- `inventory/` for initial hardware purchase candidates, network ports, VLAN/IP plan, RS-485 channels, and device inventory.
- `config/home-assistant/hitachi/` for read-only Home Assistant examples.
- `diagrams/架构图索引.md` and `diagrams/sources/*.dot` for diagram maintenance.

Treat `docs/archive/` as historical only. Do not revive archived decisions unless the user explicitly asks to compare or restore an older plan.

## Current Baseline

- `Bedroom1` is the office and RTX 3090 workstation room; keep two Cat6A drops.
- `Bedroom2` may contain another desktop; keep two Cat6A drops.
- `Bedroom3` has no fixed network port; use Wi-Fi/Zigbee sensors.
- `Balcony1` is the Bambu P2S printing area; use Wi-Fi for the printer, keep one spare Cat6A, preserve the living-room balcony door, and plan short local exhaust plus independent safety monitoring.
- `Balcony2` keeps one spare network port and gets leak sensing if a washing machine or water device is installed.
- `Storage room` is only for network and automation equipment: rack/cabinet, ONT, router/firewall, managed PoE switch, patch panel, Mac mini, UPS, Zigbee coordinator network path, and RS-485 gateways. Do not move the 3090 workstation or P2S back into this room.
- Use two wired ceiling APs initially. A third AP is only a conduit/reserve option.
- Use a 16-port managed PoE+ switch with a 24-port passive patch panel for expansion.
- Use a PoE/Ethernet Zigbee coordinator in an open central hallway location, not inside a metal rack.

## Network And Platform Architecture

Expected stack:

- Independent router/firewall.
- 16-port managed PoE+ switch, ideally with some 2.5GbE and optional 10G/SFP+.
- Mac mini running Home Assistant OS VM for the first stage.
- Home Assistant, Mosquitto MQTT, Zigbee2MQTT, ESPHome, and optional Node-RED.
- WireGuard for remote access.
- VLAN/SSID split: Trusted, Automation, IoT, Security, Guest, Management.

Do not propose exposing Home Assistant, cameras, or router admin directly to the public internet.

## Modbus And HVAC Rules

Do not treat "has RS-485" as proof of integration. Require protocol-level evidence:

- Is it actually Modbus RTU/TCP or a proprietary protocol?
- Full register table.
- Baud rate, data bits, parity, stop bits.
- Slave address and whether it is configurable.
- Function codes for reads and writes.
- Whether addresses are 0-based or 1-based in the actual tool/gateway.
- Read-only versus writable registers.
- Interaction priority with original wall controller/app.
- Warranty and support impact of third-party integration.

Keep different RS-485 systems on separate isolated channels by default. The current split is:

- Port 1: Hitachi Modbus/MiniModbus converter. Point table exists, but converter model, serial settings, slave address, function codes, and address offset still require manual/vendor/site confirmation.
- Port 2: 格恩/Gen central humidifier. Current workbook indicates RS-485 / Modbus RTU, 9600 8N1, FC03 reads, with writable controls that still need write function code and reset behavior confirmation.
- Port 3: future meter/water meter reserve.
- Port 4: future Daikin alternative or other equipment reserve.

Never mix Hitachi HVAC and the humidifier on one RS-485 bus unless the user later has explicit vendor-backed compatibility evidence.

## Hitachi Commissioning Boundary

The Hitachi point table is enough to build read-only discovery, room mapping, status monitoring, and a basic control skeleton. It is not enough to hardcode final live writes.

Required sequence:

1. Confirm converter model, physical wiring, serial settings, slave address, protocol mode, function codes, and address offset.
2. Read `4998`; only `4998=1` means controllable.
3. Read `4997`; expected indoor unit count is 1 to 160.
4. Read each unit's `Y`, system number, address number, model code, and state registers.
5. Map rooms by operating one original wall controller at a time and watching which `Y` changes.
6. Only after mapping, test one simple write at a time.
7. Always do write-after-readback checks.
8. Only then consider HA `climate` entities or a dedicated adapter service.

Protected actions:

- Do not auto-write `4999`; it clears cached unit info and can trigger a long rediscovery.
- Do not expose `4004` batch shutdown as a normal dashboard button.
- Do not write `B+85` half-degree control or `B+87` floor-heating control until Hitachi confirms the point-table ambiguity.
- Do not use smart plugs to cut power to central HVAC, humidifiers, or gas water heaters.

## Home Assistant Config Work

The existing Hitachi HA config is intentionally read-only.

Useful command:

```bash
python3 scripts/generate_hitachi_ha_yaml.py --units 4 --type rtuovertcp --output config/home-assistant/hitachi/hitachi_modbus_readonly.yaml
```

Only generate a real output file when the user asks or when there is confirmed site data. Otherwise inspect by writing to stdout.

The example secrets file is a placeholder. Do not invent final IPs, ports, or slave IDs.

## Script And Package Notes

- `scripts/copy_to_projects.sh` syncs this package to `$HOME/Projects/smartHouse`.
- The script does not implement `--help`; any argument still runs the sync.
- The project root is not currently a git worktree.
- `MANIFEST_SHA256.txt` covers the package contents and should be checked after bundle updates with:

```bash
shasum -a 256 -c MANIFEST_SHA256.txt
```

- There is a manifest-tracked Hitachi PDF under `references/日立中央空调/`. A same-topic PDF may also exist directly under `references/`; do not delete local extras without explicit user approval.

## Editing Conventions

- Preserve Chinese filenames and Chinese document titles.
- Keep `docs/current/` authoritative and versioned; move superseded drafts to `docs/archive/` only when the user asks for a package refresh.
- Keep construction-facing documents practical: contractor checklists, exact room names, wire counts, conduit requirements, and site-confirmation items matter more than abstract smart-home theory.
- When adding or changing diagrams, edit `diagrams/sources/*.dot` first and regenerate SVG/PNG outputs consistently.
- When adding Home Assistant examples, default to read-only and clearly label any placeholders.
- Do not add live write controls, destructive maintenance actions, or public remote-access patterns without explicit confirmation.
- Do not add external projects as submodules by default. Use `external/README.md` and `docs/current/开源平台选型与自研边界_V1.md` before deciding a submodule is warranted.

## Git And Repository Conventions

- Version the design documents, diagrams, scripts, Home Assistant examples, and reference evidence that supports decisions.
- Do not commit private HA `secrets.yaml`, real device credentials, LAN-only tokens, VPN keys, exported backups, or site-specific generated configs unless the user explicitly asks after review.
- Use commits as design baselines: prefer small commits that say what decision or implementation stage changed.
- Before major refactors or generated bundle refreshes, check `git status --short` and preserve user edits.
- For future code, keep hardware-touching control paths conservative by default: read-only first, guarded writes second, automation policies last.

## Open Decisions To Track

- Final Hitachi converter model, installation manual, serial parameters, slave address, function codes, and address offset.
- Final indoor/outdoor unit models, model-code table, alarm-code table, room mapping, and half-degree write behavior.
- Whether Daikin DTA120A611 becomes only a comparison option or replaces the Hitachi baseline.
- Humidifier complete model, write function code support, address base, A/B/GND wiring, terminal resistor requirements, and drain-command reset behavior.
- Curtain protocol choice: Zigbee/Thread versus RS-485/Modbus.
- Lighting circuit split, neutral wire and deep box availability, dimming needs, and multi-way control locations.
- Final positions for desks, projector, screen, AV cabinet, door video device, washing machine, water treatment equipment, and water shutoff valve.
- Balcony1 P2S exhaust path, property-management approval, outlet/smoke/VOC monitoring, and heat/noise validation.
- Final as-built line numbering, photos before sealing walls/ceilings, and acceptance records.

## Operating Principle

For future work, separate these states clearly:

- Design assumption.
- Vendor-confirmed protocol fact.
- Construction baseline.
- Site-verified wiring.
- Read-only Home Assistant validation.
- Write-control validation.
- Long-term automation policy.

Do not collapse them into one "done" status.
