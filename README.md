# VIDEO_STREAM


### Install redis server and it's python package/distro

[Visit following link for redis server install in ubuntu](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/install-redis-on-linux/)

[python distro](pip install redis)

### Install RTSP streaming app in your android phone
[Visit Google Play Store and install app](https://play.google.com/store/apps/details?id=com.esona.webcamcloud)

![Screenshot of a comment on a GitHub issue showing an image, added in the Markdown, of an Octocat smiling and raising a tentacle.](https://play-lh.googleusercontent.com/Qzyq2cbD5JUD5iQRqaCU62XcINUR6Qi3CxVy8EKgH_iCwvIeI_MT6jI0NuwGhPlZ4f0=w240-h480-rw)
### First capture video with RTSP URL provided ###

`python3 rtsp_capture.py -r rtsp://admin:admin@192.168.0.100:1935 -c test -n cam_1`
 
 ```
 -r :: RTSP URL of the camera
 -c :: REDIS channel name where this camera data to be published
 -n :: Name of the camera 
 
 ```

#### Create multiple python process with different RTSP URL and same REDIS channel name like below

```
python3 rtsp_capture.py -r rtsp://admin:admin@192.168.0.100:1935 -c test -n cam_2
python3 rtsp_capture.py -r rtsp://admin:admin@192.168.0.100:1935 -c test -n cam_3
python3 rtsp_capture.py -r rtsp://admin:admin@192.168.0.100:1935 -c test -n cam_4
.
.
python3 rtsp_capture.py -r rtsp://admin:admin@192.168.0.100:1935 -c test -n cam_n

```

### Now RUN REDIS subscriber ###

`python3 REDIS_STREAM.py -c test`

```
-c :: REDIS Channel name to be listen on
```
