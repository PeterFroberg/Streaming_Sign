import board
import neopixel
import time
from neopixel_config import (
    LED_PIN,
    NUM_LEDS,
    BRIGHTNESS,
    FADE_STEPS,
    FADE_SPEED,
    NEOPIXEL_ORDER,
    NEOPIXEL_BPP
)

# SK6812 RGB (NOT RGBW)
pixels = neopixel.NeoPixel(
    LED_PIN,
    NUM_LEDS,
    bpp=NEOPIXEL_BPP,
    brightness=1.0,        # we handle brightness manually
    auto_write=False,
    pixel_order=NEOPIXEL_ORDER
)

led_is_on = False   # 🔒 state tracking


# ----------------------------
# HELPERS
# ----------------------------

def apply_brightness(color, factor):
    return (
        int(color[0] * BRIGHTNESS * factor),
        int(color[1] * BRIGHTNESS * factor),
        int(color[2] * BRIGHTNESS * factor),
    )


def set_all(color):
    for i in range(NUM_LEDS):
        pixels[i] = color
    pixels.show()


# ----------------------------
# LIGHT CONTROL
# ----------------------------

def turn_on_all_red(color=(145, 70, 255)):
    global led_is_on

    if led_is_on:
        return

    c = apply_brightness(color, 1.0)
    set_all(c)

    led_is_on = True


def fade_on(color=(145, 70, 255)):
    global led_is_on
    if led_is_on:
        return

    for step in range(FADE_STEPS + 1):
        factor = step / FADE_STEPS
        c = apply_brightness(color, factor)
        set_all(c)
        time.sleep(FADE_SPEED)

    led_is_on = True


def turn_off_all():
    global led_is_on

    if not led_is_on:
        return

    set_all((0, 0, 0))
    led_is_on = False


def fade_off(color=(0, 0, 0)):
    global led_is_on

    if not led_is_on:
        return

    for step in reversed(range(FADE_STEPS + 1)):
        factor = step / FADE_STEPS
        c = apply_brightness(color, factor)
        set_all(c)
        time.sleep(FADE_SPEED)

    turn_off_all()
