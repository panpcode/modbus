#!/usr/bin/env python3

""" Read 10 holding registers and print result on stdout. """

import time
from pyModbusTCP.client import ModbusClient


#init modbus client
#c = ModbusClient(host='10.102.18.168', port=502, unit_id=1, auto_open=True, debug=True)
c = ModbusClient(host='10.126.78.168', port=502, unit_id=1, auto_open=True)

# Main read loop
while True:
    # Read 1 register at address 40001, store result in regs list
    regs_l = c.read_holding_registers(8193, 2)

    # If success, display registers
    if regs_l:
        print('Register 40001 value: %s' % regs_l[0])
    else:
        print('Unable to read register 40001')

    # Sleep 2s before next polling
    time.sleep(2)
