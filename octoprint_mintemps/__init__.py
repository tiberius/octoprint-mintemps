from __future__ import absolute_import

import octoprint.plugin
from octoprint.events import Events


class MinTempsPlugin(
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.EventHandlerPlugin,
):
    def get_settings_defaults(self):
        return {"bed_temp": 7, "tool_temp": 7}

    def get_template_configs(self):
        return [dict(type="settings", custom_bindings=False)]

    def on_event(self, event, payload):
        if event in (Events.PRINT_DONE, Events.PRINT_FAILED, Events.PRINT_CANCELLED):
            self._apply_min_temps()

    def _apply_min_temps(self):
        if not self._printer or not self._printer.is_operational():
            return

        bed_temp = self._settings.get_int(["bed_temp"])
        tool_temp = self._settings.get_int(["tool_temp"])

        self._logger.info("Setting bed minimum temperature to %sC", bed_temp)
        self._printer.set_temperature("bed", bed_temp)

        self._logger.info("Setting tool0 minimum temperature to %sC", tool_temp)
        self._printer.set_temperature("tool0", tool_temp)


__plugin_name__ = "MinTemps"
__plugin_description__ = (
    "Keep bed and hotend heaters at a minimum temperature after prints."
)
__plugin_version__ = "0.1.0"
__plugin_pythoncompat__ = ">=3,<4"


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = MinTempsPlugin()
