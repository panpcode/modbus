# import time
import threading

from pyModbusTCP.client import ModbusClient

# Initialize Modbus client
c = ModbusClient(host='10.126.254.195', port=502, unit_id=1, auto_open=True)

# Loading registers from a .txt file
def load_registers_from_file(file_path):
    registers = []

    with open(file_path, 'r') as file:
        for line in file:

            if line.strip():
                parts = line.strip().split(',')
                address = int(parts[0])
                name = parts[1]
                scale = float(parts[2])
                unit = parts[3]
                registers.append([address, name, scale, unit])
    return registers

# Load the registers 
# (!) This can be an input to script in order to accept different register files
registers = load_registers_from_file('registers.txt')

# Function to read and print register values
def read_and_print_register(reg):
    address = reg[0]
    name = reg[1]
    scale = reg[2]
    unit = reg[3]
    
    # Read the register value
    value = c.read_input_registers(address, 1)
    
    if value:
        real_value = value[0] * scale
        print(f'Register {address}: {name} value: {real_value} {unit}')
    else:
        print(f'Unable to read register {address}')


# Read registers in parallel
def get_registers_in_parallel():
    threads = []
    
    # Create a thread for each register
    for reg in registers:
        thread = threading.Thread(target=read_and_print_register, args=(reg,))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()

# Main read loop
while True:
    get_registers_in_parallel()
    
    # Sleep 2s before next polling
    # time.sleep(2)