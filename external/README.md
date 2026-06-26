# External Dependencies And Submodules

This directory is reserved for external source dependencies only when a submodule or pinned source checkout is genuinely needed.

Current policy:

- Do not add Home Assistant, Zigbee2MQTT, ESPHome, Mosquitto, Node-RED, or Frigate as submodules by default.
- Use official installation methods, Home Assistant Apps/Add-ons, containers, package managers, or configuration references instead.
- Add a submodule only when we need source code pinned to a specific commit and package management is not a better fit.

If a submodule is added later, document:

- repository URL;
- locked commit;
- reason for vendoring;
- update command;
- license;
- how it interfaces with this project.
