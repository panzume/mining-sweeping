# foreign function interfacing!!
import ctypes
import helper
import sys
import time
import os
import subprocess

# memory region of minesweeper field
BOARD_ADDR = 0x1005360
# memory region of board dimensions
HEIGHT = 0x01005334
WIDTH = 0x1005338
NUM_BYTES = 768 
PROCESS_VM_READ = 0x0010

try:
    i = input("Hide process from task manager - you will need to run as adminstrator to do this: Y/N\n")
    if i == 'Y':
        if getattr(sys, 'frozen', False):
            # If the application is run as a bundle, the PyInstaller bootloader
            # extends the sys module by a flag frozen=True and sets the app 
            # path into variable _MEIPASS'.
            application_path = sys._MEIPASS
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))
        
        pid = helper.get_pid()

        # DLL_Injector courtesy of https://github.com/kernelm0de/ProcessHider
        exec = subprocess.Popen([os.path.join(application_path, "DLL_Injector.exe")], stdin=subprocess.PIPE)
        exec.stdin.write("SAP.exe".encode())
        exec.stdin.close()

    while True:
        pid = helper.get_pid()

        # retrieve the process memory for board width and height
        height_buff = ctypes.create_string_buffer(4)
        width_buff = ctypes.create_string_buffer(4)
        process = ctypes.windll.kernel32.OpenProcess(PROCESS_VM_READ, 0, pid)

        ctypes.windll.kernel32.ReadProcessMemory(process, HEIGHT, height_buff, 4, None)
        ctypes.windll.kernel32.ReadProcessMemory(process, WIDTH, width_buff, 4, None) 

        # expected amount of data to read from the board
        height = int.from_bytes(height_buff.value, "little")
        width = int.from_bytes(width_buff.value, "little")
        n = height * (width + 2)

        # retrieve the process memory for board
        buf = ctypes.create_string_buffer(NUM_BYTES)
        ctypes.windll.kernel32.ReadProcessMemory(process, BOARD_ADDR, buf, NUM_BYTES, None)

        board = helper.parse(buf.value).strip()
        os.system("cls")
        print(f"Minesweeper \nBoard: {height}H x {width}W\n\n{board[:(n - 1)]}")
        
        time.sleep(0.5)
except KeyboardInterrupt:
    sys.exit(0)
except Exception as e:
    print(e)
    input()
    sys.exit(1)