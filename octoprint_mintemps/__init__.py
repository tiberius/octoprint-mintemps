from __future__ import absolute_import

import octoprint.plugin
from octoprint.events import Events
from octoprint.util import RepeatedTimer


class MinTempsPlugin(
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.EventHandlerPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.ShutdownPlugin,
):
    def __init__(self):
        self._timer = None

    def get_settings_defaults(self):
        return {
            "disabled": False,
            "bed_temp": 7,
            "tool_temps": {},
            "tool_count": 1,
            "has_bed": True,
            "enforce_interval_sec": 300,
        }

    def get_template_configs(self):
        return [dict(type="settings", custom_bindings=False)]

    def get_assets(self):
        return {"js": ["js/mintemps.js"]}

    def on_after_startup(self):
        self._sync_printer_profile_settings()
        self._restart_timer()

    def on_shutdown(self):
        self._stop_timer()

    def on_settings_save(self, data):
        super().on_settings_save(data)
        self._sync_printer_profile_settings()
        self._restart_timer()

    def on_event(self, event, payload):
        if event in (Events.PRINT_DONE, Events.PRINT_FAILED, Events.PRINT_CANCELLED):
            self._apply_min_temps(reason=event)

    def _apply_min_temps(self, reason):
        if self._settings.get_boolean(["disabled"]):
            return

        if not self._printer or not self._printer.is_operational():
            return

        if reason == "periodic" and (
            self._printer.is_printing() or self._printer.is_paused()
        ):
            return

        log = self._logger.debug if reason == "periodic" else self._logger.info

        bed_temp = self._settings.get_int(["bed_temp"])
        tool_targets = self._get_tool_targets()

        if self._settings.get_boolean(["has_bed"]):
            log("Setting bed minimum temperature to %sC (%s)", bed_temp, reason)
            self._printer.set_temperature("bed", bed_temp)

        for tool_id, temp in tool_targets:
            log("Setting %s minimum temperature to %sC (%s)", tool_id, temp, reason)
            self._printer.set_temperature(tool_id, temp)

    def _get_tool_targets(self):
        tool_count = max(0, self._settings.get_int(["tool_count"]))
        tool_temps = self._settings.get(["tool_temps"]) or {}
        if not isinstance(tool_temps, dict):
            tool_temps = {}

        targets = []
        for index in range(tool_count):
            key = "tool{}".format(index)
            value = tool_temps.get(key, 7)
            try:
                value = int(value)
            except (TypeError, ValueError):
                value = 7
            targets.append((key, value))
        return targets

    def _restart_timer(self):
        self._stop_timer()
        interval = self._settings.get_int(["enforce_interval_sec"])
        if interval <= 0:
            return
        self._timer = RepeatedTimer(interval, self._periodic_enforce)
        self._timer.start()

    def _stop_timer(self):
        if self._timer:
            self._timer.cancel()
            self._timer = None

    def _periodic_enforce(self):
        self._apply_min_temps(reason="periodic")

    def _sync_printer_profile_settings(self):
        profile = self._get_printer_profile()
        has_bed = bool(profile.get("heatedBed", True))
        extruder = profile.get("extruder", {}) or {}
        tool_count = extruder.get("count", 1)
        try:
            tool_count = int(tool_count)
        except (TypeError, ValueError):
            tool_count = 1
        tool_count = max(1, tool_count)

        updated = False
        if self._settings.get_boolean(["has_bed"]) != has_bed:
            self._settings.set(["has_bed"], has_bed)
            updated = True

        if self._settings.get_int(["tool_count"]) != tool_count:
            self._settings.set(["tool_count"], tool_count)
            updated = True

        tool_temps = self._settings.get(["tool_temps"]) or {}
        if not isinstance(tool_temps, dict):
            tool_temps = {}
            updated = True

        for index in range(tool_count):
            key = "tool{}".format(index)
            if key not in tool_temps or tool_temps[key] in (None, ""):
                tool_temps[key] = 7
                updated = True

        if updated:
            self._settings.set(["tool_temps"], tool_temps)
            self._settings.save()

    def _get_printer_profile(self):
        if not self._printer_profile_manager:
            return {}
        try:
            return self._printer_profile_manager.get_current_or_default() or {}
        except Exception:
            self._logger.exception("Unable to read printer profile")
            return {}


__plugin_name__ = "MinTemps"
__plugin_description__ = (
    "Keep bed and hotend heaters at a minimum temperature after prints."
)
__plugin_version__ = "0.2.0"
__plugin_pythoncompat__ = ">=3,<4"


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = MinTempsPlugin()
