from app.dto.webRequest import WebRequest

class YoloDto:
    def __init__(self, img_path = "", label = "", conf = 0.0, x = 0, y = 0, w = 0, h = 0):
        # self._rst_code = rst_code
        self._img_path = img_path
        self._label = label
        self._conf = conf
        self._x = x
        self._y = y
        self._w = w
        self._h = h

    def __str__(self):
        return f'YoloResult(rst_code={self._rst_code}, label={self._label}, conf={self._conf}, x={self._x}, y={self._y}, w={self._w}, h={self._h})'
    
    #@property : getter
    @property
    def get_img_path(self):
        return self._img_path
    
    @property
    def get_label(self):
        return self._label

    @property
    def get_conf(self):
        return self._conf
    
    @property
    def get_x(self):
        return self._x
    
    @property
    def get_y(self):
        return self._y
    
    @property
    def get_w(self):
        return self._w
    
    @property
    def get_h(self):
        return self._h
    
    @get_img_path.setter
    def set_img_path(self, img_path):
        self._img_path = img_path

    @get_label.setter
    def set_label(self, label):
        self._label = label
    
    @get_conf.setter
    def set_conf(self, conf):
        self._conf = conf
        
    @get_x.setter
    def set_x(self, x):
        self._x = x
    
    @get_y.setter
    def set_y(self, y):
        self._y = y
    
    @get_w.setter
    def set_w(self, w):
        self._w = w

    @get_h.setter
    def set_h(self, h):
        self._h = h
