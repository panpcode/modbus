import sys, signal, logging, time, argparse
from concurrent.futures import ThreadPoolExecutor
from pyModbusTCP.client import ModbusClient

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

running = True
def signal_handler(sig, frame):
    global running
    logging.info("Terminating script...")
    running = False

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Input: .txt file - we can accept different register files
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

# Divide registers into chunks for multiple clients
def chunk_registers(registers, num_chunks):
    chunk_size = len(registers) // num_chunks
    chunks = [registers[i:i + chunk_size] for i in range(0, len(registers), chunk_size)]
    
    if len(chunks) > num_chunks:
        chunks[-2].extend(chunks[-1])
        chunks = chunks[:-1]
    return chunks

# Function to read and print register values for a specific client
def read_registers_with_client(client, registers):
    for reg in registers:
        address = reg[0]
        name = reg[1]
        scale = reg[2]
        unit = reg[3]

        # continue only when client is available and connected 
        if not client.is_open:
            if not client.open():
                logging.error(f"Client {client.host}:{client.port} unable to connect to Modbus server.")
                return

        try:
            value = client.read_input_registers(address, 1)
            if value:
                real_value = value[0] * scale
                logging.info(f"Client {client.host}:{client.port} - Register {address}: {name} value: {real_value} {unit}")
            else:
                logging.error(f"Client {client.host}:{client.port} - Unable to read register {address}")
        except Exception as e:
            logging.error(f"Error reading register {address} with client {client.host}:{client.port}: {e}")


if __name__ == "__main__":

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Run Modbus register polling.")
    parser.add_argument("--file", type=str, default="registers.txt", help="Path to the registers file.")
    parser.add_argument("--clients", type=int, default=5, help="Number of Modbus clients to use.")
    parser.add_argument("--continuous", action="store_true", help="Run the script continuously.")
    args = parser.parse_args()

    file_path = args.file
    registers = load_registers_from_file(file_path)

    # we can discuss this number based on our needs - actual registers and resources
    num_clients = args.clients
    if num_clients <= 0:
        logging.error("Number of clients must be greater than 0.")
        sys.exit(1)
        
    # dividing registers into chunks for each of the 5 clients
    register_chunks = chunk_registers(registers, num_clients)

    clients = []
    for i in range(num_clients):
        try:
            client = ModbusClient(host='10.126.254.195', port=502, unit_id=1, auto_open=True)
            clients.append(client)
            logging.info(f"Client {i + 1} initialized: Host={client.host}, Port={client.port}, Unit ID={client.unit_id}")
        except Exception as e:
            logging.error(f"Error initializing client {i + 1}: {e}")

    try:
        while running:

            start_time = time.time() 
            # Use ThreadPoolExecutor to handle clients in parallel
            with ThreadPoolExecutor(max_workers=num_clients) as executor:
                executor.map(read_registers_with_client, clients, register_chunks)
            end_time = time.time()  
            elapsed_time = end_time - start_time 
            logging.info(f"Time taken to read all registers: {elapsed_time:.2f} seconds")

            if not args.continuous:
                break

    finally:
        for client in clients:
            client.close()

        logging.info("Script stopped and clients were closed.")