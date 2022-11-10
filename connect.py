import board
import neopixel
from adafruit_pixel_framebuf import PixelFramebuffer, VERTICAL

def connect() -> tuple[neopixel.NeoPixel, PixelFramebuffer, tuple[int, int]]: 
    pixel_width = 16
    pixel_height = 16

    pixel_pin = board.GP28_A2 # doesnt appear in autocomplete. is this correct?
    board.USB_VBUS

    pixels = neopixel.NeoPixel(
        pixel_pin,
        pixel_width * pixel_height,
        brightness=0.1,
        auto_write=False,
    )

    pixel_framebuf = PixelFramebuffer(
        pixels,
        pixel_width,
        pixel_height,
        orientation = VERTICAL,
        alternating = True, # apparently default?
    )
    
    return pixels, pixel_framebuf, (pixel_width, pixel_height)
