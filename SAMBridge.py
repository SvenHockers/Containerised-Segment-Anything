import sys
import time 
import socket
from .SAM/model import vit_h.pth

sys.path.insert(1, '/SAM/model')
import vit_h.pth as sam_checkpoint
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

    img, qualityCheck, maskQuality, maskStability = data

    """ Should I include here a wait function before moving on? """

"""
This function initialise the ANN model and generates the mask 
"""

from SAM import SamAutomaticMaskGenerator, sam_model_registry

device = "cuda" 

sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
sam.to(device=device)

if qualityCheck == False:
    mask_generator = SamAutomaticMaskGenerator(sam)
    masks = mask_generator.generate(img)

    """
    This can also be done outsite the container so, may remove this section
    """
    maskQuality = masks["predicted_iou"]
    maskStability = masks["stability_score"]

    qualtiyScore = maskQuality, maskStability

if qualityCheck == True:
    mask_generator = SamAutomaticMaskGenerator(
        model = sam,
        pred_iou_thresh = maskQuality,
        stability_score_thresh = maskStability,
    )
    masks = mask_generator.generate(img)



for i in range(1,10):
    time.sleep(2)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((sys.argv[1], int(sys.argv[2])))
    sock.sendall(masks)
    sock.close()
