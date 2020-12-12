import time

import adafruit_rfm9x
import board
import busio
import digitalio


def start(bot):
    """
    Start sequence from the Open Interface manual.
    """
    for command in (b"\x80", b"\x83", b"\x87"):
        bot.write(command)


def stop(bot):
    """
    Stop sequence from the Open Interface manual.
    """
    for command in (b"\x85", b"\xAD"):
        bot.write(command)


def keep_alive(brc):
    """
    Pulse the roomba to prevent deep sleep.
    """
    print("Keep alive")
    for i in range(2):
        brc.value = False
        time.sleep(1)
        brc.value = True


def command_received(led):
    for i in range(3):
        time.sleep(0.25)
        led.value = False
        time.sleep(0.25)
        led.value = True
        time.sleep(0.25)
        led.value = False


# base board
print("Intializing board")
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
bot = busio.UART(board.TX, board.RX, baudrate=115200)

# pin out to the BRC pin on the Open Interface
brc = digitalio.DigitalInOut(board.A1)
brc.direction = digitalio.Direction.OUTPUT

# radio
print("Initializing radio")
cs = digitalio.DigitalInOut(board.RFM9X_CS)
reset = digitalio.DigitalInOut(board.RFM9X_RST)
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 433.0)

# external observation
print("Signal to the outside world")
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT
command_received(led)
led.value = True

keep_alive(brc)

elapsed_time = 0

while True:
    elapsed_time += 3

    if elapsed_time > 270:
        keep_alive(brc)
        elapsed_time = 0

    try:
        print("receiving")
        # Time to wait (in seconds) for a packet to be received
        # We could go faster, but in this scenario it's not needed
        packet = rfm9x.receive(0.5)

        if packet is not None:
            packet_txt = str(packet, "ascii")
            print(packet_txt)

            if packet_txt == "0":
                command_received(led)
                led.value = True
                stop(bot)
                led.value = False
            elif packet_txt == "1":
                command_received(led)
                start(bot)
                led.value = True
            else:
                print("\nUnknown packet: {}\n".format(packet_txt))

    # from time to time we can get corrupted packets
    # instead of hanging or completely exiting pass
    # on the errors and restart the loop listening
    # for the next signal
    except:
        elapsed_time = 0
        pass
