[![YouTube Channel Views](https://img.shields.io/youtube/channel/views/UCz5BOU9J9pB_O0B8-rDjCWQ?label=YouTube&style=social)](https://www.youtube.com/channel/UCz5BOU9J9pB_O0B8-rDjCWQ)

# Button

A method for invoking a script using a bluetooth button ([flic](https://flic.io/shop/flic-2-three-pack)) on a linux machine (eg Raspberry Pi). 

The example is for a **Kef LS50** wireless set of speakers, but can be adapted to any script (send an email then start a timer then set all the house lights to red then play Barry White etc etc).
It controls the Kef LS50s over the local network rather than using an Infrared Remote. The motivation for this example is that the source button on the Kef Remote is annoying because you need to toggle through unused sources. /firstworldproblem

This is a very specific use-case that led to a pretty general method, so for now, the instructions might seem a bit garbled. Bear with us.

# Prerequisites

First of all if you're using the Kef speakers example, clone [kefctl](https://github.com/kraih/kefctl). This is the perl code that will actually control the speaker by issuing commands over your network. 

Then install [fliclib](https://github.com/50ButtonsEach/fliclib-linux-hci) and start flicd as a service.
NB. If you're running in a Raspberry Pi, then you need to disable and mask the bluetooth service with the following commands:

```
 sudo systemctl stop bluetooth.service
 sudo systemctl mask bluetooth.service
```

# Installation

Clone this repository and enter the directory
```
cd ~
git clone https://github.com/veebch/button.git
cd button
```

# Run
Edit the file flicKEF.py to contain the commands that you want to invoke, or if you're using the Kef speaker example, leave things as they are.
To start the code that listens to a button you've already paired to flicd (documented on the [fliclib github page](https://github.com/50ButtonsEach/fliclib-linux-hci)):
```
python3 flicKEF.py
```
# Run as a service

Make the systemd service file by running the following in a terminal:

```
cat <<EOF | sudo tee /etc/systemd/system/speakerflic.service
[Unit]
Description=speakerflic
After=flicd.service


[Service]
ExecStart=/usr/bin/python3 flicKEF.py
WorkingDirectory=/home/pi/fliclib-linux-hci/clientlib/python/
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi


[Install]
WantedBy=multi-user.target

EOF

```
Now, start the service and reboot.

```
sudo systemctl enable speakerflic.service
sudo systemctl enable speakerflic.service
sudo reboot
```
# To Do

Place button functions into a config file to simplify the process. 

# License 

GPL 3.0

