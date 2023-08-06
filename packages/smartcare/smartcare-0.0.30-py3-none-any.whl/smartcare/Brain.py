import os
import tensorflow as tf
from keras.models import load_model
from .Config import Config

class Brain:

    def __init__(self, mode=0):
        self.modeSwitcher = {
            0: Config.get("CNN_DEFAULT_MODEL")
        }
        self.model = None
        self.init(self.modeSwitcher[mode])
    def init(self, mode):
        tf.get_logger().setLevel('ERROR')
        tf.autograph.set_verbosity(0)
        self.model = load_model(mode)

    def predict(self, image):
        prediction = self.model.predict(image)
        result = {
            True: "Wandering",
            False: "Not Wandering"
        }
        prediction = [prediction > 0.5]
        return result[prediction[0][0][0]]

    def predict_profiler(self, image):
        tf.profiler.experimental.start(Config.get("LOGS_FOLDER"))
        self.model.predict(image)
        tf.profiler.experimental.stop()