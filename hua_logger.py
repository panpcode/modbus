import sys
import logging
from pyModbusTCP.client import ModbusClient

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

MODBUS_IP = '10.126.77.168'
MODBUS_PORT = 502
UNIT_ID = 1

# Function to load registers from a file
def load_registers_from_file(file_path):
    registers = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line.strip():
                    parts = line.strip().split(',')
                    if len(parts) != 4:
                        logging.warning(f"Invalid line format: {line.strip()}")
                        continue
                    address = int(parts[0])
                    name = parts[1]
                    scale = float(parts[2])
                    unit = parts[3]
                    registers.append([address, name, scale, unit])
    except FileNotFoundError:
        logging.error(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except ValueError as e:
        logging.error(f"Error parsing file '{file_path}': {e}")
        sys.exit(1)
    return registers

# Function to read and print register values
def read_and_print_register(client, reg):
    address = reg[0]
    name = reg[1]
    scale = reg[2]
    unit = reg[3]

    if not client.is_open:
        if not client.open():
            logging.error("Unable to connect to Modbus server.")
            return

    value = client.read_holding_registers(address, 1)
    if value:
        real_value = value[0] * scale
        logging.info(f'Register {address}: {name} value: {real_value} {unit}')
    else:
        logging.error(f'Unable to read register {address}')

if __name__ == "__main__":

    file_path = 'hua-registers.txt'
    registers = load_registers_from_file(file_path)

    client = ModbusClient(host=MODBUS_IP, port=MODBUS_PORT, unit_id=UNIT_ID, auto_open=True)

    for reg in registers:
        read_and_print_register(client, reg)

    client.close()