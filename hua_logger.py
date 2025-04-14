from pyModbusTCP.client import ModbusClient
import logging
# import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

MODBUS_IP = '10.100.7.163'
MODBUS_PORT = 502
REGISTER_ADDRESS = 40543
UNIT_ID = 100

client = ModbusClient(host=MODBUS_IP, port=MODBUS_PORT, unit_id=UNIT_ID, auto_open=True)

if client.open():
    value = client.read_holding_registers(REGISTER_ADDRESS, 1)
    if value:
        logging.info(f"✅ SUCCESS - Unit ID {UNIT_ID}: Register {REGISTER_ADDRESS + 40001} value = {value[0]}")
    else:
        logging.info(f"❌ No response or error from Unit ID {UNIT_ID}")
    client.close()
else:
    logging.info(f"❌ Could not connect with Unit ID {UNIT_ID}")

print("\nScan complete.")
