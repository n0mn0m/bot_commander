## About

This project contains `python` scripts and `cron` task for operating a Roomba
615 locally or remotely.

- `sms_listener.py` runs a web server that monitors a [Twilio](https://www.twilio.com/docs/sms/quickstart/python#allow-twilio-to-talk-to-your-flask-application)
end point waiting for a message to send a start signal to a connected
device (in my scenario a Roomba 615).

- `button_listener.py` is meant for use with an Adafruit [RFM LoRa](https://www.adafruit.com/product/3179)
 shield.

- `code.py` is the application that runs on the Adafruit Feather listening for different signals to process
and send to the Roomba Open Interface.

- `crontab.bak` is a backup of my `crontab` setup that starts the services
on the RaspberryPi Zero W after reboot.

- `requirements.txt` are the packages that the virtual environment requires
for the scripts above to run.

### Notes

This is currently built and running with Python 3.7 and Raspbian.


### Hardware

[Adafruit Feather](https://www.adafruit.com/product/3178) connected to the Roomba
and listening for the signal to send the Roomba the start command.

[Raspberry Pi Zero W](https://www.adafruit.com/product/3708) running the endpoint
that the Twilio webhook is connected to and hosting the bonnet where physical
buttons can be used to issue commands to the Roomba.

[Pi LoRa bonnet](https://www.adafruit.com/product/4074) provides the Pi with
LoRa send/receive functionality, an OLED screen and buttons.

### Acknowledgement

Thank you to the team at Adafruit for building the hardware and CircuitPython
ecosystem.

Referenced docs, code and demos

- [Pi LoRa](https://learn.adafruit.com/lora-and-lorawan-radio-for-raspberry-pi)
- [M0 LoRa](https://learn.adafruit.com/adafruit-feather-m0-radio-with-lora-radio-module)
- [Roomba Open Interface](https://www.irobotweb.com/~/media/MainSite/PDFs/About/STEM/Create/iRobot_Roomba_600_Open_Interface_Spec.pdf)
