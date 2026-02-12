import cv2 as cv

class Camera:

    def __init__(self):
        self.camera = cv.VideoCapture(0)
        if not self.camera.isOpened():
            raise ValueError("Camera not found")
        
        # Try to set HD resolution
        self.camera.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
        self.camera.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
        
        self.width = self.camera.get(cv.CAP_PROP_FRAME_WIDTH)
        self.height = self.camera.get(cv.CAP_PROP_FRAME_HEIGHT)

    def __del__(self):
        if self.camera.isOpened():
            self.camera.release()
    
    def get_frame(self):
        if self.camera.isOpened():
            ret, frame = self.camera.read()
            
            if ret:
                return (ret, cv.cvtColor(frame, cv.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return None 