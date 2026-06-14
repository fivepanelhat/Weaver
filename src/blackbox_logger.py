# weaver/src/blackbox_logger.py
import os
import time
from paho.mqtt import client as mqtt_client

BROKER = os.getenv("MQTT_BROKER", "127.0.0.1")
PORT = int(os.getenv("MQTT_PORT", "1883"))
TOPIC = os.getenv("MQTT_TOPIC", "weaver/logs")
LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), "weaver_blackbox.log")


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(
            f"[BLACK BOX] Successfully connected to broker. Subscribing to: {TOPIC}"
        )
        client.subscribe(TOPIC, qos=1)
    else:
        print(f"[ERROR] Failed to connect, return code {rc}")


def on_message(client, userdata, msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log_payload = msg.payload.decode("utf-8", errors="ignore")
    log_entry = f"[{timestamp}] [{msg.topic}] {log_payload}\n"

    # Write directly to localized rolling file
    try:
        with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
            f.write(log_entry)
        # Mirror out to stdout for terminal viewing
        print(log_entry.strip())
    except IOError as e:
        print(f"[CRITICAL LOG ERROR] Unable to write to disk: {e}")


def run_harvester():
    print("[INIT] Starting Sovereign Black Box logging service...")

    # Safely bypass linter checks by dynamically building initialization kwargs
    kwargs = {}
    if hasattr(mqtt_client, "CallbackAPIVersion"):
        kwargs["callback_api_version"] = getattr(
            mqtt_client, "CallbackAPIVersion"
        ).VERSION2

    client = mqtt_client.Client(**kwargs)

    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(BROKER, PORT, keepalive=60)
        # Keep loop running indefinitely in background
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Stopping Black Box logging service gracefully.")
    except Exception as e:
        print(f"[CRITICAL] Client crashed: {e}")


if __name__ == "__main__":
    run_harvester()
