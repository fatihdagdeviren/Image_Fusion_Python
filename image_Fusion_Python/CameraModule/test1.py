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

def new_buffer(sink):
    data  = sink.emit('pull-sample')
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
    pipe = Gst.parse_launch("""rtspsrc location=rtsp://admin:asis2018@192.168.1.64/Streaming/Channels/101
                                ! rtph264depay ! h264parse
                                ! decodebin
                                ! videoconvert ! video/x-raw, format=(string)BGR, width=1920, height=1080
                                ! appsink sync=false max-buffers=1 drop=true name=sink emit-signals=true """)

    # pipe = Gst.parse_launch("""rtspsrc location=rtsp://admin:asis2018@192.168.1.64/Streaming/Channels/101
    #                             ! rtph264depay ! h264parse
    #                             ! decodebin
    #                             ! videoconvert ! video/x-raw, format=(string)BGR, width=1920, height=1080,framerate=50/1
    #                             ! appsink sync=false wait-on-eos=false max-buffers=60 drop=true name=sink emit-signals=true """)

    # pipe = Gst.parse_launch("""v4l2src device=/dev/video0
    #                             ! video/x-raw, format=BGR
    #                             ! appsink sync=false max-buffers=1 drop=true name=sink emit-signals=true""")

    sink = pipe.get_by_name('sink')
    sink.connect("new-sample", new_buffer)

    #source = pipe.get_by_name('source')
    #source.props.location = 'rtsp://admin:asis2018@192.168.1.64/Streaming/Channels/101'



    pipe.set_state(Gst.State.PLAYING)

    # Wait until error or EOS
    bus = pipe.get_bus()

    while True:
        # print ("Getting a sample")
        message = bus.timed_pop_filtered(10000, Gst.MessageType.ANY)
        if image_arr is not None:
            cv2.imshow("image",image_arr)
            cv2.waitKey(1)
        if message:
            if message.type == Gst.MessageType.ERROR:
                err, debug = message.parse_error()
                print("Error received from element %s: %s" % (
                    message.src.get_name(), err))
                print("Debugging information: %s" % debug)
                break
            elif message.type == Gst.MessageType.EOS:
                print("End-Of-Stream reached.")
                break
            elif message.type == Gst.MessageType.STATE_CHANGED:
                if isinstance(message.src, Gst.Pipeline):
                    old_state, new_state, pending_state = message.parse_state_changed()
                    print("Pipeline state changed from %s to %s." %
                           (old_state.value_nick, new_state.value_nick))
            else:
                print("Unexpected message received.")
        # imshow(image_arr)
        x=2
    # print(sample.get_buffer().get_size())
    # pipeline.set_state(Gst.State.NULL)
