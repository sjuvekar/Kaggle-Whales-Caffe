IMWIDTH=384

DATA_ROOT=./
IMAGES=images/
LEVELDB=images/

TOOLS=$CAFFE_ROOT/build/tools

if [ -f prepdone ]
then
    echo prepdone exists. Skipping preprocess...
else
    python preprocess.py --imwidth $IMWIDTH
    touch prepdone
fi

echo "Create leveldbs for train, mask1. mask2 and test...."

echo "Creating train lmdb..."

GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --shuffle \
    $DATA_ROOT \
    $IMAGES/train_points.txt \
    $LEVELDB/train_lmdb

echo "Creating test lmdb..."

echo "Creating mask_point1 lmdb..."

GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --shuffle \
    --gray \
    $DATA_ROOT \
    $IMAGES/mask_point1.txt \
    $LEVELDB/mask_point1_lmdb

echo "Creating mask_point2 lmdb..."

GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --shuffle \
    --gray \
    $DATA_ROOT \
    $IMAGES/mask_point2.txt \
    $LEVELDB/mask_point2_lmdb

echo "Creating test lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --shuffle \
    $DATA_ROOT \
    $IMAGES/test_points.txt \
    $LEVELDB/test_lmdb

echo "LevelDBs creation Done."

# Train Deconv-networks for cropping
#$CAFFE_ROOT/build/tools/caffe train -solver solvers/solver_1.prototxt
$CAFFE_ROOT/build/tools/caffe train -solver solvers/solver_1.prototxt -gpu 0
$CAFFE_ROOT/build/tools/caffe train -solver solvers/solver_2.prototxt -gpu 0
### TODO: Add code (python?) to rotate&crop test images(testcrops) using estimated points1/2

# Train classifier on cropped training images
#$CAFFE_ROOT/build/tools/caffe train -solver solvers/classifier_solver.prototxt -gpu 0
