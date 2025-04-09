import sys, signal, logging, time
from threading import Lock
from concurrent.futures import ThreadPoolExecutor
from pyModbusTCP.client import ModbusClient

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Modbus client
client = ModbusClient(host='10.126.254.195', port=502, unit_id=1, auto_open=True)
client_lock = Lock()

running = True
def signal_handler(sig, frame):
    global running
    logging.info("Terminating script...")
    running = False

# signal.signal(signal.SIGINT, signal_handler)
# signal.signal(signal.SIGTERM, signal_handler)

# Input: .txt file
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

# Two functions / options:
#   1. Get the file path from an argument
#   2. Use a default local file named 'registers.txt'
file_path = sys.argv[1] if len(sys.argv) > 1 else 'registers.txt'
registers = load_registers_from_file(file_path)

# Function to read and print register values
def read_and_print_register(reg):
    address = reg[0]
    name = reg[1]
    scale = reg[2]
    unit = reg[3]

    with client_lock: 
        if not client.is_open:
            if not client.open():
                logging.error("Unable to connect to Modbus server.")
                return

        value = client.read_input_registers(address, 1)

    if value:
        real_value = value[0] * scale
        logging.info(f'Register {address}: {name} value: {real_value} {unit}')
    else:
        logging.error(f'Unable to read register {address}')

# Read registers in parallel
def get_registers_in_parallel():
    with ThreadPoolExecutor(max_workers=10) as executor: # Limit to 10 threads | adjust as needed based on our infra
        executor.map(read_and_print_register, registers)

if __name__ == "__main__":

    # comment out the while for 1 execution
    while running:

        start_time = time.time() 
        get_registers_in_parallel()
        end_time = time.time()

        elapsed_time = end_time - start_time
        logging.info(f"Time taken to read all registers: {elapsed_time:.2f} seconds")

        # logging.info("Script has stopped.")