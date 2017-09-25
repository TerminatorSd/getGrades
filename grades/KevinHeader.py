#coding=utf-8
#加载必要的库
import numpy as np

import sys,os,random

#设置当前目录
caffe_root = '/home/xsd/Deep_Learning/caffe/'
sys.path.insert(0, caffe_root + 'python')
import caffe
os.chdir(caffe_root)

net_file=caffe_root + 'models/bvlc_reference_caffenet/KevinNet_CIFAR10_deploy32.prototxt'
caffe_model=caffe_root + 'models/bvlc_reference_caffenet/KevinNet_CIFAR10_32.caffemodel'
mean_file=caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy'

net = caffe.Net(net_file,caffe_model,caffe.TEST)
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_transpose('data', (2,0,1))
transformer.set_mean('data', np.load(mean_file).mean(1).mean(1))
transformer.set_raw_scale('data', 255)
transformer.set_channel_swap('data', (2,1,0))

def getRandomFeature():
    feature = ""
    for i in range(1, 1000):
        ran = random.random()
        if(ran > 0.5):
            feature += '1'
        else:
            feature += '0'

    return feature

def write_pair(pair, pair_path):
    print pair
    print pair_path
    pair_wt = open(pair_path, 'w')
    try:
        for i in pair:
            print i
            pair_wt.write(i.encode('utf-8'))
            # print i.encode('utf-8')
            pair_wt.write(':')
            pair_wt.write(pair[i].encode('utf-8'))
            pair_wt.write('\n')
    finally:
        pair_wt.close()


    print 'complete writing pair file!'

def read_from_pair(pair_path):
    pair = {}
    pair_read = open(pair_path, 'r')
    try:
        for line in pair_read.readlines():
            str = line.split('\n')[0].split(':')
            pair[str[0]] = str[1]
    finally:
        pair_read.close()
    return pair

# extract feature of images in a certain folder and write them to the files
def extract_feature(base_dir, feature_path):

    pair = {}
    items = os.listdir(base_dir)

    for i in range(0, len(items)):
        path = os.path.join(base_dir, items[i])

        file_name = os.path.split(path)[1]
        pair[file_name] = {}

        im = caffe.io.load_image(path)
        net.blobs['data'].data[...] = transformer.preprocess('data', im)
        out = net.forward()

        encode = net.blobs['fc8_kevin_encode'].data[0].flatten()
        code = []
        for j in np.arange(encode.size):
            if (encode[j] >= 0.5):
                code.append('1')
            else:
                code.append('0')
            # print code[j],
        pair[file_name]['code'] = ''.join(code)

        to_path = os.path.join(feature_path, items[i].split('.')[0] + '.txt')

        pair[file_name]['txt_name'] = os.path.split(to_path)[1]

        feature = open(to_path, 'w')
        try:
            feature.write(''.join(code))
            feature.write('\n')
        finally:
            feature.close()
        print to_path

    return pair

def extract_feature_of_target(image):
    im = caffe.io.load_image(image)
    net.blobs['data'].data[...] = transformer.preprocess('data', im)
    out = net.forward()

    encode = net.blobs['fc8_kevin_encode'].data[0].flatten()
    code = []
    for j in np.arange(encode.size):
        # print encode[j]
        if (encode[j] >= 0.5):
            code.append('1')
        else:
            code.append('0')
    return code

def printTopk(topk, sort):
    result = {}
    print 'The result of top ' + str(topk) + ' is: '
    i = 0
    for item in sort:
        if(i < topk):
            print item[0], item[1]
            result[i] = {}
            result[i]['name'] = item[0]
            result[i]['distance'] = item[1]
            i += 1
    return result

def calculate_hamming_distance(feature_path, code, topk):
    feature_dic = {}
    items2 = os.listdir(feature_path)
    for i in range(0, len(items2)):

        # path2为遍历特征文件夹中txt文件的所有路径
        path2 = os.path.join(feature_path, items2[i])
        feature_read = open(path2, 'r')
        try:
            temp = feature_read.readlines()
            dif = 0
            for line in temp:
                # print path2.split('/')[len(path2.split('/')) - 1],
                # print line
                for k in range(0, len(code)):
                    if(code[k] != line[k]):
                        dif += 1
            feature_dic[path2] = dif
        finally:
            feature_read.close()
    sort = sorted(feature_dic.iteritems(), key = lambda asd:asd[1], reverse = False)
    result = printTopk(topk, sort)
    return result

