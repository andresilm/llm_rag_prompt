
class Cohere:
    def __init__(self, client):
        self.__cohere_client = client

    def ask_question(self, user_input, context):

        prompt = f"""Context: {context}\n.
        Given the information above, answer this question: 
        \"{user_input}\" . 
        If the question is in spanish, the answer must be in spanish.
        If the question is in english, the answer must be in english.
        If the question is in portuguese, the answer must be in portuguese.
        I need the answer in just one sentence, and add emojis to complement the answer.
        The way the answer is written must be in third person.
        """
        # temperature=0 => determinism
        response = self.__cohere_client.generate(prompt=prompt, temperature=0)

        return response.generations[0].text.strip()
