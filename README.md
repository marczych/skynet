# Skynet

Repository of instructions, links, and webserver code for building an API to
send IR commands on a Raspberry Pi. Don't miss the
[accompanying blog post][blog]!

This project was built for controlling skylight shades via IR via a raspberry
pi hence the Skynet name. However, the general approach can be used for other
applications as well so feel free to modify it to suit your needs!

This project in its current state provides:

 - Python webserver to provide the REST API and serve the web frontend
 - REST API to execute commands
 - Web frontend for users to send commands
 - Systemd unit file to run the server
 - Commands for controlling my skylights to serve as examples (`commands/`)

The remainder of this README provides installation instructions for the API and
frontend, instructions for generating commands, and a broad overview of how I
set up my Raspberry Pi for this project.

## Installation

This section provides installation instructions for just the server and assumes
that the IR transmitter is already configured. See the Hardware/Software Setup
sections below for tips for configuring that.

 - Copy this directory to `/opt/skynet/` on your Pi e.g. `rsync`/`scp`/`git
   clone`.
 - Install commands to `/opt/skynet/commands/`
 - Install server dependencies:
   `sudo pip3 install --requirement /opt/skynet/requirements.txt`.
 - Copy or symlink `/opt/skynet/skynet.service` to
   `/etc/systemd/system/skynet.service`.
 - Start the service with `sudo systemctl start skynet`.
 - Enable the service to start on boot with `sudo systemctl enable skynet`.

## REST API

The only available endpoint is `POST /api/command` with a JSON payload with the
command to run e.g.

```
POST /api/command
{"command": "foobar"}
```

In this case, `foobar` must be the name of a file in the commands directory.

## Recording Commands

Recording commands for this service can be done by running the following
command and pressing the relevant button on your remote to capture it:

```bash
ir-ctl --device /dev/lirc1 --receive > command_name
```

Note: This assumes that there is an IR receiver at `/dev/lirc1`.

## Bill of Materials

The majority of the bill of materials are normal Raspberry Pi parts other than
the IR shield but you can swap any of them out as long as you end up with a
functioning Pi with devices for sending/receiving IR signals.

 - [Raspberry Pi Zero W] but I imagine any Raspberry Pi would work
 - [IR Transmitter/Receiver Shield] to send/receive IR signals
 - [Break-Away headers] to connect the IR shield to the Pi
 - [Power supply]
 - [SD card]

[Raspberry Pi Zero W]: https://www.raspberrypi.org/products/raspberry-pi-zero-w/
[IR Transmitter/Receiver Shield]: https://www.amazon.com/gp/product/B0713SK7RJ
[Break-Away headers]: https://www.amazon.com/gp/product/B0756KM7CY
[Power supply]: https://www.amazon.com/gp/product/B00MARDJZ4
[SD card]: https://www.amazon.com/gp/product/B07YLZ8D1Y

## Hardware Setup

The hardware setup is very simple:

 - [Solder the breakaway headers to the Pi][soldering]
 - Attach the IR shield to the headers

[soldering]: https://www.raspberrypi.org/blog/getting-started-soldering/

## Software Setup

Many of the guides that I followed didn't quite pan out for one reason or
another. In particular, the guide that was provided with the IR shield was very
out dated and I couldn't get [LIRC] to work due to what appeared to be some
kernel changes that landed in Raspbian in mid 2019. This made a lot of the
existing IR tutorials and tools irrelevant but that's okay because they aren't
strictly necessary.

I followed [this guide][pi setup] for the initial OS install and WiFi/SSH
setup which should work for any Pi. Next, configure the IR devices by adding
these lines to `/boot/config.txt` (or by modifying the commented out ones if
they exist):

```
dtoverlay=gpio-ir,gpio_pin=18
dtoverlay=gpio-ir-tx,gpio_pin=17
```

The pin numbers came from the manufacturer's guide so it might differ for your
peripheral. At this point, you likely need to restart a service or reboot to
get the devices to show up at `/dev/lirc0` and `/dev/lirc1`. I didn't have any
issues with having unstable device names for the transmitter or receiver so I
didn't bother but you might consider setting udev rules if you want to ensure
that they are always the same and get more convenient names for them too.

### Testing

It is now time to test it out to make sure that everything is set up correctly.
Run this to print out the raw data as the transmitter sees it (send IR signals
to it by pressing buttons on a remote):

```bash
ir-ctl --device /dev/lirc1 --receive
```

You should see alternating lines with `pulse`/`space` if it's working (see
examples in the `commands/` directory). You can save that output to a file and
use that as a command (you might want to trim off the `truncate` line at the
end to avoid a warning when sending it).

Finally, you can replay the command by running:

```bash
ir-ctl --device /dev/lirc0 --send path/to/command
```

You can check if it's working by viewing the IR transmitter through a camera to
see if there is a faint light like the one produced when filming other remotes.

And that's it! It isn't quite as elegant as creating a remote for LIRC but it
should be able to replay any IR signal you can throw at it!

[LIRC]: https://www.lirc.org/
[pi setup]: https://www.losant.com/blog/getting-started-with-the-raspberry-pi-zero-w-without-a-monitor
[blog]: http://marczych.com/2020/05/10/skynet.html
