from main import *
from elftools.elf.elffile import ELFFile

# def extract_global_variables(filename):
#     with open(filename, 'rb') as file:
#         elffile = ELFFile(file)

#         section = elffile.get_section_by_name('.symtab')
#         if not section:
#             print("Symbol table not found")
#             return

#         for symbol in section.iter_symbols():
#             if symbol['st_info']['bind'] == 'STB_GLOBAL' and symbol['st_shndx'] != 'SHN_UNDEF':
#                 name = symbol.name
#                 address = symbol['st_value']
#                 print(f"Global Variable Name: {name} | Address: {hex(address)}")
# def extract_global_variables(filename, table_widget: QTableWidget):
#     with open(filename, 'rb') as file:
#         elffile = ELFFile(file)

#         section = elffile.get_section_by_name('.symtab')
#         if not section:
#             print("Symbol table not found")
#             return

#         for symbol in section.iter_symbols():
#             if symbol['st_info']['bind'] == 'STB_GLOBAL' and symbol['st_shndx'] != 'SHN_UNDEF':
#                 name = symbol.name
#                 address = hex(symbol['st_value'])

#                 # Create a new row in the table
#                 row_position = table_widget.rowCount()
#                 table_widget.insertRow(row_position)

#                 # Add name and address to the new row
#                 table_widget.setItem(row_position, 0, QTableWidgetItem(name))
#                 table_widget.setItem(row_position, 1, QTableWidgetItem(address))
#                 print(f"Global Variable Name: {name} | Address: {address}")

# # Replace this with your ELF file path
# elf_file_path = '/home/eddie/projects/ADI-Insight/BLE_dats/build/max32655.elf'
# extract_global_variables(elf_file_path)
