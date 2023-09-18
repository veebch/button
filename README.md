[![YouTube Channel Views](https://img.shields.io/youtube/channel/views/UCz5BOU9J9pB_O0B8-rDjCWQ?label=YouTube&style=social)](https://www.youtube.com/channel/UCz5BOU9J9pB_O0B8-rDjCWQ)

# Button

A method for running a script on your linux machine using a bluetooth (flic) button and a linux machine (eg Raspberry Pi). The example is for a **Kef LS50** wireless set of speakers, but can be adapted to any device that responds to commands made over your network.
 
The script runs while flicd is running and controls a KEF LS50 wireless over the LAN rather than using an IR blaster. The motivation for this example is that the source button on the Kef Remote is annoying because you need to toggle through unused sources. /firstworldproblem

# Prerequisites

First of all, clone [kefctl](https://github.com/kraih/kefctl). This is the perl code that will actually control the speaker by issuing commands over your network. Then install [fliclib](https://github.com/50ButtonsEach/fliclib-linux-hci) and start flicd as a service.
If you're running in a raspberry pi, you need to disable and mask the bluetooth service:

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
ExecStart=/usr/bin/python3 -u /home/pi/fliclib-linux-hci/cli$
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
# TO DO

Get button assignments to run from a config file. 

# License 

GPL 3.0

