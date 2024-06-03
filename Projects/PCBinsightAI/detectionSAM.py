import os
import emptydir
from objectdetection import Yolo
from samAnnotation import SAM

HOME = os.getcwd()

def detection_annotation(test_image):
    # Todo: Clean Directory
    emptydir.deleteDirectory()

    # Todo: Object Detection
    yolo_obj = Yolo()
    bbox = yolo_obj.model_infernce(test_image=test_image)
    # print(bbox)

    # Todo: Annotation
    sam_obj = SAM()
    sam_obj.annotate(test_image=test_image, bbox=bbox)