import abc


class INetworkLLM(abc.ABC):
    @abc.abstractmethod
    def ask_question(self, user_input, context):
        raise NotImplementedError


class Cohere(INetworkLLM):
    def __init__(self, client):
        self.__cohere_client = client

    def ask_question(self, user_input, context):

        prompt = f"""Document: {context}\n.
        Given the text from a document, extract information and complete these fields: 
        
        *deal_name
        *total_deal_amount
        *start_date
        *end_date
        *description
        *objectives
        *kpi
        *target_audience
        *geo_targeting
        
        Please format the answer as a JSON file
        """
        # temperature=0 => determinism
        response = self.__cohere_client.generate(prompt=prompt, temperature=0)

        response = response.generations[0].text.strip()

        return response
