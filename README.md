# Containerised Segment Anything

#### Containerised Segment Anything AI Using Docker for Flask framework. <br>
In this repository the <a href="https://github.com/facebookresearch/segment-anything">**Segment Anything (SAM)**</a> is containerised using <a href="https://www.docker.com">Docker<a/> for a <a href="https://flask.palletsprojects.com/en/2.2.x/">Flask</a> environment. This READMD.md is focussed of the development of the docker image and will be used during the project to take notes, gather documentation and highlight errors, limitation and (knowledge) gaps during developement.

To containerise SAM first, a brief introduction of the SAM should be establisched. After some research into Flask environements will be held to ensure the containerised version of SAM will operate accordingly and finnaly some documentation w.r.t. Docker and containerisation of AIs should be discussed.  

## Segment Anything 
SAM is a promptable image segmentation AI which is developed by Meta. In addition to segmenting 2D images, SAM is able to mask an object from a 2D image which than can be tracked in video rendered in 3D or used as an input for other systems. <br>

### Model Basics 
![SAM Flow Chart](readmeFiles/model_diagram.png)

The image is converted by the image encoder which outputs an image embedding which can be efficiently queried by a vararity of user prompts to produce object masks in real-time. For more information regarding the technical working of SAM visit this <a href="chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/https://arxiv.org/pdf/2304.02643.pdf">link</a>.



### License
Keep in mind that although the SAM is open-sourced on Github. The software is under a **Apache License 2.0** which imposes some restrictions and limitations on the use of the software as shown in the figure below.

![Apache License 2.0](readmeFiles/appacheLiciense.png)

## Container Setup
The docker image should be able to import an image, generate a mask on the image and return the mask. 
Than another container or the within the Django framwork itself the mask can be overlayed over the input image to generate the final output.
### Docker 
The docker file is setup as shown in the script below. 

The dependencies are located in <a href="requirement.txt">requirement.txt</a> and are automatically installed during image setup.

```
FROM python:3.10-slim

WORKDIR /SAM

COPY ./requirement.txt /SAM/requirement.txt
RUN pip install --no-cache-dir --upgrade /SAM/requirement.txt

COPY ./segment_anything ./SAM/SAM
COPY ./model/sam_vit_h_4b8939.pth ./SAM/model/vit_h.pth
COPY ./SAMBridge ./SAM/DockerAPI

CMD ["pyhton", "./segment_anything/activateSAM.py", "--host", "0.0.0.0", "--port", "80"]
```

### SAM Model
The SAM model is pulled from the Github repository.

```
pip install git+https://github.com/facebookresearch/segment-anything.git
```

After the model checkpoints have to be downloaded, of which three are available `vit_h` is the **default** model and will be included. At a later stage the other two model (`vit_l` & `vit_b`) maybe included also, making it possible to automatically or manually toggle between models depending on the user requirements.

These are all structured in a directory which makes it easy to navigate the environment at a later stage. 

### SAM init file 
To initialise the SAM model and be able to communicate using a docker container an extra `Python` script has been created to handle communication to and from the container, setup and execute the model. <br>

The script does not include any image pre- or post processing, this could be handled in the future by other containers or back-end depending on the need. This has been done for two reasons, firstly, the container as is is already computational heavy due to the nature of containerising a large model and secondly this way the output from the container is just the mask which allows more flexibillity with the container output.





