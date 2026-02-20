import wifi
import socketpool
import adafruit_requests
import adafruit_connection_manager

from twitch_config import CLIENT_ID, STREAMER_LOGIN, HELIX_STREAMS_URL
from twitch_auth import get_app_token

# --------------------------------
# Create shared HTTPS session
# --------------------------------
pool = socketpool.SocketPool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
requests = adafruit_requests.Session(pool, ssl_context)


def is_streamer_live():
    print("Checking Twitch stream status for " + STREAMER_LOGIN + "...")

    token = get_app_token()
    if token is None:
        print("No OAuth token available")
        return False

    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": "Bearer " + token,
    }

    url = HELIX_STREAMS_URL + "?user_login=" + STREAMER_LOGIN

    try:
        response = requests.get(url, headers=headers)

        data = response.json()
        response.close()

        # Twitch returns empty list if offline
        if "data" in data and len(data["data"]) > 0:
            print("STREAM IS LIVE")
            return True
        else:
            print("Stream offline")
            return False

    except Exception as e:
        print("Twitch request failed:", e)
        return False
