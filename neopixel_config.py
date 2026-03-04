import board
import neopixel

LED_PIN = board.A2     # change if needed
NUM_LEDS = 16

BRIGHTNESS = 0.20       # max brightness
FADE_STEPS = 30
FADE_SPEED = 0.05
NEOPIXEL_ORDER = neopixel.GRB
NEOPIXEL_BPP = 3