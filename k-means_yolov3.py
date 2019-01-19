from os import listdir
from os.path import isfile, join
import argparse
import numpy as np
import sys
import os
import shutil
import random 
import math
 
def IOU(x,centroids):
    IoUs = []
    w, h = x  
    for centroid in centroids:
        c_w,c_h = centroid   
        if c_w>=w and c_h>=h:   
            iou = w*h/(c_w*c_h)
        elif c_w>=w and c_h<=h:   
            iou = w*c_h/(w*h + (c_w-w)*c_h)
        elif c_w<=w and c_h>=h:   
            iou = c_w*h/(w*h + c_w*(c_h-h))
        else: 
            iou = (c_w*c_h)/(w*h)
        IoUs.append(iou) 
    return np.array(IoUs)
 
def avg_IOU(X,centroids):
    n,d = X.shape
    sum = 0.
    for i in range(X.shape[0]):
        sum+= max(IOU(X[i],centroids))  
    return sum/n    
 
def write_anchors_to_file(centroids,X,anchor_file,input_shape,yolo_version):
    f = open(anchor_file,'w')
    anchors = centroids.copy()
    print(anchors.shape)
    if yolo_version=='yolov2':
        for i in range(anchors.shape[0]):
           
            anchors[i][0]*=input_shape/32.
            anchors[i][1]*=input_shape/32.
    elif yolo_version=='yolov3':
        for i in range(anchors.shape[0]):
           
            anchors[i][0]*=input_shape
            anchors[i][1]*=input_shape
    else:
        print("the yolo version is not right!")
        exit(-1)
 
    widths = anchors[:,0]
    sorted_indices = np.argsort(widths)
 
    print('Anchors = ', anchors[sorted_indices])
        
    for i in sorted_indices[:-1]:
        f.write('%0.2f,%0.2f, '%(anchors[i,0],anchors[i,1]))
 
    #there should not be comma after last anchor, that's why
    f.write('%0.2f,%0.2f\n'%(anchors[sorted_indices[-1:],0],anchors[sorted_indices[-1:],1]))
    
    f.write('%f\n'%(avg_IOU(X,centroids)))
    print()
 
def kmeans(X,centroids,eps,anchor_file,input_shape,yolo_version):
    
    N = X.shape[0] 
    iterations = 0
    print("centroids.shape",centroids)
    k,dim = centroids.shape  
    prev_assignments = np.ones(N)*(-1)    
    iter = 0
    old_D = np.zeros((N,k)) 
 
    while True:
        D = []
        iter+=1           
        for i in range(N):
            d = 1 - IOU(X[i],centroids)
            D.append(d)
        D = np.array(D) 
        
        print("iter {}: dists = {}".format(iter,np.sum(np.abs(old_D-D)))) 
            
        #assign samples to centroids 
        assignments = np.argmin(D,axis=1)  
        
        if (assignments == prev_assignments).all() :  
            print("Centroids = ",centroids)
            write_anchors_to_file(centroids,X,anchor_file,input_shape,yolo_version)
            return
 
        #calculate new centroids
        centroid_sums=np.zeros((k,dim),np.float)  
        for i in range(N):
            centroid_sums[assignments[i]]+=X[i]        
        for j in range(k):           
            centroids[j] = centroid_sums[j]/(np.sum(assignments==j)+1)
        
        prev_assignments = assignments.copy()     
        old_D = D.copy()  
 
def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-filelist', default = '/home/zhangshanshan/darknet/data/kitti-voc/2007_train.txt',
                        help='path to filelist\n' )
    parser.add_argument('-output_dir', default = '/home/zhangshanshan/anchors', type = str,
                        help='Output anchor directory\n' )
    parser.add_argument('-num_clusters', default = 9, type = int, 
                        help='number of clusters\n' )
    parser.add_argument('-yolo_version', default='yolov3', type=str,
                        help='yolov2 or yolov3\n')
    parser.add_argument('-yolo_input_shape', default=608, type=int)
    args = parser.parse_args()
    
    if not os.path.exists(args.output_dir):
        os.mkdir(args.output_dir)
 
    f = open(args.filelist)
  
    lines = [line.rstrip('\n') for line in f.readlines()]
    
    annotation_dims = []
 
    for line in lines:
        line = line.replace('JPEGImages','labels')
        line = line.replace('.jpg','.txt')
        line = line.replace('.png','.txt')
        print(line)
        f2 = open(line)
        for line in f2.readlines():
            line = line.rstrip('\n')
            w,h = line.split(' ')[3:]            
            #print(w,h)
            annotation_dims.append((float(w),float(h)))
    annotation_dims = np.array(annotation_dims) 
  
    eps = 0.005
 
    if args.num_clusters == 0:
        for num_clusters in range(1,11): #we make 1 through 10 clusters 
            anchor_file = join( args.output_dir,'anchors%d.txt'%(num_clusters))
 
            indices = [ random.randrange(annotation_dims.shape[0]) for i in range(num_clusters)]
            centroids = annotation_dims[indices]
            kmeans(annotation_dims,centroids,eps,anchor_file,args.yolo_input_shape,args.yolo_version)
            print('centroids.shape', centroids.shape)
    else:
        anchor_file = join( args.output_dir,'anchors%d.txt'%(args.num_clusters))
        indices = [ random.randrange(annotation_dims.shape[0]) for i in range(args.num_clusters)]
        centroids = annotation_dims[indices]
        kmeans(annotation_dims,centroids,eps,anchor_file,args.yolo_input_shape,args.yolo_version)
        print('centroids.shape', centroids.shape)
 
if __name__=="__main__":
    main(sys.argv)
