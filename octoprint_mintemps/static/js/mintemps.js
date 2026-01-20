$(function() {
  function MinTempsViewModel(parameters) {
    var self = this;

    self.settings = parameters[0];
    self.toolSettings = ko.observableArray([]);
    self.hasBed = ko.observable(true);

    self.onSettingsShown = function() {
      var pluginSettings = self._pluginSettings();
      if (!pluginSettings) {
        return;
      }

      if (pluginSettings.has_bed) {
        self.hasBed(!!pluginSettings.has_bed());
      } else {
        self.hasBed(true);
      }

      self._buildToolSettings(pluginSettings);
    };

    self.onSettingsBeforeSave = function() {
      var pluginSettings = self._pluginSettings();
      if (!pluginSettings) {
        return;
      }

      var toolTemps = {};
      self.toolSettings().forEach(function(entry) {
        var value = parseInt(entry.temp(), 10);
        if (isNaN(value)) {
          value = 7;
        }
        toolTemps[entry.key] = value;
      });

      pluginSettings.tool_temps(toolTemps);
    };

    self._pluginSettings = function() {
      if (!self.settings || !self.settings.settings) {
        return null;
      }
      return self.settings.settings.plugins.mintemps;
    };

    self._buildToolSettings = function(pluginSettings) {
      self.toolSettings.removeAll();

      var toolCount = 1;
      if (pluginSettings.tool_count) {
        toolCount = parseInt(pluginSettings.tool_count(), 10);
        if (isNaN(toolCount) || toolCount < 1) {
          toolCount = 1;
        }
      }

      var toolTemps = {};
      if (pluginSettings.tool_temps) {
        toolTemps = pluginSettings.tool_temps() || {};
      }

      for (var index = 0; index < toolCount; index++) {
        var key = "tool" + index;
        var tempValue = toolTemps[key];
        if (tempValue === undefined || tempValue === null || tempValue === "") {
          tempValue = 7;
        }

        self.toolSettings.push({
          key: key,
          label: "Tool " + index + " minimum temperature (C)",
          temp: ko.observable(tempValue)
        });
      }
    };
  }

  OCTOPRINT_VIEWMODELS.push({
    construct: MinTempsViewModel,
    dependencies: ["settingsViewModel"],
    elements: ["#settings_plugin_mintemps"]
  });
});
