#!/usr/bin/python

import os
import numpy as np

caffe_root = './caffe-master/' 
import sys
sys.path.insert(0, caffe_root + 'python')
import caffe

import cv #Opencv
import cv2
import PIL as Image #Image from PIL
import os

mean_filename = 'images/caffemodels/mean.binaryproto'
proto_data    = caffe.io.caffe_pb2.BlobProto.FromString(open(mean_filename, "rb").read())
mean = caffe.io.blobproto_to_array(proto_data)[0]

age_net_pretrained='images/caffemodels/age_net.caffemodel'
age_net_model_file='images/prototxt/deploy_age.prototxt'
age_net = caffe.Classifier(age_net_model_file, age_net_pretrained,
                       channel_swap=(2,1,0),
                       raw_scale=255,
                       image_dims=(256, 256))

gender_net_pretrained='images/caffemodels/gender_net.caffemodel'
gender_net_model_file='images/prototxt/deploy_gender.prototxt'
gender_net = caffe.Classifier(gender_net_model_file, gender_net_pretrained,
                       channel_swap=(2,1,0),
                       raw_scale=255,
                       image_dims=(256, 256))

age_list=['(0, 2)','(4, 6)','(8, 12)','(15, 20)','(25, 32)','(38, 43)','(48, 53)','(60, 100)']
gender_list=['Male','Female']

def get_faces(image_path):
    img = np.asarray(bytearray(open(image_path).read()), dtype="uint8")
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier('images/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        tmp_image = img[max(y-100,0):y+h+100,max(x-100,0):x+w+100]
        yield tmp_image
        #prediction = age_net.predict([tmp_image])
        #print 'predicted age:', age_list[prediction[0].argmax()]
        #prediction = gender_net.predict([tmp_image])
        #print 'predicted gender:', gender_list[prediction[0].argmax()]

def predict_image(opts, profile_data, age_range_fnc):
    age_correct   = 0
    age_incorrect = 0
    gender_correct   = 0
    gender_incorrect = 0

    for user_id,user_data in profile_data['testing_data'].items():
        path  = "%s/image/%s.jpg" % (opts.inputdir, user_id)
        faces = list(get_faces(path))
 
        o_age = int(user_data['age'])
        o_gender = int(user_data['gender'])

        for face in faces:
            cv2.imwrite('/data/faces/%s.png' % user_id,face)

            prediction = age_net.predict([face])
            print(list(prediction[0]))
            age = age_list[prediction[0].argmax()][1:-1].split(',')
            age = (int(age[0]),int(age[1]))
            prediction = gender_net.predict([face])
            print(list(prediction[0]))
            gender = gender_list[prediction[0].argmax()]
            if gender == 'Male':
                gender = 0
            else:
                gender = 1
            if o_age >= age[0] and o_age <= age[1]:
                age_correct += 1
            else:
                age_incorrect += 1
            if o_gender == gender:
                gender_correct += 1
            else:
                gender_incorrect += 1
            print(age,gender,o_age,o_gender)
            print "\n"
        print (age_correct*100)/(age_correct+age_incorrect), (gender_correct*100)/(gender_correct+gender_incorrect)
