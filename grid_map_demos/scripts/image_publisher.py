#!/usr/bin/env python
# simple script to publish a image from a file.
import rospy
import time
import cv2
import sensor_msgs.msg

#change this to fit the expected topic name.
IMAGE_MESSAGE_TOPIC = 'grid_map_image'

#define here the image path and name.
#IMAGE_PATH = 'example_image_16bit.tif'
#IMAGE_PATH = 'bgra8.png'
#IMAGE_PATH = 'bgr8.png'
IMAGE_PATH = 'grayscale8.png'

def callback(self):
    """ Convert a image to a ROS compatible message
        (sensor_msgs.Image).
    """
    img = cv2.imread(IMAGE_PATH, -1)
    
#    print img.shape
#    print img.size
#    print img.dtype.itemsize

    rosimage = sensor_msgs.msg.Image()
    if img.dtype.itemsize == 2:
       if len(img.shape) == 3:
           if img.shape[2] == 3:
               rosimage.encoding = 'bgr16'
           if img.shape[2] == 4:
           	   rosimage.encoding = 'bgra16'
       else:
           rosimage.encoding = 'mono16'
    if img.dtype.itemsize == 1:
       if len(img.shape) == 3:
           if img.shape[2] == 3:
               rosimage.encoding = 'bgr8'
           if img.shape[2] == 4:
           	   rosimage.encoding = 'bgra8'
       else:
           rosimage.encoding = 'mono8'
    print "Encoding: ", rosimage.encoding
    
    rosimage.width = img.shape[1]
    rosimage.height = img.shape[0]
    rosimage.step = img.strides[0]
    rosimage.data = img.tostring()
    rosimage.header.stamp = rospy.Time.now()
    rosimage.header.frame_id = ''

    publisher.publish(rosimage)


#Main function initializes node and subscribers and starts the ROS loop
def main_program():
    global publisher
    rospy.init_node('image_publisher')
    publisher = rospy.Publisher(IMAGE_MESSAGE_TOPIC, sensor_msgs.msg.Image, queue_size=10)
    rospy.Timer(rospy.Duration(2), callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        main_program()
    except rospy.ROSInterruptException: pass
