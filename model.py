from ultralytics import YOLO

selected_model_path = r'models/light.pt'

def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton
class Model:
    def __init__(self):
        self.yolo_model = YOLO(selected_model_path, task='detect')

    def set_model(self, new_model_path):
        self.yolo_model = YOLO(new_model_path, task='detect')

    def to(self, device):
        self.yolo_model.to(device)

    def track(self, frame):
        return self.yolo_model.track(frame)

# Model()
