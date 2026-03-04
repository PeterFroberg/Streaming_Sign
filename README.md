# 📡 TwitchSign — Live Streaming Indicator Sign

A wall-mountable illuminated sign that automatically lights up when your favourite Twitch streamer goes live. Built around an **Adafruit QT Py ESP32-S3**, two **NeoPixel 8-LED sticks**, and a 3D printed enclosure with swappable face plates.

🖨️ **3D model files & print settings: [MakerWorld](https://makerworld.com)**

---

## ✨ Features

- **Automatic Twitch detection** — polls the Twitch API and lights up the moment a streamer goes live
- **Two interchangeable face plates** — swap between **"STREAMING"** and **"ON AIR"** fronts depending on your style
- **Full RGB illumination** — 16 NeoPixel LEDs give rich, vibrant colour visible across a room
- **Smooth fade effect** — LEDs fade in and out gracefully when the stream state changes
- **Wall-mountable enclosure** — clean, compact box that sits flush against the wall
- **Optional Domoticz integration** — report live/offline state to your home automation system
- **Modular code structure** — separate handlers and config files for every component

---

## 🛒 Bill of Materials

| Component | Qty | Notes |
|-----------|-----|-------|
| Adafruit QT Py ESP32-S3 WiFi Dev Board | 1 | Main microcontroller |
| NeoPixel Stick — 8 × 5050 RGB LED (51mm) | 2 | Daisy-chained for 16 LEDs |
| 3D Printed Enclosure (back box) | 1 | See MakerWorld for files |
| 3D Printed Face Plate — "STREAMING" | 1 | Interchangeable front |
| 3D Printed Face Plate — "ON AIR" | 1 | Interchangeable front |
| USB-C cable + USB power supply | 1 | Power |

---

## 🔌 Wiring

Each NeoPixel stick has pads on both sides:

```
RIGHT side (input):   GND · VDC · DIN · GND
LEFT side  (output):  GND · VDC · DOUT · GND
```

### Connection overview

Physical layout left to right: **NeoPixel Stick 2 → NeoPixel Stick 1 → QT Py ESP32-S3**

```
NeoPixel Stick 2              NeoPixel Stick 1             QT Py ESP32-S3
┌────────────────────┐       ┌─────────────────────┐         ┌────────┐
│  LEFT       RIGHT  │       │  LEFT       RIGHT   │         │        │
│                    │       │                     │         │        │
│  GND     ┌──GND ───┼───────┼─ GND     ┌──GND ────┼─────────┼─ GND   │
│  VDC     │  VDC ───┼───────┼─ VDC     │  VDC ────┼─────────┼─ 5V    │
│  DOUT    │  DIN ───┼───────┼─ DOUT    │  DIN ────┼─────────┼─ A2    │
│  GND     └──GND    │       │  GND     └──GND     │         │        │
└────────────────────┘       └─────────────────────┘         └────────┘
```

### Notes

- The two GND pads on the **right side** of each stick are bridged together with a short wire or solder bridge
- Power and data enter each stick on the **right side** (DIN, VDC) and exit on the **left side** (DOUT, VDC)
- Stick 2's left-side pads (DOUT, VDC, GND) are unused and can be left unconnected

---

## 💻 Software Setup

### Prerequisites

- [CircuitPython](https://circuitpython.org/) installed on the QT Py ESP32-S3
- The following CircuitPython libraries placed in your `lib/` folder:
  - `neopixel`
  - `adafruit_requests`
  - `adafruit_connection_manager`

### Installation

1. Copy all `.py` files to the root of your `CIRCUITPY` drive
2. Edit the config files (see below)
3. Power up — the sign connects to WiFi and starts polling Twitch automatically

---

## ⚙️ Configuration

All configuration lives in dedicated `_config.py` files. You only need to edit these — no changes to the handler or main code files are required.

### `wifi_config.py` — WiFi credentials

```python
WIFI_SSID = "your_wifi_ssid"
WIFI_PASSWORD = "your_wifi_password"
```

### `twitch_config.py` — Twitch API settings

```python
TWITCH_CLIENT_ID = "your_twitch_client_id"
TWITCH_CLIENT_SECRET = "your_twitch_client_secret"
TWITCH_STREAMER = "streamer_username_to_watch"
```

### `neopixel_config.py` — LED hardware & behaviour

```python
import board
import neopixel

LED_PIN        = board.A2     # GPIO pin connected to NeoPixel DIN — change if needed
NUM_LEDS       = 16           # Total LEDs (2 sticks × 8)
BRIGHTNESS     = 0.20         # Max brightness (0.0–1.0)
FADE_STEPS     = 30           # Number of steps in the fade animation
FADE_SPEED     = 0.05         # Delay (seconds) between fade steps
NEOPIXEL_ORDER = neopixel.GRB # Colour order for your LED strip
NEOPIXEL_BPP   = 3            # Bytes per pixel (3 for RGB, 4 for RGBW)
```

The default brightness is intentionally set to `0.20` — clearly visible while keeping power draw and heat low. Raise it if you need more punch.

### `domoticz_config.py` — Domoticz integration *(optional)*

If you use [Domoticz](https://www.domoticz.com/) home automation, the sign can report the streamer's live/offline status to a virtual device.

```python
DOMOTICZ_ENABLED = False           # Set to True to enable
DOMOTICZ_URL     = "http://192.168.x.x:8080"
DOMOTICZ_IDX     = 123             # IDX of your virtual switch in Domoticz
```

Leave `DOMOTICZ_ENABLED = False` to disable — it has no effect on normal operation.

---

### Getting Twitch API Credentials

1. Go to [dev.twitch.tv](https://dev.twitch.tv/) and log in with your Twitch account
2. Click **Register Your Application**
3. Set the OAuth redirect URL to `http://localhost`
4. Copy the **Client ID** and generate a **Client Secret**

The code uses the **Twitch Helix API** with App Access Tokens — no user login or browser required.

---

## 📁 File Structure

```
/
├── code.py                    # Main program loop
├── wifi_config.py             # WiFi credentials              ← edit this
├── wifi_handler.py            # WiFi connection logic
├── twitch_config.py           # Twitch API + streamer name    ← edit this
├── twitch_auth.py             # Twitch OAuth token handling
├── twitch_handler.py          # Stream status polling
├── neopixel_config.py         # LED pin, count, brightness    ← edit if needed
├── neopixel_light_handler.py  # LED control and fade effects
├── domoticz_config.py         # Domoticz settings (optional)  ← edit if needed
└── domoticz_handler.py        # Domoticz reporting logic
```

---

## 🚀 How It Works

1. On boot, the QT Py connects to WiFi via `wifi_handler.py`
2. It authenticates with the Twitch API via `twitch_auth.py` (App Access Token flow)
3. Every 60 seconds, `twitch_handler.py` checks whether the target streamer is live
4. **If live:** `neopixel_light_handler.py` fades the LEDs in to full brightness
5. **If offline:** LEDs fade out and turn off
6. If Domoticz is enabled, `domoticz_handler.py` updates the virtual device state

---

## 📜 License

Hardware design files: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)  
Code: [MIT License](LICENSE)

---

## 🙏 Credits

Built with:
- [Adafruit CircuitPython](https://circuitpython.org/)
- [Twitch Helix API](https://dev.twitch.tv/docs/api/)
- [Domoticz](https://www.domoticz.com/) *(optional integration)*

*Made with ❤️ for the streaming community.*
