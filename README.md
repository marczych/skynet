# Skynet

Repository of instructions, links, and webserver code for building an API for
sending IR commands on a Raspberry Pi.

This project was built for controlling skylight shades via IR via a raspberry
pi hence the Skynet name. However, the general approach can be used for other
applications as well so feel free to modify it to suit your needs!

## Recording Commands

```bash
ir-ctl --device /dev/lirc1 --receive > command_name
```
