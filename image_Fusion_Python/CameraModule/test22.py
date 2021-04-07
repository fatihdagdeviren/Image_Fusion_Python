# gi with Gst 1.0 freezes after two or so frames

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst
import numpy
import cv2
from scipy.misc import imshow


# This doesn't seem to make any difference
GObject.threads_init()

Gst.init(None)

image_arr = None

def gst_to_opencv(sample):

    buf = sample.get_buffer()
    caps = sample.get_caps()

    print (caps.get_structure(0).get_value('format'))
    print (caps.get_structure(0).get_value('height'))
    print (caps.get_structure(0).get_value('width'))

    print (buf.get_size())

    arr = numpy.ndarray(
        (caps.get_structure(0).get_value('height'),
         caps.get_structure(0).get_value('width'),
         3),
        buffer=buf.extract_dup(0, buf.get_size()),
        dtype=numpy.uint8)
    return arr

def new_buffer(data):
    global image_arr
    # buf = sample.get_buffer()
    # print "Timestamp: ", buf.pts
    arr = gst_to_opencv(data)
    image_arr = arr



if __name__ == "__main__":
    # This works
    #pipe = Gst.parse_launch("""videotestsrc !
    #        appsink sync=false max-buffers=1 drop=true name=sink emit-signals=true""")
    # This halts after a few frames
    # rtspsrc location=rtsp://admin:asis2018@192.168.1.64/Streaming/Channels/101 ! decodebin ! video/x-raw, format=BGR ! appsink sync=false max-buffers=1 drop=true name=sink emit-signals=true
    # v4l2src device=/dev/video0 ! video/x-raw, format=BGR ! appsink sync=false max-buffers=1 drop=true name=sink emit-signals=true
    # rtspsrc name=source latency=0 ! decodebin ! appsink
    #gst-launch-1.0 rtspsrc location = rtsp://admin:asis2018@192.168.1.64/Streaming/Channels/101 ! decodebin ! autovideosink

    # width, height onemli , width=1920, height=1080  normalde , digerinde kendi width heighti
    #! rtpmp4adepay ! mpeg4videoparse
    # pipe = Gst.parse_launch("""rtspsrc location=rtsp://admin:asis2018@192.168.1.64/Streaming/Channels/101
    #                             ! rtph264depay ! h264parse
    #                             ! decodebin
    #                             ! videoconvert ! video/x-raw, format=(string)BGR, width=1920, height=1080
    #                             ! appsink sync=false max-buffers=1 drop=true name=sink emit-signals=true """)

    pipe = Gst.parse_launch("""rtspsrc location=rtsp://admin:asis2018@192.168.1.64/Streaming/Channels/101
                                ! rtph264depay ! h264parse
                                ! decodebin
                                ! videoconvert ! video/x-raw, format=(string)BGR, width=1920, height=1080 
                                ! appsink sync=false max-buffers=1 drop=true name=sink emit-signals=true """)

    # pipe = Gst.parse_launch("""v4l2src device=/dev/video0
    #                             ! video/x-raw, format=BGR
    #                             ! appsink sync=false max-buffers=1 drop=true name=sink emit-signals=true""")

    sink = pipe.get_by_name('sink')

    #source = pipe.get_by_name('source')
    #source.props.location = 'rtsp://admin:asis2018@192.168.1.64/Streaming/Channels/101'

    pipe.set_state(Gst.State.PLAYING)

    while True:
        print ("Getting a sample")
        sample = sink.emit('pull-sample')
        new_buffer(sample)
        cv2.imshow("image",image_arr)
        cv2.waitKey(1)
        # imshow(image_arr)
        x=2
    # print(sample.get_buffer().get_size())
    # pipeline.set_state(Gst.State.NULL)
