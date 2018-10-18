import lib.MyUtils as MyUtils
import socket
import threading

free = MyUtils.FreeDevices()
free.add_element("chupelo")

print(free.list_elements())
