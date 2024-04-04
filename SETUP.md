I did a fresh setup of pi os lite (enable user & ssh and wifi in Raspberry Pi Imager.)

Once you can ssh into it:

```sh
sudo apt update
sudo apt upgrade
sudo apt install -y i2c-tools git python3-pip python3-setuptools libgpiod-dev python3-libgpiod puredata
sudo pip3 install --break-system-packages pygame RPi.GPIO adafruit-blinka

sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_spi 0
sudo raspi-config nonint do_serial_hw 0
sudo raspi-config nonint do_ssh 0
sudo raspi-config nonint do_camera 0
sudo raspi-config nonint disable_raspi_config_at_boot 0
```


## addons

```
sudo apt install -y pd-cyclone pd-deken pd-purepd puredata-extra puredata-import puredata-utils pd-3dp pd-ableton-link pd-ambix pd-arraysize pd-autopreset pd-bassemu pd-beatpipe pd-boids pd-bsaylor pd-chaos pd-cmos pd-comport pd-creb pd-csound pd-cxc pd-cyclone pd-deken pd-deken-apt pd-earplug pd-ekext pd-ext13 pd-extendedview pd-fftease pd-flext-dev pd-flext-doc pd-flite pd-freeverb pd-ggee pd-gil pd-hcs pd-hexloader pd-hid pd-iem pd-iemambi pd-iemguts pd-iemlib pd-iemmatrix pd-iemnet pd-iemutils pd-jmmmp pd-jsusfx pd-kollabs pd-lib-builder pd-libdir pd-list-abs pd-log pd-lua pd-lyonpotpourri pd-mapping pd-markex pd-maxlib pd-mediasettings pd-mjlib pd-moonlib pd-motex pd-mrpeach pd-mrpeach-net pd-nusmuk pd-osc pd-pan pd-pddp pd-pdogg pd-pdp pd-pdstring pd-pduino pd-plugin pd-pmpd pd-pool pd-puremapping pd-purepd pd-purest-json pd-readanysf pd-rtclib pd-sigpack pd-slip pd-smlib pd-syslog pd-tclpd pd-testtools pd-unauthorized pd-upp pd-vbap pd-wiimote pd-windowing pd-xbee pd-xsample pd-zexy
```

And lots of LADSPA plugins (use with `plugin~`):

```
sudo apt install -y ladspalist amb-plugins autotalent blepvco blop bs2b-ladspa cmt dpf-plugins-ladspa fil-plugins guitarix-ladspa invada-studio-plugins-ladspa lsp-plugins-ladspa mcp-plugins omins rev-plugins rubberband-ladspa ste-plugins swh-plugins tap-plugins vco-plugins vlevel wah-plugins zam-plugins
```

## vnc

```
sudo apt install -y fluxbox lightdm
```

Now, under `sudo raspi-config`:
- "Interface Options" / "VNC" / "Yes"
- "System Options" / "Boot / Auto Login" / "Desktop Autologin"

Now, edit `~/.fluxbox/startup` and add this before last `exec`:

```
sudo puredata -rt ~/pd/MAIN.pd &
```

## samba

This adds windows networked file access. I added a simple config to `etc/samba/smb.conf`:

```
# Global parameters
[global]
  dns proxy = No
  guest account = pi
  log file = /var/log/samba/log.%m
  map to guest = Bad Password
  max log size = 1000
  panic action = /usr/share/samba/panic-action %d
  passwd chat = *Enter\snew\s*\spassword:* %n\n *Retype\snew\s*\spassword:* %n\n *password\supdated\ssuccessfully* .
  passwd program = /usr/bin/passwd %u
  security = USER
  server role = standalone server
  server string = %h server (Samba, Raspberry OS)
  workgroup = NULL
  idmap config * : backend = tdb


[pi]
  force create mode = 0660
  force directory mode = 0770
  guest ok = Yes
  guest only = Yes
  path = /home/pi
  read only = No
```


## gadget mode

This makes it so it acts as a USB network device when you plug it into a computer. You can find good instructions [here](https://www.hardill.me.uk/wordpress/2019/11/02/pi4-usb-c-gadget/).


## python

The firmware needs some stuff:

```
sudo pip3 install --break-system-packages adafruit-circuitpython-ssd1306 pillow python-osc 
```


## todo

- [midi auto-connect](https://github.com/BlokasLabs/amidiauto)
- start pd with no gui early, if in gadget-mode, run Xvnc/fluxbox/pd-gui (and samba, if using that)
- MTP in gadget-mode (so no samba needed)
- MIDI in gadget-mode
- automate bluetooth pairing for select devices
- OLED splash screen 
- look through [pisound script](https://github.com/BlokasLabs/pisound) for anything else that is useful
- CLI menus with [whiptail](https://whiptail.readthedocs.io/en/latest/example.html)?
- restart services on change: puredata, python
- web VNC client
- [this](https://github.com/larsks/systemd-usb-gadget) is a nicer gadget setup
