import time
import busio
import logging
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_ssd1306
import adafruit_rfm9x

logging.basicConfig(filename="/home/pi/sms.log", level=logging.INFO)
logger = logging.getLogger(__name__)

i2c = busio.I2C(board.SCL, board.SDA)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3c)

# Configure LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 433.0)
rfm9x.tx_power = 23
prev_packet = None

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

while True:
    try:
        packet = None
        display.fill(0)
        display.text('RasPi LoRa', 35, 0, 1)

        if not start_button.value:
            logger.info("Starting bot.")
            display.fill(0)
            start = bytes("1","utf-8")
            rfm9x.send(start)
            display.text('\r\nStarting!', 25, 15, 1)
        elif not stop_button.value:
            logger.info("Stopping bot.")
            display.fill(0)
            stop = bytes("0","utf-8")
            rfm9x.send(stop)
            display.text('\r\nStopping!', 25, 15, 1)
        elif not dock_button.value:
            logger.info("Docking bot.")
            display.fill(0)
            dock = bytes("2","utf-8")
            rfm9x.send(dock)
            display.text('\r\nDocking!', 25, 15, 1)

        display.show()
        time.sleep(0.1)
    except BaseException as e:
        logger.exception(e)
        pass
