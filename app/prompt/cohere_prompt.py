
class CoherePrompt:
    def __init__(self, client):
        self.__cohere_client = client

    def ask_question(self, user_input, context):

        prompt = f"""Context: {context}\n.
        Given the information above, answer this question: 
        \"{user_input}\" . 
        The answer must meet this requirements:
        - Use just one sentence.
        - Use same language as the question.
        - Add emojis in the sentence that summarize its content.
        - Always respond in the third person. 
        """
        # temperature=0 => determinism
        response = self.__cohere_client.generate(prompt=prompt, temperature=0)

        return response.generations[0].text.strip()
