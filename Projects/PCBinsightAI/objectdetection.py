import os
from ultralytics import YOLOv10

class Yolo:
    def __init__(self):
        self.HOME = os.getcwd()
        print(self.HOME)

    def model_infernce(self, test_image):
        # Todo: Inference on best weight
        best_weight = f'{self.HOME}/runs/detect/train/weights/best.pt'
        model = YOLOv10(best_weight)

        # Test the model
        self.test_image = test_image

        result = model.predict(self.test_image,
                               save=True,
                               conf=0.05)
        # print(result)

        bbox = result[0].boxes

        return bbox
