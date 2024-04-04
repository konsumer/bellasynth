First, setup [patchbox os](https://community.blokas.io/t/beta-patchbox-os-image-2022-05-17/3774).

|               |              |
| ------------- | ------------ |
| User name     | `patch`      |
| Password      | `blokaslabs` |
| WiFi SSID     | Patchbox     |
| WiFi password | `blokaslabs` |

- Login. Connect to Patchbox Wifi, then run `ssh patch@patchbox.local`
- Go through initial setup. I setup jack audio.
- I chose console, to start
- Under button/assign/CLICK_3 set it to "toggle wifi hotspot". this is how you get back to hotsspot mode


## setup

Initially, I did this:

```
sudo apt update
sudo apt upgrade
sudo reboot

sudo systemctl disable vncserver-x11-serviced.service
sudo systemctl disable vncserver-virtuald.service
```

Since I am using PatchOS, I made a  module to make it easier. Install like this:


```
patchbox module install https://github.com/konsumer/bellasynth
patchbox module activate bellasynth

```

It's similar to puredata module, but it adds harware support and a pygame-based GUI.


### network gadget

I want net gadget-mode (network over USB) so no wifi is needed to interact with device (just plug into computer) so I did this:

```

```


## usage

Things to do over ssh:

```
# at any time you can start vnc/x
startx &


# re-enable VNC at boot
sudo systemctl enable vncserver-x11-serviced.service
sudo systemctl enable vncserver-virtuald.service
sudo systemctl start vncserver-x11-serviced.service
sudo systemctl start vncserver-virtuald.service

# configure patchOS things
patchbox
```