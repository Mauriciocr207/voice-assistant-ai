from vosk import Model, KaldiRecognizer
from .constants import Config
from enum import Enum
import json

class SpeechToTextConfig(Enum):
    MODEL_PATH = str(Config.RESOURCES_DIR.value / "vosk-model-small-es-0.42")

class SpeechToTextModel:
    def __init__(self):
        self.model_name = Model(model_path=SpeechToTextConfig.MODEL_PATH.value)
        self.recognizer = KaldiRecognizer(self.model_name, 16000)
        
    def recognize(self, audio_data):
        if self.recognizer.AcceptWaveform(audio_data):
            result = self.recognizer.Result()
        else:
            result = self.recognizer.PartialResult()
        
        result_dict = json.loads(result)

        return result_dict.get("text", "") or result_dict.get("partial", "")
        
        