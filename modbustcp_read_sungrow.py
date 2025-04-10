from sungrowinverter import SungrowInverter
import asyncio
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

client = SungrowInverter("10.126.77.168", timeout=10)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

try:
    result = loop.run_until_complete(client.async_update())
    if result:
        print("Data retrieved successfully:")
        print(client.data)
        if "external_power" in client.data:
            print("External power: ", client.data["external_power"])
        else:
            print("Key 'external_power' not found in client.data")
    else:
        print("Could not connect to inverter")
except Exception as e:
    logging.error(f"Error during async_update: {e}")



