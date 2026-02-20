import adafruit_requests
import wifi_handler
from domoticz_config import DOMOTICZ_URL, DOMOTICZ_STREAM_CUSTOM_SENSOR_IDX


# Track last sent value (avoid spam)
_last_status = None


def update_stream_status(status):
    """
    status = "Streaming" or "Offline"
    """

    global _last_status

    # Do not send duplicate updates
    if status == _last_status:
        return

    print("Updating Domoticz:", status)

    try:
        pool = wifi_handler.get_socketpool()
        #ssl_context = wifi_handler.get_ssl_context()  #If using HTTPS on the Domoticz Server

        requests = adafruit_requests.Session(pool)

        url = (
            DOMOTICZ_URL
            + "?type=command&param=udevice"
            + "&idx=" + DOMOTICZ_STREAM_CUSTOM_SENSOR_IDX
            + "&svalue=" + status
        )
        print("URL:", url)

        response = requests.get(url)
        response.close()

        _last_status = status
        print("Domoticz updated")

    except Exception as e:
        print("Domoticz update failed:", e)
