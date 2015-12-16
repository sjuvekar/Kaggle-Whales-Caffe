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
1. This code only ports 'test-cropping-via-deconvolution' part of the original code. Classifier will be translated soon.
2. X and Y co-ordinate-masks of both Bonnet and Head points are trained independently (a total of 4 NN trainings). Need to find a way for Caffe to work with multi-dimensional output.
3. BatchNormalization is not implemented yet.
