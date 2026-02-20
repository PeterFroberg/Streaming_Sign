import wifi
import socketpool
import ssl
import time
import ipaddress

from wifi_config import (
    SSID,
    PASSWORD,
    USE_DHCP,
    STATIC_IP_ADDRESS,
    SUBNET_MASK,
    GATEWAY_IP_ADDRESS,
    DNS_IP_ADDRESS,
)

_pool = None
_ssl_context = None


def connect(timeout=20):
    global _pool, _ssl_context

    print("Connecting to Wi-Fi...")
    print("DHCP mode:", USE_DHCP)

    try:
        # Disconnect first (important for reconnects)
        try:
            wifi.radio.stop_station()
        except Exception:
            pass

        # Start station mode
        wifi.radio.start_station()

        # ✅ STATIC IP CONFIG
        if not USE_DHCP:
            print("Setting static IP configuration...")
            print("IP: " + STATIC_IP_ADDRESS)
            print("SUBNET: " + SUBNET_MASK)
            print("GATEWAY: " + GATEWAY_IP_ADDRESS)
            print("DNS: " + DNS_IP_ADDRESS)

            wifi.radio.set_ipv4_address(
                ipv4=ipaddress.ip_address(STATIC_IP_ADDRESS),
                netmask=ipaddress.ip_address(SUBNET_MASK),
                gateway=ipaddress.ip_address(GATEWAY_IP_ADDRESS),
                ipv4_dns=ipaddress.ip_address(DNS_IP_ADDRESS),
            )

        # Connect to AP
        wifi.radio.connect(SSID, PASSWORD)

    except Exception as e:
        print("WiFi connection failed:", e)
        return False

    # Wait for IP
    start = time.monotonic()

    while not wifi.radio.ipv4_address:
        if time.monotonic() - start > timeout:
            print("WiFi timeout")
            return False

        time.sleep(0.5)

    print("WiFi connected!")
    print("IP:", wifi.radio.ipv4_address)

    # Create shared networking objects
    _pool = socketpool.SocketPool(wifi.radio)
    _ssl_context = ssl.create_default_context()

    return True


# ===== Shared networking access =====

def get_socketpool():
    return _pool


def get_ssl_context():
    return _ssl_context
