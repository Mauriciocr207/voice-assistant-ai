import sounddevice as sd
import numpy as np
import time
from classes import AudioConfig, WakeWordDetectionModel, SpeechToTextModel, LanguageModel
from queue import Queue


class VoiceAssistant:
    """
    Clase principal del asistente de voz.
    Esta clase se encarga de inicializar los modelos y gestionar el flujo de audio.
    """

    def __init__(self):
        # Queues
        self.input_audio = Queue()
        self.text_queue = Queue()
        self.audio_queue = Queue()

        # Models
        self.wwdm = WakeWordDetectionModel()
        self.sttm = SpeechToTextModel()
        self.llm = LanguageModel()

        # audio settings
        self.cooldown_time = 2
        self.is_listening = False
        self.listen_start_time = 0
        self.last_result_time = 0
        self.partial_text = ""

    def start_listening(self):
        with sd.InputStream(
            channels=AudioConfig.CHANNELS.value,
            samplerate=AudioConfig.SAMPLE_RATE.value,
            blocksize=AudioConfig.FRAME_SIZE.value,
            dtype="int16",
            callback=self.wake_word_detection,
        ):
            try:
                print("🟢 Escuchando... Di 'Hey Jarvis'")
                while True:
                    sd.sleep(1000)
            except KeyboardInterrupt:
                print("🔴 Deteniendo...")
                sd.stop()
            except Exception as e:
                print(f"Error: {e}")
                sd.stop()

    def wake_word_detection(self, indata, frames, time_info, status):
        if status:
            print(f"Advertencia en el estado del stream: {status}")

        current_time = time.time()
        audio_modo = indata[:, 0]
        wake_word_detected = self.wwdm.predict(audio_modo)
        allow_activation = current_time - self.last_result_time > self.cooldown_time

        if wake_word_detected and allow_activation:
            print("\n🟢 Activado")
            self.is_listening = True
            self.last_result_time = current_time

        if self.is_listening:
           self.speech_to_text(audio_modo, current_time)

    def speech_to_text(self, audio_mono, current_time):
        """
        Convierte el audio en texto utilizando el modelo de STT.
        """
        audio_bytes = audio_mono.astype(np.int16).tobytes()
        result = self.sttm.recognize(audio_bytes)

        stop_activation = current_time - self.last_result_time > self.cooldown_time

        if stop_activation:
            print("\n🛑 Desactivado")
            voice_input_text = self.partial_text
            self.is_listening = False
            self.partial_text = ""
            self.generate_text_response(voice_input_text)

        if result == "":
            return

        self.partial_text = result
        self.last_result_time = current_time

    def generate_text_response(self, voice_input_text):
        """
        Genera una respuesta de texto utilizando el modelo de lenguaje.
        """

        prompt = f"""
            Q: {voice_input_text}
            Clasify the text intention, your response may include only one of the words following:
            - encender_luz
            - apagar_luz
            - saludar
        """

        print(prompt)

        language_response = self.llm.predict(prompt)

        for r in language_response:
            token = r["choices"][0]["text"]
            print(token, end="")
        
                
            


if __name__ == "__main__":
    VoiceAssistant().generate_text_response("Hola puedes encender la luz");
