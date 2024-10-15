import cv2
import redis
import argparse
import time
import traceback
import threading
import pickle
import json

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--rtsp', default=None)
parser.add_argument('-c', '--channel', default= None)
parser.add_argument('-n', '--cam_name', default= "cam_1")

args=parser.parse_args()

#### POOL Redis connection and create REDIS Client

POOL = redis.ConnectionPool(host= "localhost", port= 6379, db=0, password = "123")
'''
If you do not setup redis password then discard the password segment. 
It is recommended to setup redis server password
Ex ..
 
POOL = redis.ConnectionPool(host= "localhost", port= 6379, db=0)


'''

REDIS_CLIENT = redis.Redis(connection_pool= POOL)
pub_chn_name = args.channel
data_dict = {}


if REDIS_CLIENT.ping():
    print("Ping to redis server is successfull")
else:
    print("REDIS server not available ")

cap = cv2.VideoCapture(args.rtsp, cv2.CAP_FFMPEG)

def get_cap():
    '''
    This function create VideoCapture object
    :return:
    VideoCapture object
    '''

    try:
        cap = cv2.VideoCapture(args.rtsp, cv2.CAP_FFMPEG)
        return cap
    except:
        return None


def get_stream():

    '''
    A while loop is executed
    :return:
    Video Frame
    '''

    global cap

    while True:

        try:
            if cap.isOpened():
                ret, frame = cap.read()

                if not ret:
                    print(ret)
                    cap.release()
                    time.sleep(1)
                    # cap = get_cap()
                    #pass
                else:
                    yield frame
            else:
                print("video capture not ready")

                if cap is not None:
                    cap.release()
                time.sleep(2)

                cap = get_cap()
        except:
            print(traceback.print_exc())
            print("video stream not available \n Trying create new video capture object ")
            time.sleep(2)

            if cap is not None:
                cap.release()

            cap = get_cap()



def check_video():

    while True:

        for fr in get_stream():

            try:
                cv2.imshow("VID", fr)
                cv2.waitKey(1)
            except:
                time.sleep(2)
                print("failing to show ")

def update_data(img):

    '''
    insert image and additional data in the dictionary to published on redis channel
    :param img:
    :return:
    '''
    data_dict["idx"] = 1
    data_dict["img"] = img
    data_dict["cam_name"] = args.cam_name

    return data_dict


def publish_on_redis(chn_name):

    '''

    :param chn_name: Redis channel name
    :return: None
    '''

    global index
    index = 0
    while True:
        for fr in get_stream():
            dt = update_data(img= fr)
            dt = pickle.dumps(dt)

            REDIS_CLIENT.publish(pub_chn_name,dt)
            index +=1
            print(" publishing data :: ", index)





#check_video()

publish_on_redis(pub_chn_name)