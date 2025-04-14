import unittest
from unittest.mock import patch, mock_open, MagicMock
from modbustcp_multiple_clients import load_registers_from_file, chunk_registers, read_registers_with_client
from pyModbusTCP.client import ModbusClient

class TestModbusTCPMultipleClients(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data="1,Temperature,0.1,C\n2,Pressure,1.0,Pa\n")
    def test_load_registers_from_file_valid(self, mock_file):
        registers = load_registers_from_file("registers.txt")
        self.assertEqual(len(registers), 2)
        self.assertEqual(registers[0], [1, "Temperature", 0.1, "C"])
        self.assertEqual(registers[1], [2, "Pressure", 1.0, "Pa"])

    @patch("builtins.open", new_callable=mock_open, read_data="1,Temperature,0.1\nInvalidLine\n")
    def test_load_registers_from_file_invalid(self, mock_file):
        with self.assertLogs(level="WARNING") as log:
            registers = load_registers_from_file("registers.txt")
            self.assertEqual(len(registers), 0)
            self.assertIn("Invalid line format", log.output[0])

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_registers_from_file_not_found(self, mock_file):
        with self.assertRaises(SystemExit):
            load_registers_from_file("nonexistent.txt")

    def test_chunk_registers(self):
        registers = [[1, "Temperature", 0.1, "C"], [2, "Pressure", 1.0, "Pa"], [3, "Humidity", 0.5, "%"]]
        chunks = chunk_registers(registers, 2)
        self.assertEqual(len(chunks), 2)
        print(chunks)
        self.assertEqual(chunks[0], [[1, "Temperature", 0.1, "C"]])
        self.assertEqual(chunks[1], [[2, "Pressure", 1.0, "Pa"], [3, "Humidity", 0.5, "%"]])

    @patch.object(ModbusClient, "is_open", new_callable=MagicMock, return_value=True)
    @patch.object(ModbusClient, "read_input_registers", new_callable=MagicMock, return_value=[100])
    def test_read_registers_with_client_success(self, mock_read, mock_is_open):
        client = ModbusClient(host="127.0.0.1", port=502)
        registers = [[1, "Temperature", 0.1, "C"]]
        with self.assertLogs(level="INFO") as log:
            read_registers_with_client(client, registers)
            self.assertIn("Register 1: Temperature value: 10.0 C", log.output[0])

    @patch.object(ModbusClient, "is_open", new_callable=MagicMock, return_value=True)
    @patch.object(ModbusClient, "read_input_registers", new_callable=MagicMock, return_value=None)
    def test_read_registers_with_client_read_fail(self, mock_read, mock_is_open):
        client = ModbusClient(host="127.0.0.1", port=502)
        registers = [[1, "Temperature", 0.1, "C"]]
        with self.assertLogs(level="ERROR") as log:
            read_registers_with_client(client, registers)
            self.assertIn("Unable to read register 1", log.output[0])

if __name__ == "__main__":
    unittest.main()