import time
from pyModbusTCP.client import ModbusClient

# Initialize Modbus client
c = ModbusClient(host='10.126.254.195', port=502, unit_id=1, auto_open=True)

# List of registers to read
registers = [
    [13696, 'Active Power Total', 1, 'kW'],
    [14722, 'Active Energy Export', 1, 'kWh'],
    [14720, 'Active Energy Import', 1, 'kWh'],
    [13324, 'Active Power Phase A', 1, 'kW'],
    [13326, 'Active Power Phase B', 1, 'kW'],
    [13328, 'Active Power Phase C', 1, 'kW'],
    [13700, 'Apparent Power Total', 1, 'kVA'],
    [14736, 'Apparent Energy', 1, 'kVAh'],
    [14744, 'Apparent Energy Export', 1, 'kVAh'],
    [14742, 'Apparent Energy Import', 1, 'kVAh'],
    [13336, 'Apparent Power Phase A', 1, 'kVA'],
    [13338, 'Apparent Power Phase B', 1, 'kVA'],
    [13340, 'Apparent Power Phase C', 1, 'kVA'],
    [13828, 'Frequency', 0.01, 'Hz'],
    [13318, 'Current Phase A', 0.01, 'A'],
    [13320, 'Current Phase B', 0.01, 'A'],
    [13322, 'Current Phase C', 0.01, 'A'],
    [13826, 'Neutral Current', 0.01, 'A'],
    [243, 'Current Scale', 0.1, 'A'],
    [13354, 'Current THD Phase A', 0.1, '%'],
    [13356, 'Current THD Phase B', 0.1, '%'],
    [13358, 'Current THD Phase C', 0.1, '%'],
    [13360, 'K Factor Phase A', 0.1, '-'],
    [13362, 'K Factor Phase B', 0.1, '-'],
    [13364, 'K Factor Phase C', 0.1, '-'],
    [13342, 'Power Factor Phase A', 0.001, '-'],
    [13344, 'Power Factor Phase B', 0.001, '-'],
    [13346, 'Power Factor Phase C', 0.001, '-'],
    [13702, 'Power Factor Total', 0.001, '-'],
    [13698, 'Reactive Power Total', 1, 'kVar'],
    [14730, 'Reactive Energy Export', 1, 'kVarh'],
    [14728, 'Reactive Energy Import', 1, 'kVarh'],
    [14756, 'Reactive Energy Q1', 1, 'kVArh'],
    [14758, 'Reactive Energy Q2', 1, 'kVArh'],
    [14760, 'Reactive Energy Q3', 1, 'kVArh'],
    [14762, 'Reactive Energy Q4', 1, 'kVArh'],
    [13330, 'Reactive Power Phase A', 1, 'kVar'],
    [13332, 'Reactive Power Phase B', 1, 'kVar'],
    [13334, 'Reactive Power Phase C', 1, 'kVar'],
    [13312, 'Voltage Phase A', 1, 'V'],
    [13372, 'Voltage Phase AB', 1, 'V'],
    [13314, 'Voltage Phase B', 1, 'V'],
    [13374, 'Voltage Phase BC', 1, 'V'],
    [13316, 'Voltage Phase C', 1, 'V'],
    [13376, 'Voltage Phase CA', 1, 'V'],
    [242, 'Voltage Scale', 1, 'V'],
    [13348, 'Voltage THD Phase A', 0.1, '%'],
    [13350, 'Voltage THD Phase B', 0.1, '%'],
    [13352, 'Voltage THD Phase C', 0.1, '%']
]

# Function to read and print register values
def read_and_print_registers():
    for reg in registers:
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

# Main read loop
while True:
    start_time = time.time() 
    read_and_print_registers()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken to read all registers: {elapsed_time:.2f} seconds")

    # Sleep 2s before next polling
    time.sleep(2)
