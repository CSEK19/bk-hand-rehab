import numpy as np
import pickle 
from scipy.spatial.distance import pdist
import math
import sklearn

def angle(v1, v2):
  unit_v1 = v1 / np.linalg.norm(v1)
  unit_v2 = v2 / np.linalg.norm(v2)
  dot_product = np.dot(unit_v1, unit_v2)
  angle = np.arccos(dot_product)
  return angle

def distance(x1, x2):
  return math.sqrt((x1[0] - x2[0])**2 + (x1[1] - x2[1])**2 + (x1[2] - x2[2])**2)

class StaticHandPoseClassifier:
  def __init__(self, model_weight, scaler_weight=None):
    self.model = pickle.load(open(model_weight, 'rb'))
    self.scaler = pickle.load(open(scaler_weight, 'rb'))
    self.classes = ['palm', 'left', 'right',  'up', 'down', 'palm_l', 'palm_r', 'palm_u', \
      'fist', 'hook', 'stop', 'thumb_in', 'negative']

  def feature_extraction(self, X, allow_distance=True, allow_palm_angles=True, allow_fingertip_angles=True, allow_fingerbone_angles=False):
    X = np.array(X)
    yaw, pitch, roll, handedness = X[-4:]
    raw_skeleton = X[:-4]
    features = []

    # perform feature extraction
    joints = raw_skeleton.reshape(-1,3)

    # palm joint
    palm = joints[0]
    # thumb joints
    thumb = joints[1:6]
    thumb_bones = [thumb[i+1]-thumb[i] for i in range(1,4)]
    # index joints
    index = joints[6:11]
    index_bones = [index[i+1]-index[i] for i in range(0,4)]
    # middle joints
    middle = joints[11:16]
    middle_bones = [middle[i+1]-middle[i] for i in range(0,4)]
    # ring joints
    ring = joints[16:21]
    ring_bones = [ring[i+1]-ring[i] for i in range(0,4)]
    # pinky joints
    pinky = joints[21:26]
    pinky_bones = [pinky[i+1]-pinky[i] for i in range(0,4)]
    # fingertip joints
    fingertip_joints = np.array([thumb[-1], index[-1], middle[-1], ring[-1], pinky[-1]])

    # angles between finger bones
    if allow_fingerbone_angles:
      thumb_angles = np.array([angle(thumb_bones[i], thumb_bones[i+1]) for i in range(0,2)])
      index_angles = np.array([angle(index_bones[i], index_bones[i+1]) for i in range(0,3)])
      middle_angles = np.array([angle(middle_bones[i], middle_bones[i+1]) for i in range(0,3)])
      ring_angles = np.array([angle(ring_bones[i], ring_bones[i+1]) for i in range(0,3)])
      pinky_angles = np.array([angle(pinky_bones[i], pinky_bones[i+1]) for i in range(0,3)])
      fingerbone_angles = np.concatenate((thumb_angles, index_angles, middle_angles, ring_angles, pinky_angles))
      features.append(fingerbone_angles)

    # angles between fingertips
    if allow_fingertip_angles:
      fingertip_vectors = fingertip_joints - palm
      fingertip_angles = np.array([angle(fingertip_vectors[i], fingertip_vectors[i+1]) for i in range(0,4)])
      features.append(fingertip_angles)

    # yaw pitch roll angle of palm
    if allow_palm_angles:
      palm_angles = np.array([yaw, pitch, roll])
      features.append(palm_angles)

    if allow_distance:
      fingertip_palm_distances = np.array([distance(palm, x) for x in fingertip_joints])
      fingertip_distances = np.array([distance(fingertip_joints[i], fingertip_joints[i+1]) for i in range(0,4)])
      pairwise_distances = np.concatenate((fingertip_palm_distances, fingertip_distances))
      features.append(pairwise_distances)

    if len(features) == 0:
      feature_vector =  np.array(raw_skeleton)
    elif len(features) == 1:
      feature_vector =  features[0]
    else:
      feature_vector = np.concatenate(features, axis=0)

    return feature_vector
  
  def predict(self, X): #shape: (-1, 70)
    #preprocess
    X = self.feature_extraction(np.array(X))
    y = self.model.predict(X.reshape(1,-1))[0]
    # return the class name
    return self.classes[y]
  
  def predict_proba(self, X):
    # print(self.feature_extraction(X).shape)
    # try:
      #preprocess
    X = self.feature_extraction(X)
    X = self.scaler.transform(X.reshape(1,-1))
    y = self.model.predict_proba(X)[0]
    # return the class name and score
    return self.classes[np.argmax(y)], np.max(y)
    # except:
    #   return None


# https://www.webucator.com/article/python-clocks-explained/
# https://sci-hub.se/https://ieeexplore.ieee.org/document/8572153