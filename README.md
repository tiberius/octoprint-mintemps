# OctoPrint-MinTemps

OctoPrint-MinTemps is a plugin that keeps the bed and hotend heaters at a
minimum temperature after a print finishes and periodically while idle. This
helps avoid firmware protection shutdowns in cold environments where
temperatures can drop below about 5 C.

## MVP behavior

- Provides settings to configure minimum bed and per-tool temperatures.
- Defaults all minimums to 7 C.
- Includes a disable toggle (defaults to enabled).
- After a print is done, cancelled, or failed, the plugin re-applies the
  configured minimum temperatures.
- Periodically re-applies the minimums while the printer is idle.

## Configuration

Open OctoPrint **Settings -> MinTemps** and set the desired minimum
temperatures in C. Tool count and bed availability are derived from the
current OctoPrint printer profile, with defaults of 7 C per tool. You can also
adjust the periodic enforcement interval (seconds); set it to 0 to disable the
periodic timer.

## How it works

The plugin listens for OctoPrint print completion events and, when the printer
is operational and enabled, sets:

- Bed: `bed_temp`
- Tools: `tool_temps` (tool0, tool1, ...)

It also runs periodic enforcement while idle using the configured interval.

## Project outline and feature ideas

Short-term:

- Add an optional delay before re-applying temperatures.
- Add a quick "apply now" button in settings.
- Add bounds and validation for minimum temps.

Long-term:

- Optional UI status indicator.
- REST API endpoints for external automation.
- Notifications when minimums cannot be applied.

## License

See `LICENSE`.
