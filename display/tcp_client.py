import socket, cv2
import numpy as np
import time, copy, struct

mouse_event_types = { 
    0:"EVENT_MOUSEMOVE",
    1:"EVENT_LBUTTONDOWN",
    2:"EVENT_RBUTTONDOWN",
    3:"EVENT_MBUTTONDOWN",
    4:"EVENT_LBUTTONUP",
    5:"EVENT_RBUTTONUP",
    6:"EVENT_MBUTTONUP",
    7:"EVENT_LBUTTONDBLCLK",
    8:"EVENT_RBUTTONDBLCLK",
    9:"EVENT_MBUTTONDBLCLK",
    10:"EVENT_MOUSEWHEEL",
    11:"EVENT_MOUSEHWHEEL"}
mouse_event_flags = { 
    0:"None",

    1:"EVENT_FLAG_LBUTTON", 
    2:"EVENT_FLAG_RBUTTON", 
    4:"EVENT_FLAG_MBUTTON",

    8:"EVENT_FLAG_CTRLKEY",
    9:"EVENT_FLAG_CTRLKEY + EVENT_FLAG_LBUTTON",
    10:"EVENT_FLAG_CTRLKEY + EVENT_FLAG_RBUTTON",
    11:"EVENT_FLAG_CTRLKEY + EVENT_FLAG_MBUTTON",

    16:"EVENT_FLAG_SHIFTKEY",
    17:"EVENT_FLAG_SHIFTKEY + EVENT_FLAG_LBUTTON",
    18:"EVENT_FLAG_SHIFTLKEY + EVENT_FLAG_RBUTTON",
    19:"EVENT_FLAG_SHIFTKEY + EVENT_FLAG_MBUTTON",

    32:"EVENT_FLAG_ALTKEY",
    33:"EVENT_FLAG_ALTKEY + EVENT_FLAG_LBUTTON",
    34:"EVENT_FLAG_ALTKEY + EVENT_FLAG_RBUTTON",
    35:"EVENT_FLAG_ALTKEY + EVENT_FLAG_MBUTTON"}

adfad = [[0,0],[0,0],[0,0],[0,0]]
asdsw = 0

def IMAGE_LOAD_FROM_CAMERA(UUUUUUU):

    # 서버의 주소입니다. hostname 또는 ip address를 사용할 수 있습니다.
    HOST = '192.168.1.17'  
    # 서버에서 지정해 놓은 포트 번호입니다. 
    PORT = 10200

    # 소켓 객체를 생성합니다. 
    # 주소 체계(address family)로 IPv4, 소켓 타입으로 TCP 사용합니다.  
    client_socket = socket.socket(socket. AF_INET, socket.SOCK_STREAM)
    # 지정한 HOST와 PORT를 사용하여 서버에 접속합니다. 
    client_socket.connect((HOST, PORT))

    # 메시지를 전송합니다. 
    client_socket.sendall(UUUUUUU.encode())

    asda = b""
    while(1):
        data = client_socket.recv(4096)
        if(len(data)<=0):
            break
        asda = asda + data
    client_socket.close()    # 소켓을 닫습니다.

    return asda
def SEND_INIT_POINTS_TO_CAMERA(sasasas):
    HOST = '192.168.1.17'
    PORT = 20400

    # 소켓 객체를 생성합니다. 
    # 주소 체계(address family)로 IPv4, 소켓 타입으로 TCP 사용합니다.  
    client_socket = socket.socket(socket. AF_INET, socket.SOCK_STREAM)
    # 지정한 HOST와 PORT를 사용하여 서버에 접속합니다. 
    client_socket.connect((HOST, PORT))

    # 메시지를 전송합니다. 
    client_socket.sendall("RRRR".encode()+sasasas)

    # 메시지를 전송합니다. 
    data = client_socket.recv(4096)

    client_socket.close()    # 소켓을 닫습니다.
def SEND_AUTO_INIT():
    HOST = '192.168.1.17'
    PORT = 20400

    # 소켓 객체를 생성합니다. 
    # 주소 체계(address family)로 IPv4, 소켓 타입으로 TCP 사용합니다.  
    client_socket = socket.socket(socket. AF_INET, socket.SOCK_STREAM)
    # 지정한 HOST와 PORT를 사용하여 서버에 접속합니다. 
    client_socket.connect((HOST, PORT))

    # 메시지를 전송합니다. 
    client_socket.sendall("RRRR".encode)

    # 메시지를 받습합니다. 
    data = client_socket.recv(4096)

    client_socket.close()    # 소켓을 닫습니다.
def SEND_VIEW_ALIGN():
    HOST = '192.168.1.17'
    PORT = 20400

    # 소켓 객체를 생성합니다. 
    # 주소 체계(address family)로 IPv4, 소켓 타입으로 TCP 사용합니다.  
    client_socket = socket.socket(socket. AF_INET, socket.SOCK_STREAM)
    # 지정한 HOST와 PORT를 사용하여 서버에 접속합니다. 
    client_socket.connect((HOST, PORT))

    # 메시지를 전송합니다. 
    client_socket.sendall("RRRR".encode())

    # 메시지를 받습합니다. 
    data = client_socket.recv(4096)

    client_socket.close()    # 소켓을 닫습니다.

def mouse_callback(event, x, y, flags, param):

    global asdsw
        
    if event == 1:
        adfad[asdsw][0], adfad[asdsw][1] = x, y
        asdsw = (asdsw+1) & 0b11
        print(adfad)
    elif event == 2:
        SEND_VIEW_ALIGN()
    elif event == 3:
        SEND_INIT_POINTS_TO_CAMERA(
            struct.pack( '!llllllll', 
                adfad[0][0],adfad[0][1],
                adfad[1][0],adfad[1][1],
                adfad[2][0],adfad[2][1],
                adfad[3][0],adfad[3][1]
            )
        )
        print("EVENT_MBUTTONDOWN", adfad)

def main():

    # 마우스 이벤트를 감지할 윈도우 생성 
    cv2.namedWindow('image')  
    cv2.setMouseCallback('image', mouse_callback) 

    while(1):
        
        asda = IMAGE_LOAD_FROM_CAMERA('RAW')

        encoded_img = np.frombuffer(asda, dtype = np.uint8)
        
        cv2.imshow('image', cv2.imdecode(encoded_img, cv2.IMREAD_COLOR))
        
        cv2.waitKey(100)

    cv2.destroyAllWindows()

#main()