from main import *
from . import max32xxx_ota
import asyncio
import time
import zlib

blocksize = 0
delayTime = 0.005

#--------------------| Start OTA Update   |---------------------------------------------------------------
async def ota_update_start( self, client,fileName, fileLen,crc32):       
    global blocksize
    global delayTime
    svc = client.services.get_service(max32xxx_ota.WDX_SERVICE)
    if svc == None:
        self.logger.info("WDX service not found")
        return
    #determine block size depending on MTU size
    wdx_data_char = svc.get_characteristic(max32xxx_ota.WDX_File_Transfer_Control_Characteristic)
    #determine mtu size and subtract 4 to fit the address 
    #and another 4 just because
    blocksize = wdx_data_char.max_write_without_response_size - 8
    if blocksize > 224:
        blocksize = 224
    else :
        blocksize = 120
                    
    self.logger.info(f"MTU size: {wdx_data_char.max_write_without_response_size}")
    self.logger.info(f"blocksize: {blocksize}")
    
    try:
        
        resp = 1
        #--------------------| Enable required notifications directly|---------------------
        # cant enqueue a task from within a task
        await self.notifyCallback(client,max32xxx_ota.ARM_Propietary_Data_Characteristic, True)
        await self.notifyCallback(client,max32xxx_ota.WDX_Device_Configuration_Characteristic, True)
        await self.notifyCallback(client,max32xxx_ota.WDX_File_Transfer_Control_Characteristic, True)
        await self.notifyCallback(client,max32xxx_ota.WDX_File_Transfer_Data_Characteristic, True)
        await self.notifyCallback(client,max32xxx_ota.WDX_Authentication_Characteristic, True)

        #--------------------| File discovery |---------------------
        #this is not additioin this is a byte array
        packet_to_send = (max32xxx_ota.WDX_FTC_OP_GET_REQ)   \
                    + (max32xxx_ota.WDX_FILE_HANDLE)   \
                    + (max32xxx_ota.WDX_FILE_OFFSET)   \
                    + (max32xxx_ota.maxFileRecordLength) \
                    + (max32xxx_ota.WDX_FILE_TYPE)
        
        self.logger.info("sent discovery: " + str(list(packet_to_send)))
        resp = await client.write_gatt_char(max32xxx_ota.WDX_File_Transfer_Control_Characteristic, bytearray(packet_to_send), response = True)
        while resp != None:
            await asyncio.sleep(delayTime)
        #--------------------| send header |---------------------
        #get file len and crc
        #crc32 = self.get_crc32(self.updateFileName)
        file_len_bytes = (fileLen).to_bytes(4,byteorder='little',signed=False)
        #assemble packet and send
        packet_to_send = file_len_bytes + (crc32).to_bytes(4,byteorder='little',signed=False)  
        self.logger.info("sent header: " + str(list(packet_to_send)))         
        resp = 1
        resp = await client.write_gatt_char(max32xxx_ota.ARM_Propietary_Data_Characteristic, bytearray(packet_to_send), response = True)
        while resp != None:
            await asyncio.sleep(delayTime) 
        #--------------------| send put request |---------------------
        # set the ota in progress flag because this will trigger the erase complete handler
        self.ota_in_progress = True
        #assemble packet and send
        packet_to_send = max32xxx_ota.WDX_FTC_OP_PUT_REQ \
                        + (1).to_bytes(2,byteorder='little',signed=False) \
                        + max32xxx_ota.WDX_FILE_OFFSET \
                        + file_len_bytes  \
                        + file_len_bytes  \
                        + max32xxx_ota.WDX_FILE_TYPE
        self.logger.info("sent put req: " + str(list(packet_to_send)))  
        
        await client.write_gatt_char(max32xxx_ota.WDX_File_Transfer_Control_Characteristic, bytearray(packet_to_send))
    except Exception as err:
        self.logger.setLevel(logging.WARNING)
        self.logger.warning(err)
        self.logger.setLevel(logging.INFO)
        self.otasUpdate = False
        self.writeChar = False
        # stop wait for erase complete signal


