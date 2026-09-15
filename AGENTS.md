# SmartHouse

This repository covers renovation handoff, network/low-voltage design, Home
Assistant and HVAC/Modbus integration. Preserve the wired backbone, local control,
manufacturer controllers and independent critical safety functions.

## Read for the task

- Current package/version: `README.md`; `PROJECT_TREE.md` for inventory.
- Architecture and construction: relevant documents in `docs/current/`.
  The V3.2 architecture wins over V2.1 construction where those baselines conflict.
- Room/device decisions, protocol evidence or commissioning: the relevant section
  of [design-and-commissioning.md](docs/agent-reference/design-and-commissioning.md).
- Hardware/ports/cables: `inventory/`; diagrams: `diagrams/架构图索引.md` and
  `diagrams/sources/`; read-only HA examples: `config/home-assistant/hitachi/`.

Treat `docs/archive/` as historical. Do not reopen resolved decisions or move
files into archives unless the task calls for it. Verify Git identity rather
than assuming this is still a non-Git package.

## Preserve these boundaries

- Contractor, designer and site-handoff materials use Chinese room names and prose.
  Preserve Chinese filenames and necessary product/protocol terms.
- RS-485 presence does not prove Modbus compatibility. Confirm register map,
  addressing, serial settings, function codes and controller priority before live use.
  Keep Hitachi HVAC and humidifier buses on separate isolated channels unless
  vendor-backed compatibility has been established.
- Hitachi commissioning starts with confirmed wiring/protocol, `4998=1`, unit
  enumeration and room mapping. Writes need task authority and readback. Do not
  auto-write `4999`, expose batch shutdown `4004` as a normal control, or write
  ambiguous `B+85`/`B+87` controls before vendor confirmation.
- Do not cut power to HVAC, humidifiers or gas water heaters through smart plugs.
  Keep critical safety independent of HA/cloud, and admin endpoints off public ingress.
- Keep examples read-only and placeholders explicit. Do not invent final site
  addresses or credentials. Live controls and configuration changes require the
  corresponding task authority.

## Complete the artifact

Update only affected documents/configuration and their relevant cross-references.
For diagrams, edit `.dot` sources then regenerate and inspect the affected output.
For generated packages, check the applicable manifest; a small prose edit does
not require a whole bundle rebuild. Site wiring, protocol reads, writes and
long-term operation are distinct acceptance evidence.

`scripts/copy_to_projects.sh` performs a sync even with `--help`; inspect its source
before use. Preserve user edits, local extras and private runtime configuration.

## Codex collaboration

Astra owns renovation ambiguity, protocol and safety decisions, authority, review and integration. Prefer Luna for useful independent slices when the model and delegation are available; honor explicit model choices and keep small tasks with the owner. Luna may perform a bounded documentation, diagram-source, inventory discovery or content/link check with exact write scope and evidence. Suitable slices include tracing a V3.2 architecture reference, checking a room/device mapping, reviewing read-only Hitachi examples, or updating a `.dot` source and inspecting its affected output. Keep one writer per artifact and preserve Chinese site terminology. Existing project constraints and authorization requirements still apply.
