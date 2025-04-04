from sungrowinverter import SungrowInverter
import asyncio
import logging


### If not called from within an async method

# client = SungrowInverter("10.126.77.168")

# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)
# result = loop.run_until_complete(client.async_update())

# #Get a list data returned from the inverter.
# print(client.model)
# print(client.data)


### If called within an async method in your application

# client = SungrowInverter("10.126.77.168")

# client.async_update()

# #Get a list data returned from the inverter.
# print(client.model)
# print(client.data)


#####  Option 3

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
#logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

# Change IP Address (192.168.4.2) to suit your inverter 
client = SungrowInverter("10.126.77.168", timeout=5)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
result = loop.run_until_complete(client.async_update())

#Get a list data returned from the inverter.
if result:
    print(client.data)
else:
    print("Could not connect to inverter")