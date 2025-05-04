from enum import Enum

class AudioConfig(Enum):
    CHANNELS = 1
    SAMPLE_RATE = 16000
    FRAME_DURATION_MS = 200
    FRAME_SIZE = int(SAMPLE_RATE * (FRAME_DURATION_MS / 1000))
    COOLDOWN_TIME = 2
