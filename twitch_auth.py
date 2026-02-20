import time
import wifi
import socketpool
import adafruit_requests
import adafruit_connection_manager

from twitch_config import CLIENT_ID, CLIENT_SECRET, TOKEN_URL

# -----------------------------
# Create HTTPS session (CP10 way)
# -----------------------------
pool = socketpool.SocketPool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
requests = adafruit_requests.Session(pool, ssl_context)

# -----------------------------
# Token cache
# -----------------------------
_token = None
_token_expiry = 0


def get_app_token():
    global _token, _token_expiry

    # Reuse token if still valid
    if _token and time.monotonic() < _token_expiry:
        print("Using cached OAuth token")
        return _token

    print("Requesting new Twitch OAuth token...")

    url = (
        TOKEN_URL
        + "?client_id=" + CLIENT_ID
        + "&client_secret=" + CLIENT_SECRET
        + "&grant_type=client_credentials"
    )

    try:
        response = requests.post(url)
        data = response.json()
        response.close()

        _token = data["access_token"]
        expires_in = data["expires_in"]

        # refresh slightly before expiration
        _token_expiry = time.monotonic() + expires_in - 60

        print("OAuth token acquired")
        return _token

    except Exception as e:
        print("OAuth request failed:", e)
        return None
