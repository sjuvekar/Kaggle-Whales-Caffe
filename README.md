# Kaggle-Whales-Caffe

### Description

This is a translation into Caffe of Anil Thomas's Neon-based project for Kaggles Whale Detection Challenge.

- [Competition page at Kaggle](https://kaggle.com/c/noaa-right-whale-recognition)
- [Anil's Code](https://github.com/anlthms/whale-2015)
- [Caffe](caffe.berkeleyvision.org)

### Usage

This is a work in progress and most of the code will still require some of the Python scripts 
from [Anil's repo](https://github.com/anlthms/whale-2015)

1. Download and install Caffe. [Check instructions here](https://github.com/BVLC/caffe/)

2. Create ```/train```, ```/test``` and ```/traincrops``` directories using 
   [Anil's repo](https://github.com/anlthms/whale-2015). All you need is call ```prep``` method in ```run.sh``` in 
   his repo. Copy all three directories to ```data/``` directory here.

3. Declare ```CAFFE_ROOT``` environmental variable. 

    ```
    export CAFFE_ROOT=/path/to/caffe/folder
    ```

4. Call ```run.sh```

    ```
    ./run.sh
    ```

### TODO and Differences
1. X and Y co-ordinate-masks of both Bonnet and Head points are trained independently (a total of 4 NN trainings). Need to find a way for Caffe to work with multi-dimensional output.
2. BatchNormalization is not implemented yet.
3. Cropping Neural Network still blows up on GPU memory in ```g2.2xlarge``` instance. Try running it on ```g2.8xlarge```, or   add following lines to ```image_data_param``` key in ```train/point1_x_train.prototxt``` etc
```
new_height: 512
new_width: 512
```
