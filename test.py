import board
import neopixel
import time

led_pin = board.D18
led_order = neopixel.GRB


total_leds = 5
pixels = neopixel.NeoPixel(led_pin, total_leds, auto_write=False, pixel_order=led_order)


# Turn off all leds
def red(pixels):
    for i in range(len(pixels)):
        pixels[i] = (0, 255, 0)

    pixels.show()


if __name__ == "__main__":
    while True:
        red(pixels)
        time.sleep(2)
