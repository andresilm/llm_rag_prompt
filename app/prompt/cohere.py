import cohere

COHERE_API_KEY = '0gzbXiqJmVIkL3zDTxZ4LHoVccVDBj3R7HreHbNB'


class CoherePrompt:
    def __init__(self):
        self.__cohere_client = cohere.Client(COHERE_API_KEY)

    def ask_question(self, user_input, context):

        prompt = f"""{context}
        Given the information above, answer this question: {user_input}"""

        response = self.__cohere_client.generate(
            prompt=prompt
        )

        return response.generations[0].text.strip()
