# Modbus Tools

Planned commissioning and verification scripts.

Targets:

- Hitachi Modbus/MiniModbus converter.
- Gree/Gen central humidifier controller.
- Future electric/water meter devices if they expose open Modbus.

First tools to build:

- Read `4998` and `4997`.
- Scan Hitachi indoor unit `Y / system / address / model` fields.
- Export room mapping templates.
- Verify address base (`raw address` versus `address - 1`).
- Read Gree/Gen humidity, water level, status word, and fault word.
- Generate CSV/JSON records for `commissioning/`.

Writes are out of scope until read-only validation and original-controller cross-checks are complete.
