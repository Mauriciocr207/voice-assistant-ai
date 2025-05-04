from openwakeword.model import Model
import openwakeword.utils
from enum import Enum
from .constants import Config

class WakeWordDetectionConfig(Enum):
    MODEL_DIR = str(Config.RESOURCES_DIR.value / "openwakeword-models")
    MODEL_NAME = "hey_jarvis_v0.1"
    MODEL_PATH = f"{MODEL_DIR}/{MODEL_NAME}.tflite"

openwakeword.utils.download_models(
    model_names=[WakeWordDetectionConfig.MODEL_NAME.value],
    # target_directory=WakeWordDetectionConfig.MODEL_DIR.value,
)

class WakeWordDetectionModel:
    def __init__(self):
        print(WakeWordDetectionConfig.MODEL_PATH.value)
        self.model = Model(wakeword_models=[WakeWordDetectionConfig.MODEL_PATH.value])

    def predict(self, audio_data):
        prediction = self.model.predict(audio_data)
        probability = float(prediction.get(WakeWordDetectionConfig.MODEL_NAME.value, 0.0))

        return True if probability > 0.5 else False
