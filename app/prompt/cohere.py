import cohere

COHERE_API_KEY = '0gzbXiqJmVIkL3zDTxZ4LHoVccVDBj3R7HreHbNB'


class Prompt:
    def __init__(self):
        self.__cohere_client = cohere.Client(COHERE_API_KEY)

    def ask_question(self, question):
        response = self.__cohere_client.generate(
            model='xlarge',  # Puedes especificar el tamaño del modelo que deseas usar
            prompt=question,
            max_tokens=50  # Define la longitud máxima de la respuesta
        )

        return response.generations[0].text.strip()