#--------------------| send file   |---------------------------------------------------------------
async def ota_update_send_file( self, client,fileName, fileLen):      
    global blocksize
    global delayTime
    try:    
        self.ota_file_write_complete = False
        tempLen = fileLen
        self.logger.info("Start of sending file")
        address = 0x00000000  
        with open(fileName, 'rb') as f:
            while client.is_connected:
                try:
                    rawBytes = f.read(blocksize)
                    tempLen = tempLen - len(rawBytes)
                    percent =int((1-(tempLen / fileLen))*100)
                    self.otas_progress_value.emit(percent)
                    if not rawBytes:
                        break
                    nextAddress=(address).to_bytes(4,byteorder='little',signed=False)
                    resp = 1
                    resp = await client.write_gatt_char(max32xxx_ota.WDX_File_Transfer_Data_Characteristic, bytearray(nextAddress + rawBytes))
                    address +=len(rawBytes)
                    while resp != None:
                        await asyncio.sleep(delayTime)
                    #Smaller blocksize indicates we are using OTAS with internal flash which is much slower
                    if blocksize < 220:
                        await asyncio.sleep(0.02)
                    else:
                        await asyncio.sleep(delayTime)
                except Exception as err:
                    self.logger.info(err)
        self.otasUpdate = False
        self.logger.info("End of sending file")  
        time.sleep(1)

    except Exception as err:
        self.logger.setLevel(logging.WARNING)
        self.logger.warning(err)
        self.logger.setLevel(logging.INFO)
        self.otasUpdate = False
        self.writeChar = False

async def ota_update_verify_file( self, client):
    global delayTime
    try:
        #--------------------| send verify file request   |---------------------
        if client.is_connected :
            #assemble packet and send
            #file handle is incremented
            new_WDX_FILE_HANDLE = (1).to_bytes(2,byteorder='little',signed = False)
            packet_to_send = max32xxx_ota.WDX_FTC_OP_VERIFY_REQ +  new_WDX_FILE_HANDLE
            self.logger.info("sent verify req: " + str(list(packet_to_send)))   
            resp = await client.write_gatt_char(max32xxx_ota.WDX_File_Transfer_Control_Characteristic, bytearray(packet_to_send))
            while resp != None:
                await asyncio.sleep(delayTime)
    except Exception as err:
        self.logger.setLevel(logging.WARNING)
        self.logger.warning(err)
        self.logger.setLevel(logging.INFO)
        self.otasUpdate = False
    self.writeChar = False
async def ota_update_reset_device( self, client):
    global delayTime
    try: 
        #--------------------| send reset request   |---------------------
        if client.is_connected :
            # assemble packet and send
            packet_to_send = max32xxx_ota.WDX_DC_OP_SET + max32xxx_ota.WDX_DC_ID_DISCONNECT_AND_RESET 
            self.logger.info("sent reset req: " + str(list(packet_to_send))) 
            resp = 1  
            resp = await client.write_gatt_char(max32xxx_ota.WDX_Device_Configuration_Characteristic, bytearray(packet_to_send))
            while resp != None:
                print("waiting")
                await asyncio.sleep(delayTime)
            
            await asyncio.sleep(delayTime)
            
            self.logger.info("File sent. Firmware update done")
            ## TODO see what is going on with indications 

            self.disconnect_triggered = True
            # TODO make gui clean up method/signal for disconnect event

    except Exception as err:
        self.logger.setLevel(logging.WARNING)
        self.logger.warning(err)
        self.logger.setLevel(logging.INFO)
        self.otasUpdate = False
    self.writeChar = False

def get_crc32(fileName):
   
    max32xxx_ota.BUFFER_SIZE
    with open(fileName, 'rb') as f:
        crc = 0
        fileLen = 0
        while True:
            data = f.read(max32xxx_ota.BUFFER_SIZE)
            fileLen += len(data)
            if not data:
                break
            crc = zlib.crc32(data, crc)
    return [crc,fileLen]

def ota_device_erase_complete_handler(self):
   
    self.ota_erase_complete = True
    self.logger.info("erase complete")