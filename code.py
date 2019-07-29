import board
import busio
import digitalio
import adafruit_rfm9x
import time


class OpenInterface:
    def __init__(self, tx_pin, rx_pin, brc_pin, baud_rate=115200):
        self._board = busio.UART(tx_pin, rx_pin, baudrate=baud_rate)
        self._tx_pin = tx_pin
        self._rx_pin = rx_pin
        self._brc_pin = brc_pin
        self._brc_pin.direction = digitalio.Direction.OUTPUT
        self._baud_rate = baud_rate
        self._stopped = True

    def start(self):
        if self._stopped:
            self.wake_up()

        for command in (b"\x80", b"\x83", b"\x87"):
            self._board.write(command)

    def stop(self):
        for command in (b"\x85", b"\xAD"):
            self._board.write(command)
        self._stopped = True

    def wake_up(self):
        for i in range(3):
            self._brc_pin.value = False
            time.sleep(0.5)
            self._brc_pin.value = True
            time.sleep(0.5)
            self._brc_pin.value = False
            time.sleep(0.5)

        self._stopped = False


spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

cs = digitalio.DigitalInOut(board.RFM9X_CS)
reset = digitalio.DigitalInOut(board.RFM9X_RST)

led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT
led.value = True

rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 433.0)

bot = OpenInterface(board.TX, board.RX, digitalio.DigitalInOut(board.A1))
bot.wake_up()


while True:
    # Wait for a packet to be received (up to 0.5 seconds)
    packet = rfm9x.receive(0.5)

    if packet is not None:
        packet_txt = str(packet, "ascii")

        if packet_txt == "0":
            bot.stop()
            led.value = False
        elif packet_txt == "1":
            led.value = False
            bot.start()
            led.value = True
        else:
            print(packet_txt)
