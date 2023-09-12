
from . import ota 
BUFFER_SIZE = 8192
 # UUIDs
WDX_SERVICE = "0000FEF6-0000-1000-8000-00805F9B34FB"
WDX_Device_Configuration_Characteristic = "005f0002-2ff2-4ed5-b045-4c7463617865"
WDX_File_Transfer_Control_Characteristic = "005f0003-2ff2-4ed5-b045-4c7463617865"
WDX_File_Transfer_Data_Characteristic = "005f0004-2ff2-4ed5-b045-4c7463617865"
WDX_Authentication_Characteristic   = "005f0005-2ff2-4ed5-b045-4c7463617865"
ARM_Propietary_Data_Characteristic ="e0262760-08c2-11e1-9073-0e8ac72e0001"

#WDXS File List Configuration
WDX_FLIST_HANDLE       = 0   #brief File List handle */
WDX_FLIST_FORMAT_VER   = 1   #brief File List version */
WDX_FLIST_HDR_SIZE     = 7   #brief File List header length */
WDX_FLIST_RECORD_SIZE  = 40  #brief File List record length */

#Size of WDXC file discovery dataset 
DATC_WDXC_MAX_FILES  = 4
#File Transfer Control Characteristic Operations
WDX_FTC_OP_NONE         = 0        
WDX_FTC_OP_GET_REQ      = (1).to_bytes(1,byteorder='little',signed=False)      
WDX_FTC_OP_GET_RSP      = 2      
WDX_FTC_OP_PUT_REQ      = (3).to_bytes(1,byteorder='little',signed=False)      
WDX_FTC_OP_PUT_RSP      = 4       
WDX_FTC_OP_ERASE_REQ    = 5       
WDX_FTC_OP_ERASE_RSP    = 6       
WDX_FTC_OP_VERIFY_REQ   = (7).to_bytes(1,byteorder='little',signed=False)           
WDX_FTC_OP_VERIFY_RSP   = 8     
WDX_FTC_OP_ABORT        = 9     
WDX_FTC_OP_EOF          = 10

WDX_DC_OP_SET           = (2).to_bytes(1,byteorder='little',signed=False)  
WDX_DC_ID_DISCONNECT_AND_RESET = (37).to_bytes(1,byteorder='little',signed=False)

WDX_FILE_HANDLE = (0).to_bytes(2,byteorder='little',signed = False)
WDX_FILE_OFFSET = (0).to_bytes(4,byteorder='little',signed=False)
WDX_FILE_TYPE = (0).to_bytes(1,byteorder='little',signed=False)
maxFileRecordLength = ((WDX_FLIST_RECORD_SIZE * DATC_WDXC_MAX_FILES) \
                    + WDX_FLIST_HDR_SIZE).to_bytes(4,byteorder='little',signed=False)


#------------------------------| MAX32xxx OTA Update task enqueuers |-------------------------------------------
async def max32xxx_ota_task_list(self,task ,client, *args, **kwargs):
    print(f"task: {task}")  
    if task == "max32xxx_ota_start":
        await ota.ota_update_start(self, client, *args, **kwargs)
    if task == "max32xxx_ota_send_file":
        await ota.ota_update_send_file(self, client, *args, **kwargs)
    if task == "max32xxx_ota_verify_file":
        await ota.ota_update_verify_file(self, client, *args, **kwargs)
    if task == "max32xxx_ota_reset_device":
        await ota.ota_update_reset_device(self, client, *args, **kwargs)

def BLE_task_enqueue_max32xxx_ota_start(self,fileName, fileLen, crc32):
    if fileLen == 0 or crc32 == 0:
        self.logger.setLevel(logging.WARNING)
        self.logger.warning("File length or CRC32 is 0, you must select a file first")
        self.logger.setLevel(logging.INFO)
        return
    elif self.is_connected == False:
        self.logger.setLevel(logging.WARNING)
        self.logger.warning("You must connect to a device first")
        self.logger.setLevel(logging.INFO)
        return
    self.ota_file_len = fileLen
    self.ota_file_name = fileName
    task = ("max32xxx_ota_start", [fileName,fileLen,crc32], {})
    try:
        self.async_queue.put_nowait(task)
    except Exception as err:
        self.logger.setLevel(logging.WARNING)
        self.logger.warning(f"Queue is full: {err}")
        self.logger.setLevel(logging.INFO)
        self.logger.info("OTA failed")
        
def BLE_task_enqueue_max32xxx_ota_send_file(self,fileName, fileLen):
    if fileLen == 0 or fileName == None:
        self.logger.setLevel(logging.WARNING)
        self.logger.warning("File length is 0, you must select a file first")
        self.logger.setLevel(logging.INFO)
        return
    elif self.is_connected == False:
        self.logger.setLevel(logging.WARNING)
        self.logger.warning("You must connect to a device first")
        self.logger.setLevel(logging.INFO)
        return
    self.ota_file_len = fileLen
    self.ota_file_name = fileName
    task = ("max32xxx_ota_send_file", [fileName,fileLen], {})
    try:
        self.async_queue.put_nowait(task)
    except Exception as err:
        self.logger.setLevel(logging.WARNING)
        self.logger.warning(f"Queue is full: {err}")
        self.logger.setLevel(logging.INFO)
        self.logger.info("OTA failed")

def BLE_task_enqueue_max32xxx_ota_verify_file(self):
    if self.is_connected == False:
        self.logger.setLevel(logging.WARNING)
        self.logger.warning("Connection lost")
        self.logger.setLevel(logging.INFO)
        return

    task = ("max32xxx_ota_verify_file",[], {})
    try:
        self.async_queue.put_nowait(task)
    except Exception as err:
        self.logger.setLevel(logging.WARNING)
        self.logger.warning(f"Queue is full: {err}")
        self.logger.setLevel(logging.INFO)
        self.logger.info("OTA failed")

def BLE_task_enqueue_max32xxx_ota_reset_device(self):
    if self.is_connected == False:
        self.logger.setLevel(logging.WARNING)
        self.logger.warning("Connection lost")
        self.logger.setLevel(logging.INFO)
        return

    task = ("max32xxx_ota_reset_device",[], {})
    try:
        self.async_queue.put_nowait(task)
    except Exception as err:
        self.logger.setLevel(logging.WARNING)
        self.logger.warning(f"Queue is full: {err}")
        self.logger.setLevel(logging.INFO)
        self.logger.info("OTA failed")

def ota_reset_state_handler(self):
    self.logger.info("OTA update state reset")
    self.ota_in_progress = False
    self.ota_erase_complete = False
    self.ota_file_write_complete = False
    self.ota_file_len = 0
    self.ota_file_name = None
    self.otas_progress_value.emit(0)
    # failed signal simply resets the variable in main.py
    self.device_ota_update_reset.emit(self)