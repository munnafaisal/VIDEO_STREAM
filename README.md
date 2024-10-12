# VIDEO_STREAM

### First capture video with RTSP URL provided ###

 `rtsp_capture.py -r rtsp://admin:admin@192.168.0.100:1935 -c test -n cam_1`
 
 ```
 -r :: RTSP URL of the camera
 -c :: REDIS channel name where this camera data to be published
 -n :: Name of the camera 
 
 ```
 
### Now RUN REDIS subscriber ###

