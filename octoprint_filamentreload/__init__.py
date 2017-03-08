# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
from octoprint.events import eventManager, Events
from flask import jsonify, make_response
import RPi.GPIO as GPIO
import time
import datetime

global time2
time2 = time.time()+200

class FilamentReloadedPlugin(octoprint.plugin.StartupPlugin,
                             octoprint.plugin.EventHandlerPlugin,
                             octoprint.plugin.TemplatePlugin,
                             octoprint.plugin.SettingsPlugin):

    def initialize(self):
        self._logger.info("Running RPi.GPIO version '{0}'".format(GPIO.VERSION))
        if GPIO.VERSION < "0.6":       # Need at least 0.6 for edge detection
            raise Exception("RPi.GPIO must be greater than 0.6")
        GPIO.setmode(GPIO.BOARD)       # Use the board numbering scheme
        GPIO.setwarnings(False)        # Disable GPIO warnings

    def on_after_startup(self):
        self._logger.info("Filament Sensor Reloaded started")
        self.pin = int(self._settings.get(["pin"]))
        self.bounce = int(self._settings.get(["bounce"]))
        self.switch = int(self._settings.get(["switch"]))

        if self._settings.get(["pin"]) != -1:   # If a pin is defined
            self._logger.info("Filament Sensor active on GPIO Pin [%s]"%self.pin)
            GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Initialize GPIO as INPUT

    def get_settings_defaults(self):
        return dict(
            pin     = 5,   # Default is no pin
            bounce  = 250,  # Debounce 250ms
            switch  = 1    # Normally Open
        )

    def get_template_configs(self):
        return [dict(type="settings", custom_bindings=False)]

    def on_event(self, event, payload):
        if event == Events.PRINT_STARTED:  # If a new print is beginning
            self._logger.info("Printing started: Filament sensor enabled")
            if self.pin != -1:
                GPIO.add_event_detect(self.pin, GPIO.BOTH, callback=self.check_gpio, bouncetime=self.bounce)
        elif event in (Events.PRINT_DONE, Events.PRINT_FAILED, Events.PRINT_CANCELLED):
            self._logger.info("Printing stopped: Filament sensor disabled")
            try:
                GPIO.remove_event_detect(self.pin)
            except Exception:
                pass

    def check_gpio(self, channel):
	global time2
	while time1-30 > time2:
	    time1 = time.time()
	    state = GPIO.input(self.pin)
            self._logger.info("time1: [%s] time2: [%s]"%(time1, time2))
            if state != self.switch:    # If the sensor is tripped
                time2 = time.time()
	        self._logger.info("Sensor tripped")
	    time.sleep(1)
	
	if self._printer.is_printing():
	    self._printer.toggle_pause_print()
	    self._logger.info("PRINT STOPPED")

    def get_update_information(self):
        return dict(
            octoprint_filament=dict(
                displayName="Filament Sensor Reloaded",
                displayVersion=self._plugin_version,

                # version check: github repository
                type="github_release",
                user="Clone5656",
                repo="Octoprint-Filament-Reloaded",
                current=self._plugin_version,

                # update method: pip
                pip="https://github.com/Clone5656/Octoprint-Filament-Reloaded/archive/{target_version}.zip"
            )
        )

__plugin_name__ = "Filament Sensor Reloaded"
__plugin_version__ = "1.0.1"

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = FilamentReloadedPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
}
