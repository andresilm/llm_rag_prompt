import cohere

COHERE_API_KEY = '0gzbXiqJmVIkL3zDTxZ4LHoVccVDBj3R7HreHbNB'


class CoherePrompt:
    def __init__(self):
        self.__cohere_client = cohere.Client(COHERE_API_KEY)

    def ask_question(self, user_input, context):

        prompt = f"""Context: {context}\n.
        Given the information above, answer this question: 
        \"{user_input}\" . 
        The answer must meet this requirements:
        - Answer in just one sentence.
        - The language must be the same as the one in which the question is asked.
        - Add emojis in the sentence that summarize its content.
        - Always respond in the third person. 
        """

        response = self.__cohere_client.generate(prompt=prompt, temperature=0)  # temperature=0 ==> determinism

        return response.generations[0].text.strip()
