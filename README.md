# light

control your elgato ring light

i'll probably rewrite this in rust... tomorrow

```
usage: light [-h] [--brightness BRIGHTNESS] [--color COLOR] [--ip IP] [--toggle] [--status]

optional arguments:
  -h, --help            show this help message and exit
  --brightness BRIGHTNESS
                        Desired brightness in percent (range [3, 100])
  --color COLOR         Desired color temperature in Kelvin (range [2900, 7000])
  --ip IP               the local IP address for the Elgato Ring Light
  --toggle              toggle the light on or off, depending on its state
  --status              print the current state of the light
```