#!/usr/bin/python3

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst
print(Gst.version())

import numpy


def bus_call(bus, msg, *args):
    print("BUSCALL", msg, msg.type, *args)
    sample = args[1].emit("pull-sample")

    if msg.type == Gst.MessageType.EOS:
        print("End-of-stream")
        loop.quit()
        return
    elif msg.type == Gst.MessageType.ERROR:
        print("GST ERROR", msg.parse_error())
        loop.quit()
        return
    return True

saturation = 50
def set_saturation():
    print("Setting saturation to {0}".format(saturation))
    videosrc.set_property("saturation", saturation)
    return True

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



def new_buffer(sink, data):
    global image_arr
    sample = sink.emit("pull-sample")
    # buf = sample.get_buffer()
    # print "Timestamp: ", buf.pts
    arr = gst_to_opencv(sample)
    image_arr = arr
    return Gst.FlowReturn.OK


if __name__ == "__main__":
    GObject.threads_init()
    # initialization
    loop = GObject.MainLoop()
    Gst.init(None)
    # create elements
    pipeline = Gst.Pipeline()
    # watch for messages on the pipeline's bus (note that this will only
    # work like this when a GLib main loop is running)
    bus = pipeline.get_bus()

    sink = Gst.ElementFactory.make("appsink", 'sink0')
    #sink.connect("new-sample", new_buffer, sink)
    #sink.set_property("emit-signals", True)

    bus.add_watch(0, bus_call, loop,sink) # 0 == GLib.PRIORITY_DEFAULT

    # create elements
    videosrc = Gst.ElementFactory.make('v4l2src', "src0")
    #videosrc = Gst.ElementFactory.make('rpicamsrc', "src0")
    videosrc.set_property("saturation", saturation)

    sink = Gst.ElementFactory.make("autovideosink", 'sink0')



    caps = Gst.Caps.from_string("video/x-raw, width=320, height=240")

    # add elements
    pipeline.add(videosrc)
    pipeline.add(sink)

    # link elements
    videosrc.link_filtered(sink, caps)

    # this will call set_saturation every 1s
    GObject.timeout_add(1000, set_saturation)

    # run
    pipeline.set_state(Gst.State.PLAYING)
    try:
        loop.run()
    except Exception as e:
        print(e)
    # cleanup
pipeline.set_state(Gst.State.NULL)