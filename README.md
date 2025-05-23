# Modbus Register Polling Scripts

This repository contains Python scripts for polling Modbus registers using the `pyModbusTCP` library. The scripts are designed to handle Modbus communication efficiently, with options for multithreading (modbustcp_read_satec4.py) and multiple clients (modbustcp_multiple_clients.py).

---

## Table of Contents
- [Overview](#overview)
- [Requirements](#requirements)
- [Features](#features)
  - [modbustcp_read_satec4.py](#modbustcp_read_satec4py)
  - [modbustcp_multiple_clients.py](#modbustcp_multiple_clientspy)
- [Installation](#installation)
- [SpeedResults](#speedresults)

---

## Overview

The scripts in this repository allow you to:
- Poll Modbus registers from a Modbus server.
- Use multithreading to improve performance.
- Use multiple Modbus clients to distribute the workload. The number of clients to be discussed with Konstantinos and the team.
- Run the polling process either once or continuously. This need has to be discussed with Konstantinos and the team.

---

## Requirements

- Python 3.10 or higher
- `pyModbusTCP` library. It can be installed through pip:
  
  ```bash
  pip install pyModbusTCP

---

## Features

### `modbustcp_read_satec4.py`
- Reads Modbus registers using a single client.
- Supports multithreading for parallel register reads.
- No performance gains compared to the serial reading of `modbustcp_read_satec2.py` script.

### `modbustcp_multiple_clients.py`
- Uses multiple Modbus clients to distribute the workload.
- Divides registers into chunks, with each client handling a subset.
- Supports both one-time execution and continuous polling.
- Configurable via command-line arguments.
- 3 or 4 times faster than the rest of the scripts.
- Arguments:
  ```bash
  --file: Path to the file containing register details (default is registers.txt).
  --clients: Number of Modbus clients.
  --continuous: If provided, the script will run continuously. Otherwise once.
  ```

---

## Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:panpcode/modbus.git
   cd modbus
   python modbustcp_multiple_clients.py
   # Example of usage with arguments
   python modbustcp_multiple_clients.py --file registers.txt --clients 5 --continuous


## SpeedResults

1. Script with single client

    ```bash
    panpap@192 modbus % python3 modbustcp_read_satec4.py
    2025-04-09 17:04:56,043 - INFO - Time taken to read all registers: 3.85 seconds
    2025-04-09 17:04:59,416 - INFO - Time taken to read all registers: 3.37 seconds
    2025-04-09 17:05:02,904 - INFO - Time taken to read all registers: 3.49 seconds
    2025-04-09 17:05:06,613 - INFO - Time taken to read all registers: 3.71 seconds
    2025-04-09 17:05:09,985 - INFO - Time taken to read all registers: 3.37 seconds
    2025-04-09 17:05:13,456 - INFO - Time taken to read all registers: 3.47 seconds
    2025-04-09 17:05:16,913 - INFO - Time taken to read all registers: 3.46 seconds
    2025-04-09 17:05:20,389 - INFO - Time taken to read all registers: 3.48 seconds

    Average time to provide output with a single client: 3.52 seconds

2. Script with multiple clients

    ```bash
    panpap@192 modbus % python3 modbustcp_multiple_clients.py --continuous
    2025-04-09 17:00:49,041 - INFO - Time taken to read all registers: 1.21 seconds
    2025-04-09 17:00:49,971 - INFO - Time taken to read all registers: 0.93 seconds
    2025-04-09 17:00:50,913 - INFO - Time taken to read all registers: 0.94 seconds
    2025-04-09 17:00:51,842 - INFO - Time taken to read all registers: 0.93 seconds
    2025-04-09 17:00:52,756 - INFO - Time taken to read all registers: 0.91 seconds
    2025-04-09 17:00:53,737 - INFO - Time taken to read all registers: 0.98 seconds
    2025-04-09 17:00:54,740 - INFO - Time taken to read all registers: 1.00 seconds
    2025-04-09 17:00:55,687 - INFO - Time taken to read all registers: 0.95 seconds
    2025-04-09 17:00:56,725 - INFO - Time taken to read all registers: 1.04 seconds
    ^C2025-04-09 17:00:57,256 - INFO - Terminating script...
    2025-04-09 17:00:57,692 - INFO - Time taken to read all registers: 0.97 seconds
    2025-04-09 17:00:57,692 - INFO - Script stopped and clients were closed.

    Average time to provide output with multiple clients: 0.99 seconds


