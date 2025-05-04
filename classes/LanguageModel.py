from llama_cpp import Llama


class LanguageModel():
    """
    A class to represent a language model.
    """

    def __init__(self):
        """
        Initializes the LanguageModel with a name and a model.

        Args:
            name (str): The name of the language model.
            model (str): The model of the language model.
        """
        self.model = Llama(
            model_path="./resources/qwen2.5-0.5b-instruct-q8_0.gguf",
            verbose=False
        )
        self.chat_history = []

    def predict(self, prompt: str) -> str:
        


        return self.model(
            prompt,
            stream=True
        )
