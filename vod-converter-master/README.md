# Visual Object Dataset converter

Converts between object dataset formats.

Example: convert from data in [KITTI](http://www.cvlibs.net/datasets/kitti/eval_object.php) format to
[Pascal VOC](http://host.robots.ox.ac.uk/pascal/VOC/voc2012/htmldoc/index.html) format:

```
$ python vod_converter/main.py --from kitti --from-path datasets/mydata-kitti --to voc --to-path datasets/mydata-voc
```

## Usage

Flags:

* `--from-path`: Source dataset
* `--from`: Type of source dataset. This flag only accepts 4 values:
    * `kitti`: [KITTI](http://www.cvlibs.net/datasets/kitti/eval_object.php).
    * `kitti-tracking`: [KITTI tracking](http://www.cvlibs.net/datasets/kitti/eval_tracking.php).
    * `voc`: [Pascal VOC](http://host.robots.ox.ac.uk/pascal/VOC/voc2012/htmldoc/index.html)
    * `udacity-crowdai`: [Udacity CrowdAI](https://github.com/udacity/self-driving-car/tree/master/annotations#dataset-1).
    * `udacity-autti`: [Udacity AUTTI](https://github.com/udacity/self-driving-car/tree/master/annotations#dataset-2)
* `--to-path`: Destination path
* `--to`: Type of destination dataset. This flag only accepts 2 values:
    * `kitti`: [KITTI](http://www.cvlibs.net/datasets/kitti/eval_object.php).
    * `voc`: [Pascal VOC](http://host.robots.ox.ac.uk/pascal/VOC/voc2012/htmldoc/index.html)

See `main.py` for documentation on how to easily plug in additional data formats; you can define a function
that can read in your data into a common format, and it will be then ready to convert to any supported format.

Similarly, you can implement a single function that takes the common format and outputs to the filesystem in
your format and you will be ready to convert from e.g VOC to yours.


# Acknowledge

This repository is a fork from [vod-converter](https://github.com/umautobots/vod-converter) but has some 
changes to be compatible with both Python 2 and 3