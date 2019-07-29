import time
import busio
import logging
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_ssd1306
import adafruit_rfm9x

LOG_FORMAT = '%(asctime)s:%(levelname)s:%(message)s'
logging.basicConfig(filename="/home/pi/logs/button.log", level=logging.INFO, format=LOG_FORMAT, datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger(__name__)

i2c = busio.I2C(board.SCL, board.SDA)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3c)

# Configure LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 433.0)
rfm9x.tx_power = 23

start_button = DigitalInOut(board.D5)
start_button.direction = Direction.INPUT
start_button.pull = Pull.UP

stop_button = DigitalInOut(board.D6)
stop_button.direction = Direction.INPUT
stop_button.pull = Pull.UP

dock_button = DigitalInOut(board.D12)
dock_button.direction = Direction.INPUT
dock_button.pull = Pull.UP

logger.info("Starting application")

display.fill(0)
display.text('RasPi LoRa', 35, 0, 1)
display.show()

while True:
    try:
        if not start_button.value:
            msg = "Starting Roomba."
            logger.info(msg)
            rfm9x.send(bytes("1","ascii"))
            display.fill(0)
            display.text(msg, 25, 15, 1)
        elif not stop_button.value:
            msg = "Stopping Roomba."
            logger.info(msg)
            rfm9x.send(bytes("0","ascii"))
            display.fill(0)
            display.text(msg, 25, 15, 1)
        elif not dock_button.value:
            msg = "Docking Roomba."
            logger.info(msg)
            rfm9x.send(bytes("2","ascii"))
            display.fill(0)
            display.text(msg, 25, 15, 1)

        display.show()
        # Be careful how often this refreshes to give time for sms to process.
        # Switching buttons to interupt instead of poll could help resolve
        # this conflict.
        time.sleep(3)
    except BaseException as e:
        logger.exception(e)
        pass
