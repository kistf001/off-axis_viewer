import viewport, controlGui, threading, time, tcp_client

def info():
    print("aaaaaaaaaaaaaaaaaa")
    viewport.main()
def fsss():
    print("ssssssssssssssssss")
    controlGui.main()

if __name__ == '__main__':
    p0 = threading.Thread(target=info)
    p1 = threading.Thread(target=fsss)
    p0.start()
    time.sleep(1)
    p1.start()
