import numpy as np 
import torch 
import matplotlib.pyplot as plt
import cv2

#import image and convert to RGB format
img = cv2.imread('image path') 
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 

"""
Load the ANN and setup the model
"""
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor

sam_checkpoint = "sam_vit_h_4b8939.pth"
model_type = "vit_h"

device = "cuda"

sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
sam.to(device=device)

mask_generator = SamAutomaticMaskGenerator(sam)

masks = mask_generator.generate(img) #generate the mask

