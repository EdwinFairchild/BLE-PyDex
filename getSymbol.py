import pyocd
from elftools.elf.elffile import ELFFile
import logging
import time

# Replace 'your_elf_file.elf' with the path to your ELF file
elf_file_path = 'max32655.elf'

# Replace 'your_symbol_name' with the symbol name you want to retrieve the address for
symbol_name = 'testVal'



# Connect to the target with your probe
with pyocd.target.get_device_count() as session:
    if session > 0:
        with pyocd.target.Session() as target:
            try:
                # Load the ELF file onto the target
                target.load_binary(elf_file_path)

                # Get the address of the symbol
                address = target.get_symbol_address(symbol_name)

                if address is not None:
                    logger.info(f"The address of '{symbol_name}' is 0x{address:08X}")
                else:
                    logger.info(f"Symbol '{symbol_name}' not found.")
                
            except Exception as e:
                logger.warning(f"Error while connecting to the probe: {e}")
    else:
        logger.info("No probe found!")

# Rest of your code (variable monitoring, etc.) goes here...
