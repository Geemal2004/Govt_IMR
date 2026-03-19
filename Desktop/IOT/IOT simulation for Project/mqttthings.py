import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime

# --- ThingsBoard Configuration ---
THINGSBOARD_HOST = "mqtt.thingsboard.cloud" 
PORT = 1883
ACCESS_TOKEN = "3h4tdas1k0v3p7jym918"  # Get this from your Device page in ThingsBoard
TOPIC = "v1/devices/me/telemetry"          # This is the required topic for TB

# Timing Settings
INTERVAL = 5 
DURATION_HOURS = 5
TOTAL_STEPS = (DURATION_HOURS * 3600) // INTERVAL

def on_publish(client, userdata, result):
    print("Data published to ThingsBoard...")

client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)  # TB uses the Token as the Username
client.on_publish = on_publish
# Tell ThingsBoard the device is active via attributes
client.publish("v1/devices/me/attributes", json.dumps({"active": True}))

def generate_tb_data():
    """Generates the telemetry payload for TB"""
    return {
        "temperature": round(4.2 + random.uniform(-0.5, 0.5), 1),
        "humidity": round(65.3 + random.uniform(-2.0, 2.0), 1),
        "shock_g": round(random.uniform(0.05, 0.20), 2),
        "battery_pct": round(87 - (random.random() * 2), 1),
        "latitude": round(1.3521 + random.uniform(-0.001, 0.001), 4),
        "longitude": round(103.8198 + random.uniform(-0.001, 0.001), 4),
        "active": True
    }

def run_simulation():
    try:
        client.connect(THINGSBOARD_HOST, PORT, 60)
        client.loop_start()
        
        print(f"Starting ThingsBoard stream for {DURATION_HOURS} hours...")
        
        for i in range(TOTAL_STEPS):
            data = generate_tb_data()
            client.publish(TOPIC, json.dumps(data))
            
            # Print feedback to console
            print(f"[{i+1}/{TOTAL_STEPS}] Sent: {data['temperature']}°C | Bat: {data['battery_pct']}%")
            
            time.sleep(INTERVAL)
            
    except KeyboardInterrupt:
        print("\nSimulation stopped.")
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    run_simulation()