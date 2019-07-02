#! /usr/bin/python3

# geektechstuff Security Python

# modules to import
import socket
import requests
from datetime import datetime

def ip_honey_trap():
    # honey trap to receive data from browser connecting
    # IP Address of device running the trap
    TCP_IP = "192.168.0.11"
    # Port of address to open
    TCP_Port = 45368
    Buffer = 100
    # opens port and listens for a connection to TCP_IP:TCP_Port
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((TCP_IP,TCP_Port))
    s.listen(1)
    conn,addr = s.accept()
    print('Connection address: ',addr," is active")
    # whilst the connecting browser is open it will send date about itself (browser name, operating system etc..)
    while 1:
        data = conn.recv(Buffer)
        if not data:break
        print("Received data: ",data)
        conn.send(data)
        conn.close
    return()

def port_scan_UI():
    # the port scanner with user input
    IP_INPUT = input("What IPv4 address should I connect to: ")
    ports = port_range()
    active_ports =[]
    # goes through all the ports in the port list
    for port in ports:
        remove_flag = 0
        http_address = "http://"+IP_INPUT
        http_address = str(http_address)
        https_address = "https://"+IP_INPUT
        https_address = str(https_address)
        str_port = str(port)
        full_address = http_address+":"+str_port
        full_address = str(full_address)
        full_address2 = https_address+":"+str_port
        full_address2 = str(full_address2)
        # tries to connect to HTTP
        try:
            r = requests.get(full_address)
            print(full_address,r.status_code,"----POTENTIAL WEBSITE-----")
            remove_flag = 1
            active_ports.append(port)
        except:
            print("No connection", full_address)    
        # tries to connect to HTTPS    
        try:
            r2 = requests.get(full_address2)
            print(full_address2,r2.status_code,"----POTENTIAL WEBSITE-----")
            remove_flag = 1
            active_ports.append(port)
        except:
            print("No connection", full_address2)
        # removes any web based ports
        if remove_flag == 1 :
            ports.remove(port)
    # tries to connect via sockets to remaining ports
    for remaining_ports in ports:
        s = socket.socket()
        try:
            s.connect((IP_INPUT,remaining_ports))
            response = s.recv(1024)
            print(IP_INPUT,remaining_ports,response,"-----POTENTIAL OPEN PORT------")
            s.close
            active_ports.append(remaining_ports)
        except:
            print("nothing on port", remaining_ports)
    return()

def port_range():
    # asks user what port range they want to use
    range1 = input("Which port should I start at: ")
    range2 = input("Which port should I stop at: ")
    try:
        range1 = int(range1)
        range2 = int(range2)
    except:
        print("I was expecting integer numbers")
    p_range =list(range(range1,range2))
    return(p_range)

def port_scan_auto(IP_INPUT,START_IP,END_IP):
    # the port scanner with no user input
    START_IP=int(START_IP)
    END_IP=int(END_IP)
    p_range=(list(range(START_IP,END_IP)))
    ports = p_range
    active_ports =[]
    # goes through all the ports in the port list
    for port in ports:
        remove_flag = 0
        http_address = "http://"+IP_INPUT
        http_address = str(http_address)
        https_address = "https://"+IP_INPUT
        https_address = str(https_address)
        str_port = str(port)
        full_address = http_address+":"+str_port
        full_address = str(full_address)
        full_address2 = https_address+":"+str_port
        full_address2 = str(full_address2)
        # tries to connect to HTTP
        try:
            r = requests.get(full_address)
            remove_flag = 1
            active_ports.append(port)
        except:
            print("")
        
              
        # tries to connect to HTTPS    
        try:
            r2 = requests.get(full_address2)
            remove_flag = 1
            active_ports.append(port)
        except:
            print("")
            
        # removes any web based ports
        if remove_flag == 1 :
            ports.remove(port)
    # tries to connect via sockets to remaining ports
    for remaining_ports in ports:
        s = socket.socket()
        try:
            s.connect((IP_INPUT,remaining_ports))
            response = s.recv(1024)
            s.close
            active_ports.append(remaining_ports)
        except:
            print("")

    ports = str(ports)
    active_ports = str(active_ports)
    now = datetime.now()
    file_name = now.strftime("%d:%m:%Y_%H:%M:%S_port_scan.txt")
    file_name = str(file_name)
    with open(file_name, 'w') as filehandle:
                    filehandle.writelines("IP Address scanned: \n")
                    filehandle.writelines(IP_INPUT,)
                    filehandle.writelines("\nPorts scanned: \n")
                    filehandle.writelines(ports)
                    filehandle.writelines("\nActive ports found: \n")
                    filehandle.writelines(active_ports)
                    filehandle.writelines("\n")
    return()


#port_scan_UI()
port_scan_auto("192.168.0.38","10","81")

