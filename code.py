import time
import wifi

import twitch_handler
import neopixel_light_handler
import wifi_handler
import domoticz_handler


# Polling interval (seconds)
POLL_INTERVAL = 5 * 60


# --------------------------------
# Safe sleep (keeps USB responsive)
# --------------------------------
def safe_sleep(seconds):
    for _ in range(seconds):
        time.sleep(1)


# --------------------------------
# Ensure WiFi is connected
# --------------------------------
def ensure_wifi():
    if not wifi.radio.connected:
        print("WiFi disconnected — reconnecting...")
        wifi_handler.connect()


# --------------------------------
# Main loop
# --------------------------------
def main():

    print("Starting Twitch On-Air polling loop...")

    # Initial WiFi connection
    if not wifi_handler.connect():
        print("Could not connect to Wi-Fi.")
        return

    while True:
        try:
            ensure_wifi()

            live = twitch_handler.is_streamer_live()

            if live:
                print("Streamer is LIVE! 🔴")
                neopixel_light_handler.fade_on()
                domoticz_handler.update_stream_status("Streaming")
            else:
                print("Streamer is OFFLINE ⚪")
                neopixel_light_handler.fade_off()
                domoticz_handler.update_stream_status("Offline")

        except Exception as e:
            print("Error checking Twitch:", e)

        print(f"Next check in {POLL_INTERVAL} seconds...")
        safe_sleep(POLL_INTERVAL)


# --------------------------------
# Auto start on boot
# --------------------------------
#if __name__ == "__main__":
main()
