import sys
import socket
import time 

data = img, qualityCheck, maskQuality, maskStability

for i in range(1,10):
    time.sleep(2)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((sys.argv[1], int(sys.argv[2])))
    sock.sendall(data)
    sock.close()

recieveData = True 

while recieveData:
    conn, addr = s.accept()
    masks = conn.recv(1024)
    conn.close()
    print("Data recieved in container: %s" % (masks)) 

    if qualityCheck == True:
        maskQuality = masks["predicted_iou"]
        maskStability = masks["stability_score"]

        print(f"Predicted mask quality is {maskQuality}, and predicted stabillity is {maskStability}")