# Working Stargate Mk2 Control Code with Raspberry Pi

Control code for [Glitch's Working Stargate Mk2](https://www.thingiverse.com/thing:1603423) via a web browser.

Written by [Dan Clarke](https://github.com/danclarke). Dialing "address book", debug page, and other refinements added by [Jeremy Gustafson](https://github.com/jeremygustafson).

Updated November 2021 for latest Raspberry Pi OS "Buster", python3, as well as a [revised custom PCB](https://oshwlab.com/jeremyrgustafson/stargate-hat-with-wormhole) to support a "wormhole" light strip.

A note from Jeremy: my background is in software, not electrical engineering, so I've tried to clarify some of the directions I found confusing when I was first starting my build. Those who are more familiar with electronics may find some of what I've written to be tediously over-explained, but my goal was to take both Glitch's and Dan's amazing work and make it more accessible to people like me who may need just a little extra hand-holding along the way. (in my case, my Dad provided the hand-holding!) With that said, Dan's original warning still applies:

**Warning:** Do not attempt this build if you don't have a rudimentary understanding of electronics and Linux. This build involves surface-mount soldering, updating of Python files, and basic configuration of Linux via command line. There is no GUI.

Last preface: I (Jeremy) have tried hard to make these directions as complete as possible, but there might be things I missed or forgot about. If you find a mistake or something is missing, please let me know so I can try to fix it!

## Requirements
- 1x Raspberry Pi 3 B+ (a Pi 4 might work, but I started my build before the 4 had been released; I'd recommend sticking with the 3B+ unless you really know what you're doing)
- 1x [Adafruit Motor Hat](https://www.adafruit.com/product/2348)
- 2x sets of [Adafruit Brass Standoffs](https://www.adafruit.com/product/2336)
- 1x 2.54mm 2x20 stacking header [C35165](https://lcsc.com/product-detail/Female-Header_2-54mm-2-20P_C35165.html) 
- 1x [Adafruit I2S 3W Breakout](https://www.adafruit.com/product/3006)
- 1x [2.5 or 3" Speaker](https://www.adafruit.com/product/1314)
- 2x [Adafruit Stepper motor - NEMA-17 size - 200 steps/rev, 12V 350mA](https://www.adafruit.com/product/324)
- 1x [12V DC power supply adapter](https://smile.amazon.com/gp/product/B01AZLA9XQ)
- 1x bright white 5mm LED (Glitch used a Lumex SLX-LX5093UWC/C - 3.4V 23mA) (you could use a different LED, as long as it is VERY bright)
- 1x [Photoresistor / light dependent resistor (LDR)](https://www.adafruit.com/product/161)
- 8x 1206-style [White LEDs for the ramp](https://lcsc.com/product-detail/Light-Emitting-Diodes-LED_white1206-Non-warm-tones-of-white_C71796.html) (Glitch used 8 x Broadcom ASMT-YWB1-NGJB2 - 3.2V 60mA)
- 27x [Orange LEDs for the chevrons](https://lcsc.com/product-detail/Light-Emitting-Diodes-LED_FC-3215HOK-600H-Orange_C130716.html) (Glitch used Kingbright KPT-1608SECK 2.1V 20mA) 
- 1x Revised [Stargate HAT Printed Circuit Board (PCB)](https://oshwlab.com/jeremyrgustafson/stargate-hat-with-wormhole), and the electronics listed in that section below
- thin wire, jumper wires, thin-tipped soldering iron, other various tools for electronics work, multimeter, etc
- Optional: 1x [12V Blue LED strip for wormhole](https://smile.amazon.com/gp/product/B07MXVRSR9/)
- Optional: 1x [WaveShare 7 inch HDMI touch screen](https://smile.amazon.com/gp/product/B077PLVZCX/)
- Optional: 1x [short HDMI cable for monitor](https://smile.amazon.com/gp/product/B06XT7ZTTH/)


### Motor HAT
The Adafruit Motor HAT will be stacked directly on top of the Raspberry Pi, with Dan's custom Stargate HAT/PCB then stacked on top of the Motor HAT. You will need pass-through stacking headers from the Pi to the Motor HAT. Dan suggested (and I also used) [C35165](https://lcsc.com/product-detail/Female-Header_2-54mm-2-20P_C35165.html) from LCSC. The stacking header needs to be soldered onto the Motor HAT (the header goes underneath the board and pins come through the holes to be soldered on top). You'll also need to solder on the 5 terminals that ship with the Motor HAT.

When you connect the stepper motors to the Motor HAT's terminals (M1-GND-M2 and M3-GND-M4), if you find your motors spin the wrong direction, swap the yellow and red wires to reverse the spin direction. My wires for each motor ended up as: yellow, red, (empty), green, grey.

### Custom PCB
My revised [custom Stargate HAT/PCB](https://oshwlab.com/jeremyrgustafson/stargate-hat-with-wormhole) based off of Dan's original design has all connections and required components marked in the silkscreen. The following components are required to be soldered directly to this PCB. Many have minimum order sizes because they come on a "tape and reel," but because they are so inexpensive it doesn't add much cost.

 - 11x BC847 SOT23 Transistors [C8547](https://lcsc.com/product-detail/Transistors-NPN-PNP_BC847A-1E_C8574.html)
 - 1x SS8050 1.5A Transistor [C2150](https://lcsc.com/product-detail/Bipolar-Transistors-BJT_Changjiang-Electronics-Tech-CJ-SS8050_C2150.html)
 - 10x 470ohm 0805 Resistor [C114747](https://lcsc.com/product-detail/Chip-Resistor-Surface-Mount_470R-471-5_C114747.html)
 - 2x 10k ohm 0805 Resistor [C84376](https://lcsc.com/product-detail/Chip-Resistor-Surface-Mount_10KR-1002-1_C84376.html)
 - 1x [LM2596S Buck Converter Breakout](https://www.bitsbox.co.uk/index.php?main_page=product_info&cPath=140_171&products_id=3202)
 - 1x [MCP3008](https://smile.amazon.com/gp/product/B01HGCSGXM/)
 - 1x [16-pin DIL Socket](https://www.bitsbox.co.uk/index.php?main_page=product_info&cPath=255_256&products_id=1933) (strictly speaking this is optional, but I'd highly recommend it so you're not soldering the MCP3008 directly to the PCB)
 - 1x 5mm 2-pin terminal [C3703](https://lcsc.com/product-detail/Terminal-Blocks_WJ127-5-0-2P_C3703.html)
 - 1x 2.54mm 7-pin female header [C124418](https://lcsc.com/product-detail/Female-Header_Shenzhen-Cancome-Female-header-1-7P-2-54mm-Straight-line_C124418.html)
 - 1x 2.54mm 2x20 female header - short [C50982](https://lcsc.com/product-detail/Female-Header_2-54mm-2-20PFemale-header_C50982.html)

Because the Stargate HAT/PCB will be at the top of the stack, you can use a standard female header/socket instead of the pass-through (mentioned earlier for the HAT). Like the Motor Hat, the header needs to be soldered into the PCB.

Power for the whole system is provided via the Stargate HAT/PCB, so you will not need to plug in the Raspberry Pi board directly (except once during initial setup, described later).

#### Pinouts

| Pin | Item |
| :---: | :---: |
| GPIO17 | Chevron 1 |
| GPIO27 | Chevron 2 |
| GPIO22 | Chevron 3 |
| GPIO5 | Chevron 4 |
| GPIO6 | Chevron 5 |
| GPIO13 | Chevron 6 |
| GPIO26 | Chevron 7 |
| GPIO12 | Chevron 8 |
| GPIO16 | Chevron 9 |
| GPIO24 | Ramp LEDs |
| GPIO20| Calibration LED |
| GPIO19 | Audio LRCLK |
| GPIO18 | Audio BCLK |
| GPIO21 | Audio DIN |
| GPIO8 | MCP3008 CS |
| GPIO10 | MOSI |
| GPIO9 | MISO |
| GPIO11 | SCLK |
| GPIO23 | Wormhole |

The physical Chevron wire ordering does not matter since it will be corrected in software.

## Connections and soldering

Set up your Raspberry Pi for SSH so that the Pi can be configured without direct physical access (for this initial setup you *will* need to plug the Pi into normal power; after this, though, the Pi's power will be supplied from the Stargate HAT).

Prior to soldering, connect the LM2596S Buck Converter to your 12V power supply and adjust the potentiometer until 5.1V is at the output terminals.

Solder the LM2596S Buck Converter onto the Stargate HAT. Dan suggested using any available wire such as the offcuts from LEDs; I (Jeremy) used individual header pins, and those worked well for me.

I didn't have this particular spacing issue, but Dan's original instructions noted: When soldering the LM2596S, ensure the bottom part (Output) is flush with the PCB. Due to some of the through-hole components the entire board can't be flush, but it's important the lower part is. The top part (Input) can stand slightly proud since there's more space between it and the ramp.

Solder the 2-pin terminal to the 12V space marked on the Stargate HAT, then connect your 12V power supply to it. (I used male-male jumper wires to connect to the [12V DC power supply adapter](https://smile.amazon.com/gp/product/B01AZLA9XQ); it was a while yet before I connected that to real power from the wall).

Solder jumper wires on the Stargate HAT's 12V-2 terminal output, and run them to the 12V input of the Motor HAT. Power is provided for the whole system via the LM2596S Buck Converter (then down through the Motor HAT, then to the Pi via the 40-pin headers), so do not connect power directly to the Raspberry Pi.

If you haven't already, this is a good time to solder the 40-pin headers: one set coming up into your Motor HAT and the other into your Stargate HAT/PCB. Once that's done, you can stack the Motor HAT onto the Pi (using one set of the brass standoffs on the side opposite the header pins to help support the board). The Stargate HAT/PCB can be stacked on top later, once all the soldering on that board is done.

For connections to the LEDs and LDR Dan used LED strip JST connectors. I missed reading that note in his directions, so I used some available male-female jumper wires, soldering the male end of each to the appropriate spots on the Stargate HAT and plugging the LED and LDR wires directly into the female ends of the jumpers, then wrapping with electrical tape as needed. I did this for the chevron LEDs, ramp LEDs, calibration LED, and the calibration LDR (light dependent resistor).

The calibration LED is powered via 12V from the "Gantry" section on the Stargate HAT/PCB, with ground to the "LED" pin in the Gantry row. **The LDR must be powered via 3.3V, not 12V**, and its ground goes to the "LDR" pin in the Gantry row.

On a related side-note: as far as I can tell, on the Stargate HAT, neither the Gate nor Gantry's ground ("GND") pins are used, since the ground is provided by each of individual gate chevrons and the gantry ramp LEDs. I'm not a master electrician, though, so it's entirely possible I'm wrong, all I can say is my Stargate lights up correctly and I didn't use those two pins.

Lastly, use the 7-pin female header to solder the audio breakout board onto the Stargate HAT/PCB (to the "Audio" row of pins on the PCB).

When fully assembled, the Raspberry Pi stack fits at a slightly skewed angle on the two left-most screw holes in the base - it sounds like Dan screwed his Pi into place on the Stargate base, but for my build I couldn't quite get the Pi to line up to the holes, and also needed to shift it around once I put the ramp top piece on; it still all fit for me, but just barely. In particular, I had to bend my pins a little bit so the mini-breakout audio board sits at a slight angle under the ramp.

## LEDs
The chevron LEDs are all powered from the PCB's "Gate" row's 12V pin (I daisy chained the 12V wire to each LED's anode lead), with ground going to each of the labeled chevron numbers in that row on the PCB. You will also need to solder the surface mount resistors and transistors onto the board, as well as the DIL socket (which the MCP3008 sits in).

The Ramp / Gantry LEDs can be wired in series on each side, with no resistor. The 12V divided by the 4 LEDs results in 3V to each LED. This should nicely dim the white LEDs resulting in a well-lit but not overwhelmingly bright ramp. Ground goes to the "RMP" pin on the PCB. This is also significantly easier to wire up than a resistor and power line to each individual LED. If your LEDs can't be lit with 3V, you'll need to customise your wiring and potentially add in some resistors.

Dan used 1206 surface mount LEDs from [Bright Components](http://bright-components.co.uk/), however any LED of the right colour will work. (I used the LEDs linked in the Requirements section, above). The 1206 form factor is much easier to solder than the 0604s used in Glitch's original instructions and fit fine.

Dan notes: be very careful of the pads on the LEDs, they're very easy to rip off in this application. Ensure all wires have strain relief to prevent a pad from being accidentally ripped off. He used small dots of hotmelt glue to hold wires in place and adds to be very careful with hotmelt and PLA since it will soften and even melt the PLA.

Instead of hot glue, I soldered the three LEDs into a straight line with an inch or so of wire between then, then *carefully* twisted the whole set of three into a loop, and superglue each LED onto the holders I'd printed from [www.thingiverse.com/thing:2795518](https://www.thingiverse.com/thing:2795518). This worked really well. Once the LED loops were glued onto the holders, I could then place each holder / set of three LEDs into the gate in order to measure how long of wire I needed to reach out the bottom of the gate (these were the ground wires that will go into the numbered pins on the PCB) and then to continue daisy chaining the 12V supply on to the next chevron. I then removed the LED holders and soldered all the long wires together, before putting the LED holders and wires back into the gate for final assembly. I test-fitted all the LED holders underneath the 3D printed front pieces of the Stargate, before gluing each into place, one section at a time. I started at the very top of the gate and worked my way down each side, which made wire management easier. Also, be sure to mark your 12V wire (or wires - I used a separate 12V wire on each "side" of the gate) otherwise you risk ending up with 10 or 11 wires out the bottom of your gate and no idea which ones are supposed to be 12V vs ground. (I speak from experience)


## Rasperry Pi Setup

### Install Raspbian Lite
First [install a fresh copy of Raspbian Lite](https://www.raspberrypi.org/documentation/installation/installing-images/). At the time of this writing, the latest release was "Buster" (build date May 7, 2021). Newer versions of Raspbian may require changes to portions of these directions.

Before installing your SD card into the Pi, set it up for wireless access and ssh ("headless" setup). The exact steps here will differ depending if you're on a Mac or Windows. I've written these instructions based on macOS.

On your laptop, with the SD card inserted, open your Applications > Utilities > Terminal.app.

Perform step 3 from https://www.raspberrypi.org/documentation/remote-access/ssh/ to enable ssh:

```touch /Volumes/boot/ssh```

Then, follow these steps to set up wifi access: https://www.raspberrypi.org/documentation/configuration/wireless/headless.md

```vi /Volumes/boot/wpa_supplicant.conf```

(I use `vi` for my editor; if you're new to the command line, replace the word "vi" with "nano" in the command above, and anywhere else in this document that you see "vi")

Add these lines to the file, changing the ssid and psk variables for your own wifi network:

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=US

network={
	ssid="YOUR WIFI NETWORK NAME"
	psk="YOUR WIFI PASSWORD"
}
```

Unmount the SD card and move it from your laptop to your Pi. Plug in the Pi (either directly, or, if you've already assembled your PCB HAT, you can attach the HAT onto the Pi and plug in the 5V/12A power adapter; DO NOT plug in BOTH the power adapter and also the Pi's power adapter).

**Important:** if you choose to use the optional WaveShare 7" monitor I listed above, don't plug it into the Pi until you've changed the required settings (described below).

Wait 5 minutes for the Pi to boot the first time. You should then be able to connect to it (in your Terminal) by typing `ssh pi@raspberrypi.local`. (Dan set up his Pi with a static IP; I chose not to do that, but you can if you want. His directions are at [https://github.com/danclarke/WorkingStargateMk2Raspi](https://github.com/danclarke/WorkingStargateMk2Raspi))

Once connected, I suggest changing the hostname to `stargatepi`, and also changing the pi user's default password. To do both of these, type `sudo raspi-config` and look for the appropriate menu items. After rebooting, you can then connect with `ssh pi@stargatepi.local`.


### Passwordless SSH
If desired, you can also set up passwordless ssh at this time.

```
pi$ ssh-keygen
# Hit enter at each of the prompts

pi$ nano .ssh/authorized_keys
```

Into that authorized_keys file, paste the contents of this next command, then save the file:

```your laptop$ cat .ssh/id_rsa.pub```


### Run updates

Even though you just installed a brand new image, check for (and install) any software updates. Follow the prompts after each of these three commands:

```
pi$
sudo apt-get update
sudo apt-get upgrade
sudo apt autoremove
```

### Optional: Install vi text editor

```
sudo apt-get install vim
sudo update-alternatives --config editor
```

```
vi ~/.vimrc
# Add this line:
set mouse-=a
```

```
sudo vi /root/.vimrc
# Add this line:
set mouse-=a
```


### Install required packages

Some of these may already be at the newest version.

```
sudo apt install python3 python3-daemon python3-pip python3-gpiozero build-essential git python3-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsdl1.2-dev libsmpeg-dev python3-numpy subversion libportmidi-dev ffmpeg libswscale-dev libavformat-dev libavcodec-dev
```

Install one more package, required for controlling the speaker volume from the web page interface:

```sudo apt install alsa-utils```

Install the required Python packages:

```sudo pip3 install Adafruit-MCP3008 pygame gpiozero daemon daemontools python-daemon```

### Configure I2C and SPI

I2C and SPI are required for the Motor HAT. Follow these instructions to enable I2C:

https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c

Note: if you're setting up your Pi without the motor HAT attached, you will not see any devices listed at the end when running `i2cdetect`.

Next, follow these instructions to enable SPI:

https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-spi

Lastly, update the I2C speed to 400Khz (400000): 

```
sudo vi /boot/config.txt

# Add this line underneath the line "dtparam=i2c_arm=on"
dtparam=i2c_baudrate=400000
```
(For additional information, see http://www.mindsensors.com/blog/how-to/change-i2c-speed-with-raspberry-pi)


### Configure the I2S Breakout

Follow Adafruit's instructions for the I2S Breakout: https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/raspberry-pi-usage

When prompted, I suggest enabling the /dev/zero playback in background.


### Double check necessary settings are enabled

```sudo vi /boot/config.txt```

Look for these settings:

```
dtparam=i2c_arm=on
dtparam=i2c_baudrate=400000
#dtparam=i2s=on
dtparam=spi=on

```

If using the WaveShare 7" monitor, follow these directions from https://www.waveshare.com/w/upload/5/58/7inch_HDMI_LCD_%28H%29_User_Manual.pdf : 

```sudo vi /boot/config.txt```

Add these lines to the bottom of the file:
```
max_usb_current=1
hdmi_force_hotplug=1
config_hdmi_boost=10
hdmi_group=2
hdmi_mode=87
hdmi_cvt 1024 600 60 6 0 0 0
```
Reboot your pi, after which you can plug in the WaveShare monitor:

```sudo reboot```

Create a folder for the Stargate in the home directory:

```mkdir stargate```

Copy all of the Python files here. I used the following "rsync" command, so I could make edits on my local computer and then upload quickly to the Pi:

```my laptop$ rsync -vPrltgoD -e ssh "/path/to/Stargate/WorkingStargateMk2Raspi/" pi@stargatepi.local:/home/pi/stargate/```


If you're using the WaveShare 7" or another touch-sensitive monitor attached to your Pi, create a script on your Pi's Desktop that will launch the web interface:

```vi /home/pi/Desktop/StargateCommand.sh```

Copy/paste these file contents:

```
#!/bin/bash
# https://pimylifeup.com/raspberry-pi-kiosk/
rm -r /home/pi/.cache/chromium/Default/Cache/*
sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' /home/pi/.config/chromium/Default/Preferences
sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/' /home/pi/.config/chromium/Default/Preferences
export DISPLAY=:0.0
/usr/bin/chromium-browser --noerrdialogs --disable-infobars --disable-session-crashed-bubble --kiosk 127.0.0.1/index.htm &
```

Make the file executable:

```chmod u+x /home/pi/Desktop/StargateCommand.sh```

Later, once the Stargate software is running, you can double tap on this script from your Pi's desktop to launch a full-screen web browser to control the Stargate.

### Running without an internet connection

If your Raspberry Pi won't have an active internet connection, there are a couple extra steps to do. In the "web" folder", edit these three files:

```
index.htm
dialingcomputer.htm
testing.htm
```

and change these lines:

```
<script type="text/javascript" src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
<!--<script type="text/javascript" src="jquery-3.3.1.min.js"></script>-->
```
to:
```
<!-- <script type="text/javascript" src="https://code.jquery.com/jquery-3.3.1.min.js"></script>-->
<script type="text/javascript" src="jquery-3.3.1.min.js"></script>
```

Then, on your Pi, download the jquery file into your "web" directory, so it can be loaded locally instead of over the internet:

```
cd /home/pi/stargate/web/
wget https://code.jquery.com/jquery-3.3.1.min.js
```


## Code Setup

Dan has some great functions built into main.py to allow testing of your LEDs and motors. I've also added some functionality to Dan's original code so I could test each component as I was assembling the gate. The following directions are a combination of both approaches.

For each of the below tests, make sure you're in the stargate directory (`cd /home/pi/stargate`), then run `sudo python3 main.py`

To test the motors: open main.py and comment out `stargate_control.quick_calibration()`, and the entire Web Control section. Uncomment `stargate_control.drive_test()`. This will spin the main gate motor. See the `drive_test()` function in StargateControl.py, and also you can edit the `motor_drive` variable in config.py to use something other than `MICROSTEP` if desired. That seemed to be the smoothest setting for me, though. When done, undo your main.py commenting/uncommenting from this step.

To test the gate chevron LEDs, method 1 (Dan's method): open main.py and comment out `stargate_control.quick_calibration()`, and the entire Web Control section. Uncomment `light_control.cycle_chevrons()`. Make note of what order the chevrons light up, then open config.py and follow the instructions for figuring out the chevron lighting order. Update the array with your results. When done, undo your main.py commenting/uncommenting from this step.

To test the gate chevron LEDs, method 2 (Jeremy's method): open main.py and comment out `stargate_control.quick_calibration()`, but leave the Web Control section active. Run the program (`sudo python3 main.py`), then on your Pi's attached touch-screen monitor, double tap on the StargateCommand.sh script created earlier. (If prompted with a dialog box, choose "Execute"). This will open a full-screen web browser with the dialing interface. Scroll to the bottom of the page and tap the "Testing / Debug" button. From this new page, you can turn on individual chevron LEDs, as well as the ramp LEDs and the calibration LED. I found this to be VERY useful when figuring out the LED wiring order. You can also spin the gate motor, lock/unlock the top chevron, and run the motor drive test from earlier. When finished, press Control+C to stop the program, and then undo all the commenting/uncommenting from this step.

To test your LED and LDR calibration, open main.py and uncomment the "LDR TEST" section below the Web Control logic. You can leave the Web Control uncommented (or commented, it doesn't matter for this step), and be sure `stargate_control.quick_calibration()` is UN-commented. Run the program (`sudo python3 main.py`) and watch the output values from the LDR; when the gate reaches "home" (the "earth" symbol is at the top chevron), you should see the LDR output spike to a higher number, as the LED light shines through the small hole in the symbol at the bottom of the gate (beneath the ramp). You'll need to adjust your `cal_brightness` value in config.py based on this number. I had to get a different, brighter LED than the one I'd originally used (I hadn't used a bright enough one like Dan had recommended in his parts list), and I also needed to put some black electrical tape shrouding the LDR holder to block ambient light from bleeding in. As usual, once you're done with this step, undo all the commenting/uncommenting in main.py.

Lastly, do a full calibration. Open main.py and uncomment `stargate_control.full_calibration()`, then run the program. This will output some values, which you'll need to add to config.py. The calibration values all start with **cal_**.

Note: if the full calibration fails while first moving the gate to "home" (the `move_home()` function), you may need to temporarily increase the `num_steps_circle` value to something significantly higher, and try again.

When you've gone through all steps and updated config.py to your liking, open main.py and make sure the web control section and `stargate_control.quick_calibration()` are uncommented. Run the program. You can now open the StargateCommand.sh script on your touch-monitor, or on another computer visit to http://stargatepi.local , to control your Stargate.

If you're happy with how the Stargate works, you can now set the program to auto-run:

### Auto-Run

You can use [Daemon tools](https://samliu.github.io/2017/01/10/daemontools-cheatsheet.html) to ensure the Python program runs at boot.

First ensure the Python program isn't running, then execute following commands:

```
sudo apt install daemontools daemontools-run
sudo mkdir /etc/service/stargate
sudo vi /etc/service/stargate/run
```

Enter the following text:

```
#!/bin/bash
cd /home/pi/stargate
exec /usr/bin/python3 main.py
```

Save the file, then execute the following:

```sudo chmod u+x /etc/service/stargate/run```

The Python program should immediately start running. You can now control the Stargate via web browser as soon as the Raspberry Pi boots.

### Auto-launch dialing page on Pi's touch-screen

To automatically launch the dialing web page on your Pi's touch-screen monitor when the Pi boots, do the following:

Check to see if you already have an autostart file:

```ls /home/pi/.config/lxsession/LXDE-pi/autostart```

If you don't, copy the default one as a starting point:

```
mkdir -p /home/pi/.config/lxsession/LXDE-pi/
cp /etc/xdg/lxsession/LXDE-pi/autostart /home/pi/.config/lxsession/LXDE-pi/autostart
```

Now edit it:

```vi /home/pi/.config/lxsession/LXDE-pi/autostart```

and add this line to the bottom (this will execute the script we created in an earlier step)

```@/bin/bash /home/pi/Desktop/StargateCommand.sh```

Reboot your Pi, and the webpage should launch on its attached display automatically!


### Screensaver

If you'd like to enable a Stargate Command screensaver (I downloaded [this video](https://www.youtube.com/watch?v=ufjKYaq2hp4) as an mp4), do the following steps:

```sudo apt-get install xscreensaver```

Change permissions on this file (already included in your Git download):

```chmod +x /home/pi/stargate/web/VideoScreensaver.sh```

Edit your autostart file:

```vi /home/pi/.config/lxsession/LXDE-pi/autostart```

and add these lines at the end: (the "xscreensaver" line may already be present, and does not need to be added again)

```
@xscreensaver -no-splash
@/home/pi/stargate/web/VideoScreensaver.sh
```

Your complete autostart file should now look something like this:

```
@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@xscreensaver -no-splash
@/bin/bash /home/pi/Desktop/StargateCommand.sh
@/home/pi/stargate/web/VideoScreensaver.sh
```

And, of course, download a video you'd like for the screensaver. You can name it "SGCSpinningLogoAnimation.mp4" and drop it into the "web" folder, or if it's named something else, edit the VideoScreensaver.sh script to use your correct filename.


### That's it!

You're all done! Congratulations! I'm proud of you for sticking with it! Now, enjoy your Stargate!

## Other Helpful links

[Glitch's Stargate on Thingiverse](https://www.thingiverse.com/thing:1603423)

[Glitch's Stargate original circuit diagram](http://www.glitch.org.uk/circuit-diagram/) and [PDF](http://www.glitch.org.uk/wp-content/uploads/Circuit_Diagram_Stargate_Mk2.pdf)

[Glitch's Stargate assembly video](https://www.youtube.com/watch?v=6X2FbyxViao&feature=youtu.be)

[Glitch's Stargate web page](http://www.glitch.org.uk/working-stargate-mk2/)

[Glitch's Stargate electronics FAQ](http://www.glitch.uk/working-stargate-mk2-electronics-faq/)

[Dan's Stargate build](https://www.thingiverse.com/make:495159)

[Dan's original Stargate code](https://github.com/danclarke/WorkingStargateMk2Raspi) (upon which all this is based)

[Dan's Stargate HAT](https://easyeda.com/boogleoogle/Stargate-HAT)

[Mod parts for Stargate](https://www.thingiverse.com/thing:2795518)

[WaveShare monitor instructions](https://www.waveshare.com/w/upload/5/58/7inch_HDMI_LCD_%28H%29_User_Manual.pdf)