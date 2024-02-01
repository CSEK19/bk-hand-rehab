import numpy as np
import cv2
import ctypes

class Visualizer:
  def __init__(self, width=400, height=400):
    self.maps_initialized = False
    self.width = width
    self.height = height

  def visualize(self, images, label=None, secs=1):
    # images: left and right images of LM controller
    if not self.maps_initialized:
      self.left_coordinates, self.left_coefficients = self.convert_distortion_maps(images[0])
      self.right_coordinates, self.right_coefficients = self.convert_distortion_maps(images[1])
      self.maps_initialized = True

    image = images[0]
    vis_img = self.undistort(image, self.left_coordinates, self.left_coefficients, self.width, self.height)

    if label:
      vis_img = cv2.putText(vis_img, label, (100,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 1, cv2.LINE_AA)
    
    return vis_img

  def convert_distortion_maps(self, image):
    distortion_length = image.distortion_width * image.distortion_height
    xmap = np.zeros(distortion_length//2, dtype=np.float32)
    ymap = np.zeros(distortion_length//2, dtype=np.float32)

    for i in range(0, distortion_length, 2):
      xmap[distortion_length//2 - i//2 - 1] = image.distortion[i] * image.width
      ymap[distortion_length//2 - i//2 - 1] = image.distortion[i + 1] * image.height

    xmap = np.reshape(xmap, (image.distortion_height, image.distortion_width//2))
    ymap = np.reshape(ymap, (image.distortion_height, image.distortion_width//2))

    #resize the distortion map to equal desired destination image size
    resized_xmap = cv2.resize(xmap, (image.width, image.height), 0, 0, cv2.INTER_LINEAR)
    resized_ymap = cv2.resize(ymap, (image.width, image.height), 0, 0, cv2.INTER_LINEAR)

    #Use faster fixed point maps
    coordinate_map, interpolation_coefficients = cv2.convertMaps(resized_xmap, resized_ymap, cv2.CV_32FC1, nninterpolation = False)

    return coordinate_map, interpolation_coefficients

  def undistort(self, image, coordinate_map, coefficient_map, width, height):
    destination = np.empty((width, height), dtype = np.ubyte)
    ptr = image.data_method()
    # print(ptr)
    # print(hex(id(ptr)))
    #wrap image data in numpy array
    
    i_address = (int(ptr.cast()))

    ctype_array_def = ctypes.c_ubyte * image.height * image.width
    # as ctypes array
    as_ctype_array = ctype_array_def.from_address(i_address)
    # as numpy array
    as_numpy_array = np.ctypeslib.as_array(as_ctype_array)
    img = np.reshape(as_numpy_array, (image.height, image.width))

    #remap image to destination
    destination = cv2.remap(img,
                            coordinate_map,
                            coefficient_map,
                            interpolation = cv2.INTER_LINEAR)

    #resize output to desired destination size
    destination = cv2.resize(destination,
                              (width, height),
                              0, 0,
                              cv2.INTER_LINEAR)
    return destination