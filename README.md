# OctoPrint-MinTemps

OctoPrint-MinTemps is a plugin that keeps the bed and hotend heaters at a
minimum temperature after a print finishes. This helps avoid firmware
protection shutdowns in cold environments where temperatures can drop below
about 5 C.

## MVP behavior

- Provides settings to configure minimum bed and hotend temperatures.
- Defaults both minimums to 7 C.
- After a print is done, cancelled, or failed, the plugin re-applies the
  configured minimum temperatures to the bed and tool0.

## Configuration

Open OctoPrint **Settings -> MinTemps** and set the desired minimum
temperatures in C.

## How it works

The plugin listens for OctoPrint print completion events and, when the printer
is operational, sets:

- Bed: `bed_temp`
- Tool: `tool_temp` (tool0)

## Project outline and feature ideas

Short-term:

- Add an enable/disable toggle.
- Add an optional delay before re-applying temperatures.
- Allow separate minimums per tool (tool0, tool1, ...).

Long-term:

- Periodic enforcement while idle (with safe timeout).
- Optional UI status indicator and manual "apply now" button.
- REST API endpoints for external automation.
- Safety bounds and notifications if target min exceeds a max.

## License

See `LICENSE`.
