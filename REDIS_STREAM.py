import cv2
import redis
import argparse
import time
import traceback
import threading
import pickle
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--channel', default="test")

args=parser.parse_args()

POOL = redis.ConnectionPool(host= "localhost", port= 6379, db=0)
REDIS_CLIENT = redis.Redis(connection_pool= POOL)


pubsub = REDIS_CLIENT.pubsub()
pubsub.subscribe(args.channel)


def get_stream(pub):

    for message in pubsub.listen():
        if message.get("type") == "message":

            data = message.get("data")
            data = pickle.loads(data)
            im = data["img"]
            cam_name = data["cam_name"]
            cv2.imshow(cam_name, im)
            cv2.waitKey(1)
            #print("data found ..")


get_stream(pub=pubsub)