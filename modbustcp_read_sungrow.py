# from pymodbus.client.sync import ModbusTcpClient
# import logging
# import time

# # Enable debug logging
# logging.basicConfig(level=logging.DEBUG)

# def read_with_retries(client, address, retries=3, delay=1):
#     for attempt in range(retries):
#         try:
#             logging.info(f"Attempt {attempt + 1} to read address {address}")
#             result = client.read_holding_registers(address, count=1)
#             logging.debug(f"Response: {result}")
#             if result.isError():
#                 raise Exception("Modbus read error")
#             return result
#         except Exception as e:
#             logging.error(f"Error: {e}")
#             if attempt < retries - 1:
#                 time.sleep(delay)
#             else:
#                 raise e

# # Adjust the unit ID and timeout as needed
# client = ModbusTcpClient(host="10.126.77.168", port=502, unit_id=1, timeout=3)
# client.connect()

# try:
#     result = read_with_retries(client, address=100)
#     print(result.registers)
# finally:
#     client.close()

from sungrowinverter import SungrowInverter
import asyncio
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

client = SungrowInverter("10.126.77.168", timeout=5)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
result = loop.run_until_complete(client.async_update())

if result:
    print(client.data)
else:
    print("Could not connect to inverter")