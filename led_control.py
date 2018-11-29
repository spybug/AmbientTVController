import board
import neopixel

led_pin = board.D18
led_order = neopixel.GRB


class LEDController:
    def __init__(self, horiz_num, vert_num):
        self.horiz_leds = horiz_num
        self.vert_leds = vert_num
        self.total_leds = horiz_num * 2 + vert_num * 2
        self.pixels = neopixel.NeoPixel(led_pin, self.total_leds,
                                        brightness=0.2, auto_write=False, pixel_order=led_order)

    # Update from top left corner
    def update_colors(self, color_buffer):
        if len(color_buffer) != len(self.pixels):
            return False

        pixel_index = 0
        for color in color_buffer:
            self.pixels[pixel_index] = color
            pixel_index += 1

        self.pixels.show()  # Update led strip

    # Turn off all leds
    def stop(self):
        for i in range(len(self.pixels)):
            self.pixels[i] = (0, 0, 0)

        self.pixels.show()


