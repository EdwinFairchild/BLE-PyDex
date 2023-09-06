from main import *
from elftools.elf.elffile import ELFFile
from pyocd.core.helpers import ConnectHelper
import subprocess
import logging
import time
import sys

from PySide6.QtCore import QThread

class ExtractGlobalVariablesThread(QThread):
    logger = logging.getLogger("PDexLogger")
    symbol_extracted = Signal(str, int )  # Define a signal to emit the variable name and address
    exit_early = False
    ramStart = None
    ramEnd = None
    def __init__(self, filename, table_widget):
        super().__init__()
        self.filename = filename

    def run(self):
        with open(self.filename, 'rb') as file:
            elffile = ELFFile(file)
            # for futuree development
            if elffile.has_dwarf_info():
                dwarfinfo = elffile.get_dwarf_info()
                
            section = elffile.get_section_by_name('.symtab')
            if not section:
                self.logger.info("Symbol table not found")
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
                    if self.ramStart <= address <= self.ramEnd:
                        self.symbol_extracted.emit(name, address)
                    # if exit_early is true then exit the thread
                    if self.exit_early:
                        return
                    # TODO make this a user setting, possibly slider to select sample rate
                    time.sleep(0.005)
            self.logger.info("Finished extracting global variables")



class MonitoringThread(QThread):
    signal_update_variable = Signal(str, object)  # Signal to update the variable value
    monitor_active = False
    exit_early = False
    logger = logging.getLogger("PDexLogger")
    getCoreRegs = False
    core_regs_tuple = Signal(zip)

    def __init__(self, address_dict):
        super().__init__()
        self.address_dict = address_dict #vars_watched_dict from main.py


    def run(self):
        # Save the original stdout
        probe = None
        original_stdout = sys.stdout
        original_stderr = sys.stderr

        session_options = {
            "halt_on_connect": False,
            "connect_mode": "attach",  # Use 'attach' instead of 'under_reset' or other modes
        }
        # Connect to the probe
        try:
            # Replace stdout with a custom stream that logs messages
            # this is needed becasue pyocd prints to stdout
            logger_stream = LoggerStream(self.logger)
            sys.stdout = logger_stream
            sys.stderr = logger_stream
            probe = ConnectHelper.session_with_chosen_probe(blocking= False,return_first=True, target_override="MAX32655", session_options=session_options)
        except Exception as e:
            self.logger.setLevel(logging.WARNING)
            self.logger.warning("Error while connecting to the probe: %s", e)
            self.logger.setLevel(logging.INFO)
            
        finally:
            # Restore the original stdout
            sys.stdout = original_stdout
            sys.stderr = original_stderr
        if probe is None:
            self.logger.info("No probe found!")
            self.logger.info("Monitoring variables ended")
            self.exit_early = False
            monitor_active = False
            # TODO emit signal to update UI monitoring button
            return

        with probe:
            monitor_active = True
            target = probe.target
            target.resume()
            self.print_core_registers(target)
            self.monitor_variables(target, self.address_dict)
           

    def print_core_registers(self, target):
        # Define the list of core registers you want to read
        reg_list = ['r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'r10', 'r11', 'r12', 'sp', 'lr', 'pc', 'xpsr']

        #halt tagert
        target.halt()
        # Get the core registers
        core_registers = target.read_core_registers_raw(reg_list)
        #resume target
        target.resume()
        
        # emite core registers
        regs_tuple = zip(reg_list, core_registers)
        self.core_regs_tuple.emit(regs_tuple)
 
        

    def monitor_variables(self, target, addresses):
        
        try:
            ###########| Main Loop |###########
            while self.exit_early is False:
                for var_name, details in list(addresses.items()):
                    address = details['address']
                    value = target.read32(address)
                    
                    self.signal_update_variable.emit(var_name, value)  # Emitting the signal with the variable name and value
                if self.getCoreRegs is True:
                    self.print_core_registers(target)
                    self.getCoreRegs = False
                time.sleep(0.010)  # Adjust the refresh rate as needed
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
            monitor_active = False
            
        
    def mass_erase(self):
        pass


class LoggerStream:
    def __init__(self, logger):
        self.logger = logger

    def write(self, message):
        # Make sure not to log empty messages (like newlines)
        if message.strip():
            self.logger.info(message)

    def flush(self):
        pass