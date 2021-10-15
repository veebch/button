[![YouTube Channel Views](https://img.shields.io/youtube/channel/views/UCz5BOU9J9pB_O0B8-rDjCWQ?label=YouTube&style=social)](https://www.youtube.com/channel/UCz5BOU9J9pB_O0B8-rDjCWQ)

# flicKEF

This script runs while flicd is running and controls a KEF LS50 wireless over the lan rather than using an IR blaster. The reason is that the source button is annoying and you need to toggle through unused sources.

# Prerequisites

First of all, clone [kefctl](https://github.com/kraih/kefctl). This is the perl code that will actually control the speaker. Then install [fliclib](https://github.com/50ButtonsEach/fliclib-linux-hci) and start flicd as a service.
If you're running in a raspberry pi, you need to disable and mask the bluetooth service:

```
 sudo systemctl stop bluetooth.service
 sudo systemctl mask bluetooth.service
```

# Run
```
python3 flicKEF.py
```
# Run as a service
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

Get it to run from a config file. More flexibility.

# License 

GPL 3.0

