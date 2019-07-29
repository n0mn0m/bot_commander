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

LOG_FORMAT = '%(asctime)s:%(levelname)s:%(message)s'
logging.basicConfig(filename="/home/pi/logs/sms.log", level=logging.INFO, format=LOG_FORMAT, datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger(__name__)

# Initialize and setup
i2c = busio.I2C(board.SCL, board.SDA)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3c)
display.fill(0)
display.show()

# Initialize LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 433.0)
rfm9x.tx_power = 23

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def sms_start_roomba():
    """
    When a message is received determine which
    signal to send  the Roomba and reply
    to the sender.
    """

    txt = request.values.get("Body").lower()
    logger.info("Command received %s", txt)

    if txt == "start":
        msg = "Starting the Roomba."
        cmd = bytes("1","ascii")
    elif txt == "halt":
        msg = "Stopping the Roomba."
        cmd = bytes("0","ascii")
    elif txt == "dock":
        msg = "Roomba beginning to dock."
        cmd = bytes("2","ascii")
    else:
        msg = "Unknown command. Continuing."
        cmd = None

    logger.info(f"{msg} Command sent to Roomba: {cmd}")

    display.fill(0)
    display.show()
    display.text(msg, 25, 15, 1)
    display.show()

    if cmd:
        rfm9x.send(cmd)

    resp = MessagingResponse()
    resp.message(msg)

    return str(resp)

if __name__ == "__main__":
    while True:
        try:
            display.fill(0)
            display.show()
            display.text("LoRa Flask starting.", 25, 15, 1)
            display.show()

            logger.info("Starting flask app.")
            app.run(debug=False)
        except BaseException as e:
            logger.exception(e)
            pass

