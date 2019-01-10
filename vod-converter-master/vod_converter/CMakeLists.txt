cmake_minimum_required(VERSION 3.9)
project(vod_converter)

set(CMAKE_CXX_STANDARD 11)

add_executable(vod_converter
        __init__.py
        converter.py
        kitti.py
        kitti_tracking.py
        main.py
        udacity.py
        voc.py)
