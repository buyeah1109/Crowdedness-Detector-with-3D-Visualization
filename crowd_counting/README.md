
# A Computer Vision Dual-model Crowd Counting, Locating and Crowdedness Computation Software

This repository provides a software prototype that contains front-end and back-end implementation in a very-beginning stage. This software is built for crowd counting, locating and computing crowdedness. The data will then be projected to pre-built 3D model for visualization

## At a glance
[![Figure 1][pic 1]][pic 1]

Note: All the image for demo are from www.unsplash.com and [ShanghaiTech A dataset](https://github.com/desenzhou/ShanghaiTechDataset).

Our Application is boosted up by well-known opensource computer vision best practice repository [computervision_recipes](https://github.com/microsoft/computervision-recipes) from Microsoft. We used some consistent APIs to build parts of backend modules that are able to detect and count crowd. Then we applied our self-designed algorithm to compute crowdedness.

## Dual Model

We adopted two model in this application and they are Multi-Column Convolutional Neural Network (MCNN, [Paper Here]()) and OpenPose Model.

The reasons we select these two model are that they both achieve high-speed performance requirement, and MCNN is suitable for high-density while OpenPose performs well in low-density scenarios. Thus, this dual-model could handle general scenarios by deciding which model to be used. For more information, please refer to Microsoft repository we posted above and there is more detail about model selection.

[pic 1]: media/glance.PNG

## Crowdedness Computation

There is few implementation on crowdedness computation. Thus, we designed an algorithm to satisfy this requirement.

[![Figure 2][pic 2]][pic 2]

This algorithm computes an index which could indicates crowdedness in scenarios that crowd is dense or not dense but tend to form clusters (the distribution is within a small area). In general, it is related with social distance.

For example, following two crowd distribution map (preprocessed) should both be considered as 'crowded', a good crowdedness computation algorithm should output a similar index.

Figure 1: 10 people form two group (Low Density, tend to form cluster)

[![Figure 3][pic 3]][pic 3]

Figure 2: 15 people average distributed (Higher density, not tend to form cluster)

[![Figure 4][pic 4]][pic 4]

Diffence between Figure 1 & 2:

1. in traditional density approach: 50%

2. in our crowdedness index: 3.16%

Figure 3: 10 people average distributed

[![Figure 4][pic 5]][pic 5]

Difference between Figure 1 & 3

1. in traditional approach: 0%
2. in our approach: 31.2%

Which indicates that our algorithm is much better than common density approach, for traditional mean central distance approach, it could not differenciate clustering tendency as well.

[pic 2]: media/equation.png
[pic 3]: crowdcounting/data/images/den1.png
[pic 4]: crowdcounting/data/images/den2.png
[pic 5]: crowdcounting/data/images/den3.png



## Setup
### Dependencies
You need dependencies below. 
- Python 3
- Tensorflow 1.4.1+
- PyTorch

### Install
Clone the repo recursively and install libraries.
```bash
git clone --recursive git@github.com:microsoft/ComputerVision.git
cd ComputerVision/contrib/crowd_counting/
pip install -r requirements.txt 
```

Then download the MCNN model trained on the Shanghai Tech A dataset and save it under folder crowdcounting/data/models/ of the cloned repo. The link to the model can be found in the Test section of [this repo](https://github.com/svishwa/crowdcount-mcnn).

### Test
Below is how to run the demo app and call the service using a local image.
```
python crowdcounting/demo/app-start.py -p crowdcounting/data/models/mcnn_shtechA_660.h5
curl -H "Content-type: application/octet-stream" -X POST http://0.0.0.0:5000/score --data-binary @/path/to/image.jpg
```
## Performance
Below we report mean absolute error on our own dataset. 

|Crowd Density | MCNN | OpenPose | Router|
| -------| ------- | ------- | ------- |
| low | 51.95 | 0.56 | 0.63 |
| high |  151.11 | 442.15 | 195.93 |


## Examples
A tutorial can be found in the crowdcounting/examples folder.

## Docker image
A docker image for a demo can be built and run with the following commands:
```bash
nvidia-docker build -t crowd-counting:mcnn-openpose-gpu
nvidia-docker run -d -p 5000:5000 crowd-counting:mcnn-openpose-gpu
```
Then type the url 0.0.0.0:5000 in a browser to try the demo.

## Build Status
[![Build Status](https://dev.azure.com/team-sharat/crowd-counting/_apis/build/status/lixzhang.cnt?branchName=lixzhang%2Fsubmodule-rev3)](https://dev.azure.com/team-sharat/crowd-counting/_build/latest?definitionId=49&branchName=lixzhang%2Fsubmodule-rev3)
