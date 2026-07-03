import socket
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

class PortStatus(Enum):
    OPEN = "Open"
    CLOSED = "Closed"
    UNRESOLVED = "Could Not Resolve Host"

def check_port(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        result = s.connect_ex((host, port))
        if result == 0:
            return PortStatus.OPEN
        else:
            return PortStatus.CLOSED
        
    except socket.gaierror as e:
        return PortStatus.UNRESOLVED
    finally:
        s.close()
    

#print(check_port("this-does-not-exist-asdf.local", 8000))

def scan_range(host, port_range):
    open_ports = []
    port_dict = {}
    try:
        ip = socket.gethostbyname(host)
    except socket.gaierror:
        return PortStatus.UNRESOLVED
    
    #Insert Executor here:
    with ThreadPoolExecutor(max_workers=100) as executor:
        for x in range(port_range[0], port_range[1] + 1):
            future = executor.submit(check_port, host, x)
            port_dict[future] = x
            
        for future in as_completed(port_dict.keys()):
             status = future.result()
             if status == PortStatus.OPEN:
                  open_ports.append(port_dict[future])
             
            
    return open_ports

