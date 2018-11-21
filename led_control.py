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
    def update_colors(self, top_row, right_column, bottom_row, left_column):
        if len(top_row) + len(right_column) + len(bottom_row) + len(left_column) != len(self.pixels):
            return False

        pixel_index = 0
        for color in top_row:
            self.pixels[pixel_index] = color
            pixel_index += 1

        for color in right_column:
            self.pixels[pixel_index] = color
            pixel_index += 1

        for color in bottom_row:
            self.pixels[pixel_index] = color
            pixel_index += 1

        for color in left_column:
            self.pixels[pixel_index] = color
            pixel_index += 1

        self.pixels.show()  # Update led strip

