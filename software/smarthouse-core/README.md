# SmartHouse Core

Planned self-built service layer for house-specific logic.

Initial responsibilities:

- Guarded Hitachi HVAC writes.
- Guarded Gree/Gen humidifier writes.
- Write queue, rate limits, precondition checks, and write-after-readback.
- Audit log for all control actions.
- MQTT/REST/WebSocket interface for Home Assistant.
- Policy logic that is too specific or risky for generic Home Assistant automations.

Non-goals:

- Replacing Home Assistant's device registry or dashboards.
- Replacing original HVAC/humidifier controllers.
- Implementing safety-critical protection that should remain in certified devices.

Implementation language is not fixed yet. Python is the likely first prototype because commissioning scripts and Modbus tooling will be faster to build and inspect.
