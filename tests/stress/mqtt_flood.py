# weaver/tests/stress/mqtt_flood.py
import json
import time
import threading
import random
from paho.mqtt import client as mqtt_client

BROKER = "127.0.0.1"
PORT = 1883
TOPIC = "manakai/soil/stress"
NUM_SIMULATED_NODES = 50
MESSAGES_PER_NODE = 100


def simulate_node(node_id):
    client_id = f"stress-node-{node_id}"

    # Safely bypass linter checks by dynamically building initialization kwargs
    kwargs = {"client_id": client_id}
    if hasattr(mqtt_client, "CallbackAPIVersion"):
        kwargs["callback_api_version"] = getattr(
            mqtt_client, "CallbackAPIVersion"
        ).VERSION2

    client = mqtt_client.Client(**kwargs)

    try:
        client.connect(BROKER, PORT, keepalive=60)
        client.loop_start()

        for _ in range(MESSAGES_PER_NODE):
            # Simulate a standard telemetry packet
            payload = json.dumps(
                {
                    "node": node_id,
                    "moisture": random.uniform(20.0, 80.0),
                    "ts": time.time(),
                }
            )
            client.publish(TOPIC, payload, qos=1)
            time.sleep(0.001)  # Rapid blast

        client.loop_stop()
        client.disconnect()
    except Exception as e:
        print(f"Node {node_id} crashed: {e}")


if __name__ == "__main__":
    print(
        f"Starting flood test: Spawning {NUM_SIMULATED_NODES} nodes "
        f"blasting {MESSAGES_PER_NODE} packets each..."
    )
    start_time = time.time()

    threads = []
    for i in range(NUM_SIMULATED_NODES):
        t = threading.Thread(target=simulate_node, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    duration = time.time() - start_time
    total_msgs = NUM_SIMULATED_NODES * MESSAGES_PER_NODE
    print(
        f"Test finished. Dispatched {total_msgs} messages in "
        f"{duration:.2f} seconds ({total_msgs / duration:.1f} msgs/sec)."
    )
