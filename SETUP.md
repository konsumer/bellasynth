I did a fresh setup of pi os lite (enable user & ssh and wifi in Raspberry Pi Imager.)

Once you can ssh into it:

```sh
sudo apt update
sudo apt upgrade
sudo apt install -y i2c-tools git python3-pip python3-setuptools libgpiod-dev python3-libgpiod puredata
sudo pip3 install --break-system-packages pygame RPi.GPIO adafruit-blinka oscpy

sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_spi 0
sudo raspi-config nonint do_serial_hw 0
sudo raspi-config nonint do_ssh 0
sudo raspi-config nonint do_camera 0
sudo raspi-config nonint disable_raspi_config_at_boot 0
```


Additionally you can install lots of addons:

```
sudo apt install -y pd-cyclone pd-deken pd-purepd puredata-extra puredata-import puredata-utils pd-3dp pd-ableton-link pd-ambix pd-arraysize pd-autopreset pd-bassemu pd-beatpipe pd-boids pd-bsaylor pd-chaos pd-cmos pd-comport pd-creb pd-csound pd-cxc pd-cyclone pd-deken pd-deken-apt pd-earplug pd-ekext pd-ext13 pd-extendedview pd-fftease pd-flext-dev pd-flext-doc pd-flite pd-freeverb pd-ggee pd-gil pd-hcs pd-hexloader pd-hid pd-iem pd-iemambi pd-iemguts pd-iemlib pd-iemmatrix pd-iemnet pd-iemutils pd-jmmmp pd-jsusfx pd-kollabs pd-lib-builder pd-libdir pd-list-abs pd-log pd-lua pd-lyonpotpourri pd-mapping pd-markex pd-maxlib pd-mediasettings pd-mjlib pd-moonlib pd-motex pd-mrpeach pd-mrpeach-net pd-nusmuk pd-osc pd-pan pd-pddp pd-pdogg pd-pdp pd-pdstring pd-pduino pd-plugin pd-pmpd pd-pool pd-puremapping pd-purepd pd-purest-json pd-readanysf pd-rtclib pd-sigpack pd-slip pd-smlib pd-syslog pd-tclpd pd-testtools pd-unauthorized pd-upp pd-vbap pd-wiimote pd-windowing pd-xbee pd-xsample pd-zexy
```

And lots of LADSPA plugins (use with `plugin~`):

```
sudo apt install -y ladspalist amb-plugins autotalent blepvco blop bs2b-ladspa cmt dpf-plugins-ladspa fil-plugins guitarix-ladspa invada-studio-plugins-ladspa lsp-plugins-ladspa mcp-plugins omins rev-plugins rubberband-ladspa ste-plugins swh-plugins tap-plugins vco-plugins vlevel wah-plugins zam-plugins
```