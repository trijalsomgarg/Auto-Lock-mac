import asyncio
from bleak import BleakScanner

async def find_devices():
    print("Scanning for Bluetooth devices...")

    devices = await BleakScanner.discover(
        timeout=15,
        return_adv=True
    )

    for address, (device, advertisement) in devices.items():
        print("----------------------------")
        print("Name:", device.name)
        print("ID:", device.address)
        print("Signal:", advertisement.rssi)

asyncio.run(find_devices())