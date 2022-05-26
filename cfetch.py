import os
import ctypes
from datetime import datetime, timedelta
import socket
import psutil
import math

def Main():
    user = os.getlogin()
    uptime = timedelta(seconds=ctypes.windll.kernel32.GetTickCount64() // 1000)
    host = socket.gethostname()
    ip = socket.gethostbyname(host)
    mem = f"{round(psutil.virtual_memory().used / math.pow(1024, 3), 2)}GB / {round(psutil.virtual_memory().total / math.pow(1024, 3), 2)}GB"
    mem_bar = ""
    for x in range(round(psutil.virtual_memory().percent / 10)):
       mem_bar += "█"
    mem_bar = mem_bar.ljust(10, "▒")
    cpu = psutil.cpu_percent(interval=0.1)
    cpu_bar = ""
    for x in range(round(cpu / 10)):
       cpu_bar += "█"
    cpu_bar = cpu_bar.ljust(10, "▒")

    print("    ______\t" + f"user\t\t-> {user}")
    print("   / ____/\t" + f"host\t\t-> {host}")
    print("  / /     \t" + f"uptime\t\t-> {uptime}")
    print(" / /___   \t" + f"local ip\t-> {ip}")
    print(" \____/   \t" + f"cpu usage\t-> {cpu}% \t\t{cpu_bar}")
    print("\t\t" + f"mem usage\t-> {mem}\t{mem_bar}")
    
if __name__ == '__main__':
    Main()