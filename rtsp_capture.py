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

POOL = redis.ConnectionPool(host= "localhost", port= 6379, db=0)
REDIS_CLIENT = redis.Redis(connection_pool= POOL)
pub_chn_name = args.channel
data_dict = {}


if REDIS_CLIENT.ping():
    print("Ping to redis server is successfull")
else:
    print("REDIS server not available ")


#cap = cv2.VideoCapture("rtsp://admin:admin@192.168.0.100:1935", cv2.CAP_FFMPEG)
cap = cv2.VideoCapture(args.rtsp, cv2.CAP_FFMPEG)

def get_cap():

    try:
        cap = cv2.VideoCapture(args.rtsp, cv2.CAP_FFMPEG)
        return cap
    except:
        return None


def get_stream():

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
                print("vidcap not ready")

                cap.release()
                time.sleep(2)
                cap = get_cap()

        except:
            print(traceback.print_exc())
            print("stream not available")
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

    data_dict["idx"] = 1
    data_dict["img"] = img
    data_dict["cam_name"] = args.cam_name

    return data_dict


def publish_on_redis(chn_name):

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