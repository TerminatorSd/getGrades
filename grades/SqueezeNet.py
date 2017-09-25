#coding=utf-8
#加载必要的库
import numpy as np
import sys,os
import netPublic as npc
import time

#设置当前目录
caffe_root = '/home/xsd/Deep_Learning/caffe/'
sys.path.insert(0, caffe_root + 'python')
import caffe
os.chdir(caffe_root)

net_file=caffe_root + 'models/SqueezeNet/squeezenet_v1.1.prototxt'
caffe_model=caffe_root + 'models/SqueezeNet/squeezenet_v1.1.caffemodel'
mean_file=caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy'

net = caffe.Net(net_file,caffe_model,caffe.TEST)
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_transpose('data', (2,0,1))
transformer.set_mean('data', np.load(mean_file).mean(1).mean(1))
transformer.set_raw_scale('data', 255)
transformer.set_channel_swap('data', (2,1,0))


# extract feature of images in a certain folder and write them to the files
base_dir = '/home/xsd/Deep_Learning/Python_code/images'
feature_path = '/home/xsd/Deep_Learning/Python_code/feature'
blob = 'pool10'
# t1 = time.time()
# npc.extract_feature(base_dir, feature_path, net, transformer, blob)
# print time.time()-t1

# extract feature of the image to be retrieve
image = '/home/xsd/Deep_Learning/Python_code/images/feiji.jpg'
code = npc.extract_feature_of_target(image, net, transformer, blob)

# calculate the hamming distance of features
npc.calculate_hamming_distance(feature_path, code, 6)


