# Inventory

This directory will hold structured equipment and network inventory.

Planned files:

- `devices.csv`: model, vendor, room, protocol, power, warranty, notes.
- `network_ports.csv`: patch panel port, room, wall plate label, switch port, VLAN.
- `power_socket_points.csv`: fixed-device power loads, socket point requirements, UPS boundaries, and smart-plug restrictions.
- `ip_plan.md`: VLANs, static DHCP reservations, hostnames.
- `rs485_channels.md`: gateway port, bus wiring, serial settings, slave IDs, termination.
- `purchase_candidates.md`: hardware candidates and decision status.

Do not store passwords, API keys, tokens, or private account recovery data here.

Current files:

- `purchase_candidates.md`: initial hardware candidate list and purchase priority.
- `hardware_decision_matrix.md`: tradeoff matrix for controller, network ecosystem, switch, AP, Zigbee, RS-485, and UPS choices.
- `contractor_wiring_checklist.csv`: contractor-facing wiring and installation checklist.
- `network_ports.csv`: construction-stage low-voltage port schedule.
- `power_socket_points.csv`: power/socket point review list for rack, workstations, P2S, AV/projection, curtains, water equipment, HVAC, humidifier, and entry devices.
- `ip_plan.md`: first VLAN/IP/static DHCP plan.
- `rs485_channels.md`: RS-485 channel split and commissioning rules.
- `devices.csv`: initial device inventory skeleton.
