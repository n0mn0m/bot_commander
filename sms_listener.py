import os
import time
import logging
# Import Blinka Libraries
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
# Import the SSD1306 module.
import adafruit_ssd1306
# Import RFM9x
import adafruit_rfm9x
# App dependencies
from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

logging.basicConfig(filename="/home/pi/sms.log", level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize and setup
i2c = busio.I2C(board.SCL, board.SDA)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3c)

# Clear the display at initialization.
display.fill(0)
display.show()
width = display.width
height = display.height

# Initialize LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 433.0)
rfm9x.tx_power = 23
prev_packet = None

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def sms_start_roomba():
    """
    When we receive a message signal to start the Roomba.
    """

    logger.info("Command received.")
    display.fill(0)
    start_command = bytes("1","utf-8")
    rfm9x.send(start_command)
    logger.info("Starting the roomba")
    display.text('\r\nStarting Roomba!', 25, 15, 1)
    display.show()

    # Start our response
    resp = MessagingResponse()
    resp.message("Starting the Roomba")

    return str(resp)

if __name__ == "__main__":
    while True:
        try:
            logger.info("Starting flask app.")
            app.run(debug=True)
        except BaseException as e:
            logger.exception(e)
            pass

