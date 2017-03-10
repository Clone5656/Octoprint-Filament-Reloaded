# OctoPrint-FilamentReloaded

Based on the Octoprint-Filament-Reloaded plugin by kontakt (https://github.com/kontakt/Octoprint-Filament-Reloaded), this modification is for the use of a hall sensor instead a filament sensor. It uses the hall sensor to detect the magnets on a wheel that is spun as filament is fed.

Future developments are planned to include multiple filament sensors, pop-ups, pre-print validation and custom filament run-out scripting.

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/Clone5656/Octoprint-Filament-Reloaded/archive/master.zip

Using this plugin requires a filament sensor. The code is set to use the Raspberry Pi's internal Pull-Up resistors, so the switch should be between your detection pin and a ground pin.
