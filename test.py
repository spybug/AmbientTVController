import board
import neopixel
import time

led_pin = board.D18
led_order = neopixel.GRB


total_leds = 78
#13 x 26 x 13 x 26
pixels = neopixel.NeoPixel(led_pin, total_leds, pixel_order=led_order)


# Turn off all leds
def red():
    global pixels
    for i in range(len(pixels)):
        pixels[i] = (0, 0, 255)

    pixels.show()


if __name__ == "__main__":
    while True:
        red()
        time.sleep(1)