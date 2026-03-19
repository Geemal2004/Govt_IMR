import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime, timedelta

# --- Configuration ---
BROKER = "mqtt.thingsboard.cloud"  # e.g., "broker.hivemq.com" or "localhost"
PORT = 1883
TOPIC = "cargo/telemetry"
DEVICE_ID = "CARGO-ESP32-001"
CONTAINER_ID = "CTR-SG-4472"

# Timing: 5 hours * 3600 seconds / 5 second intervals = 3600 messages
# You asked for 1000 messages, but to fill 5 hours at 5s intervals, 
# you actually need 3600. I will set it to run for the duration.
INTERVAL = 5 
DURATION_HOURS = 5
TOTAL_STEPS = (DURATION_HOURS * 3600) // INTERVAL

client = mqtt.Client()

def connect_mqtt():
    try:
        client.connect(BROKER, PORT, 60)
        print(f"Connected to {BROKER}")
    except Exception as e:
        print(f"Connection failed: {e}")
        exit(1)

def generate_data():
    # Simulating slight movement and sensor fluctuations
    return {
        "device_id": DEVICE_ID,
        "container_id": CONTAINER_ID,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "location": {
            "lat": round(1.3521 + random.uniform(-0.001, 0.001), 4),
            "lon": round(103.8198 + random.uniform(-0.001, 0.001), 4)
        },
        "temperature": round(4.2 + random.uniform(-0.5, 0.5), 1),
        "humidity": round(65.3 + random.uniform(-2.0, 2.0), 1),
        "shock_g": round(random.uniform(0.05, 0.20), 2),
        "door_open": False,
        "battery_pct": max(0, 87 - (random.randint(0, 1) * 0.01)) # Slow drain
    }

def run_simulation():
    connect_mqtt()
    client.loop_start()
    
    print(f"Starting broadcast at {datetime.now().strftime('%H:%M:%S')}")
    
    try:
        for i in range(TOTAL_STEPS):
            data = generate_data()
            payload = json.dumps(data)
            
            client.publish(TOPIC, payload)
            print(f"[{i+1}/{TOTAL_STEPS}] Published: {payload}")
            
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("\nSimulation stopped by user.")
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    run_simulation()