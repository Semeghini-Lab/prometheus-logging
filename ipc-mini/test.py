from ipc_mini_manager import *

dm = IPCMiniManager('192.168.0.104')
print(dm.get_pressure())
print(dm.get_current())
print(dm.get_voltage())