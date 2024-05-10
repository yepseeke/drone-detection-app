import cv2


def to_rgb(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


class VideoProcessor:
    def __init__(self, source):
        self.video_capture = cv2.VideoCapture(source)
        self.net_model = None

    def get_frame(self, color_model='BGR'):
        success, frame = self.video_capture.read()
        if success:
            if color_model == 'RGB':
                return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return frame
        return None

    # function returns annotated frame
    def find_objects(self, frame):
        pass

    def get_annotated_frame(self, color_model='BGR'):
        frame = self.get_frame(color_model)
        if frame:
            annotated_frame = self.find_objects(frame)
            return annotated_frame
        return frame
