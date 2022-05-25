import os
import ctypes
from datetime import datetime, timedelta
import socket
import psutil
import math

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

print(f"\t\t>{user}")
print("   ______\t" + f"host\t\t-> {host}")
print("  / ____/\t" + f"uptime\t\t-> {uptime}")
print(" / /     \t" + f"local ip\t-> {ip}")
print("/ /___   \t" + f"cpu usage\t-> {cpu}% \t\t{cpu_bar}")
print("\____/   \t" + f"mem usage\t-> {mem}\t{mem_bar}")