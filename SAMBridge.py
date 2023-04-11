import sys
import time 
import socket

sam_checkpoint = "sam_vit_h_4b8939.pth"
model_type = "vit_h"

print(sys.argv[1])
print(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((sys.argv[1], int(sys.argv[2])))
s.listen(3)

recieveData = True 

while recieveData:
    conn, addr = s.accept()
    data = conn.recv(1024)
    conn.close()
    print("Data recieved in container: %s" % (data)) 

    """ Should I include here a wait function before moving on? """

from segment_anything import SamAutomaticMaskGenerator, sam_model_registry
sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
mask_generator = SamAutomaticMaskGenerator(sam)
masks = mask_generator.generate(data)

for i in range(1,10):
    time.sleep(2)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((sys.argv[1], int(sys.argv[2])))
    sock.sendall(masks)
    sock.close()
