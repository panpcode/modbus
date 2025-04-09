import time
from pyModbusTCP.client import ModbusClient

# Initialize Modbus client
c = ModbusClient(host='10.126.254.195', port=502, unit_id=1, auto_open=True)

# Function to read and print a register value
def read_register(address, description, scale=1, unit=''):
    regs = c.read_holding_registers(address, 1)
    if regs:
        real_value = regs[0] * scale
        print(f'{description} (Register {address}) value: {real_value} {unit}')
    else:
        print(f'Unable to read register {address} ({description})')

# Main read loop
while True:
    # Read and print various registers
    read_register(13696, 'Active Power Total', 1, 'kW')
    read_register(14722, 'Active Energy Export', 1, 'kWh')
    read_register(14720, 'Active Energy Import', 1, 'kWh')
    read_register(13324, 'Active Power Phase A', 1, 'kW')
    read_register(13326, 'Active Power Phase B', 1, 'kW')
    read_register(13328, 'Active Power Phase C', 1, 'kW')
    read_register(13700, 'Apparent Power Total', 1, 'kVA')
    read_register(14736, 'Apparent Energy', 1, 'kVAh')
    read_register(14744, 'Apparent Energy Export', 1, 'kVAh')
    read_register(14742, 'Apparent Energy Import', 1, 'kVAh')
    read_register(13336, 'Apparent Power Phase A', 1, 'kVA')
    read_register(13338, 'Apparent Power Phase B', 1, 'kVA')
    read_register(13340, 'Apparent Power Phase C', 1, 'kVA')
    read_register(13828, 'Frequency', 0.01, 'Hz')
    read_register(13318, 'Current Phase A', 0.01, 'A')
    read_register(13320, 'Current Phase B', 0.01, 'A')
    read_register(13322, 'Current Phase C', 0.01, 'A')
    read_register(13826, 'Neutral Current', 0.01, 'A')
    read_register(243, 'Current Scale', 0.1, 'A')
    read_register(13354, 'Current THD Phase A', 0.1, '%')
    read_register(13356, 'Current THD Phase B', 0.1, '%')
    read_register(13358, 'Current THD Phase C', 0.1, '%')
    read_register(13360, 'K Factor Phase A', 0.1, '-')
    read_register(13362, 'K Factor Phase B', 0.1, '-')
    read_register(13364, 'K Factor Phase C', 0.1, '-')
    read_register(13342, 'Power Factor Phase A', 0.001, '-')
    read_register(13344, 'Power Factor Phase B', 0.001, '-')
    read_register(13346, 'Power Factor Phase C', 0.001, '-')
    read_register(13702, 'Power Factor Total', 0.001, '-')
    read_register(13698, 'Reactive Power Total', 1, 'kVar')
    read_register(14730, 'Reactive Energy Export', 1, 'kVarh')
    read_register(14728, 'Reactive Energy Import', 1, 'kVarh')
    read_register(14756, 'Reactive Energy Q1', 1, 'kVArh')
    read_register(14758, 'Reactive Energy Q2', 1, 'kVArh')
    read_register(14760, 'Reactive Energy Q3', 1, 'kVArh')
    read_register(14762, 'Reactive Energy Q4', 1, 'kVArh')
    read_register(13330, 'Reactive Power Phase A', 1, 'kVar')
    read_register(13332, 'Reactive Power Phase B', 1, 'kVar')
    read_register(13334, 'Reactive Power Phase C', 1, 'kVar')
    read_register(13312, 'Voltage Phase A', 1, 'V')
    read_register(13372, 'Voltage Phase AB', 1, 'V')
    read_register(13314, 'Voltage Phase B', 1, 'V')
    read_register(13374, 'Voltage Phase BC', 1, 'V')
    read_register(13316, 'Voltage Phase C', 1, 'V')
    read_register(13376, 'Voltage Phase CA', 1, 'V')
    read_register(242, 'Voltage Scale', 1, 'V')
    read_register(13348, 'Voltage THD Phase A', 0.1, '%')
    read_register(13350, 'Voltage THD Phase B', 0.1, '%')
    read_register(13352, 'Voltage THD Phase C', 0.1, '%')

    # Sleep 2s before next polling
    time.sleep(2)