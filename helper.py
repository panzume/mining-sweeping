import psutil
import sys
PROC_NAME = "Winmine__XP.exe"

# parses input delimited by 0x10
def parse(data: bytes) -> str:
    board = ''
    row = False
    for c in data:
        match c:
            case 0x10:
                if row:
                    board += '\n'
                    row = False
                else:
                    row = True
            # All cases indicate mines in different states
            case (0x8F | 0x8A | 0xCC) if row:
                board += 'x'
            case 0x40 if row:
                board += '_'
            # Indicates number of mines 
            # in order of 1..8 
            case 0x41 if row:
                board += '1'
            case 0x42 if row:
                board += '2'
            case 0x43 if row:
                board += '3'
            case 0x44 if row:
                board += '4'
            case 0x45 if row:
                board += '5'
            case 0x46 if row:
                board += '6'
            case 0x47 if row:
                board += '7'
            case 0x48 if row:
                board += '8'
            case _ if row:
                board += '.'
    return board

# gets pid from process name (we only care about minesweeper here)
def get_pid() -> int:
    pid = None

    for proc in psutil.process_iter():
        if proc.name() == PROC_NAME:
            pid = proc.pid

    if pid is None:
        print(f"Process '{PROC_NAME}' could not be found",file=sys.stderr)
        input()
        sys.exit(1)
    else:
        return pid