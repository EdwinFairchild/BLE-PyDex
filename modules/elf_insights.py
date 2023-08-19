from main import *
from elftools.elf.elffile import ELFFile
from pyocd.core.helpers import ConnectHelper
import subprocess
import logging
import time

from PySide6.QtCore import QThread

class ExtractGlobalVariablesThread(QThread):
    logger = logging.getLogger("PDexLogger")
    symbol_extracted = Signal(str, int , str)  # Define a signal to emit the variable name and address
    exit_early = False
    def __init__(self, filename, table_widget):
        super().__init__()
        self.filename = filename
       

    def handle_checkbox_state_change(self, state, var_name, address):
        if state == Qt.Checked:
            self.address_dict[var_name] = address
        else:
            self.address_dict.pop(var_name, None)

    def run(self):
        with open(self.filename, 'rb') as file:
            elffile = ELFFile(file)
            section = elffile.get_section_by_name('.symtab')
            if not section:
                print("Symbol table not found")
                return

            for symbol in section.iter_symbols():
                if symbol['st_info']['bind'] == 'STB_GLOBAL':
                    shndx = symbol['st_shndx']
                    if shndx not in ('SHN_UNDEF', 'SHN_ABS'):
                        shndx = int(shndx)
                        sec = elffile.get_section(shndx)
                        section_name = sec.name if sec else 'UNKNOWN'
                    else:
                        section_name = shndx
                    
                    name = symbol.name
                    address = symbol['st_value']
                    self.symbol_extracted.emit(name, address, section_name)
                    # if exit_early is true then exit the thread
                    if self.exit_early:
                        return
                    time.sleep(0.003)
            self.logger.info("Finished extracting global variables")


class MonitoringThread(QThread):
    signal_update_variable = Signal(str, int)  # Signal to update the variable value
    monitor_active = False
    exit_early = False
    logger = logging.getLogger("PDexLogger")

    def __init__(self, address_dict):
        super().__init__()
        self.address_dict = address_dict


    def run(self):
        session_options = {
            "halt_on_connect": False,
            "connect_mode": "attach",  # Use 'attach' instead of 'under_reset' or other modes
        }
        # Connect to the probe
        probe = ConnectHelper.session_with_chosen_probe(return_first=True, target_override="MAX32655", session_options=session_options)

        if probe is None:
            self.signal_print.emit("No probe found!")
            return

        with probe:
            target = probe.target
            target.resume()
            self.print_core_registers(target)
            self.monitor_variables(target, self.address_dict)
           

    def print_core_registers(self, target):
        pass
        # Define the list of core registers you want to read
        # [...] Implementation here

    def monitor_variables(self, target, addresses):
        previous_values = {key: None for key in addresses}
        try:
            while self.exit_early is False:
                for var_name, details in list(addresses.items()):
                    address = details['address']

                    value = target.read32(address)
                    if value != previous_values[var_name]:
                        previous_values[var_name] = value
                        self.signal_update_variable.emit(var_name, value)  # Emitting the signal with the variable name and value
                time.sleep(0.01)  # Adjust the refresh rate as needed
        except Exception as e:
            self.logger.setLevel(logging.WARNING)
            self.logger.warning("Error while monitoring variables: %s", e)
            self.logger.setLevel(logging.INFO)
        finally:
            # This code will be executed no matter what, even if an exception occurs
            #target.close()  # Replace this with the appropriate method to close the connection to the target
            # You can also add any other cleanup code that needs to be executed here
            self.logger.info("Monitoring variables ended")
            self.exit_early = False
            
        # [...] Implementation here

    def mass_erase(self):
        pass
        # [...] Implementation here

    # Add any additional methods here, as needed