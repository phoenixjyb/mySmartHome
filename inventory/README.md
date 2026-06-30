# Inventory

This directory will hold structured equipment and network inventory.

Planned files:

- `devices.csv`: model, vendor, room, protocol, power, warranty, notes.
- `network_ports.csv`: patch panel port, room, wall plate label, switch port, VLAN.
- `power_socket_points.csv`: fixed-device power loads, socket point requirements, UPS boundaries, and smart-plug restrictions.
- `rs485_cable_runs.csv`: RS-485 candidate runs, topology, estimated construction length, and reserve length.
- `ip_plan.md`: VLANs, static DHCP reservations, hostnames.
- `rs485_channels.md`: gateway port, bus wiring, serial settings, slave IDs, termination.
- `purchase_candidates.md`: hardware candidates and decision status.
- `docs/current/首期硬件型号与购买链接建议_V1.md`: model-level purchase candidates, rough price bands, and JD/Taobao search links.

Do not store passwords, API keys, tokens, or private account recovery data here.

Current files:

- `purchase_candidates.md`: initial hardware candidate list and purchase priority.
- `../docs/current/首期硬件型号与购买链接建议_V1.md`: current model-level recommendations and purchase links.
- `hardware_decision_matrix.md`: tradeoff matrix for controller, network ecosystem, switch, AP, Zigbee, RS-485, and UPS choices.
- `contractor_wiring_checklist.csv`: contractor-facing wiring and installation checklist.
- `network_ports.csv`: construction-stage low-voltage port schedule.
- `power_socket_points.csv`: power/socket point review list for rack, workstations, P2S, AV/projection, curtains, water equipment, HVAC, humidifier, and entry devices.
- `ip_plan.md`: first VLAN/IP/static DHCP plan.
- `rs485_channels.md`: RS-485 channel split and commissioning rules.
- `rs485_cable_runs.csv`: design-stage RS-485 line-length estimate for Hitachi, Gen, and future reserve channels.
- `devices.csv`: initial device inventory skeleton.
