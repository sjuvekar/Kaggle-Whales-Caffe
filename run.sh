imwidth=384

if [ -f prepdone ]
then
    echo prepdone exists. Skipping prep...
else
    python preprocess.py --imwidth $imwidth
    touch prepdone
fi

# Train Deconv-networks for cropping
$CAFFE_ROOT/build/tools/caffe train -solver solvers/solver_1_x.prototxt -gpu 0
$CAFFE_ROOT/build/tools/caffe train -solver solvers/solver_1_y.prototxt -gpu 0
$CAFFE_ROOT/build/tools/caffe train -solver solvers/solver_2_x.prototxt -gpu 0
$CAFFE_ROOT/build/tools/caffe train -solver solvers/solver_2_y.prototxt -gpu 0

## Uncomment these to use two networks for each of the points
# $CAFFE_ROOT/build/tools/caffe train -solver solvers/solver_1.prototxt -gpu 0
# $CAFFE_ROOT/build/tools/caffe train -solver solvers/solver_2.prototxt -gpu 0
### TODO: Add code (python?) to rotate&crop test images(testcrops) using estimated points1/2

# Train classifier on cropped training images
$CAFFE_ROOT/build/tools/caffe train -solver solvers/classifier_solver.prototxt -gpu 0
