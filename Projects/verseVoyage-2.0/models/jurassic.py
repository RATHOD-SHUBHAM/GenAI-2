import boto3
import json

class jurassic:

    def jurassic(self, user_input, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY):

        bedrock = boto3.client(service_name='bedrock-runtime',
                               region_name="us-east-1",
                               aws_access_key_id=AWS_ACCESS_KEY_ID,
                               aws_secret_access_key=AWS_SECRET_ACCESS_KEY
                               )

        user_input = user_input

        prompt = """
            You are an imaginative, humorous, romantic, and intelligent poet. 
            You are comparable to Shakespeare.
        
            Your task is to write poetry about .
        """

        # Todo: API Request

        model_Id = 'ai21.j2-mid-v1'
        content_Type = "application/json"
        accept = "application/json"

        ### Apis body
        payload = {
            "prompt":prompt + user_input,
            "maxTokens":512,
            "temperature":0.8,
            "topP":0.9
        }
        body=json.dumps(payload)


        response = bedrock.invoke_model(
            modelId=model_Id,
            contentType=content_Type,
            accept=accept,
            body=body
        )

        response_body = json.loads(response.get('body').read())


        # text
        response_text = response_body.get('completions')[0].get('data').get('text')
        return response_text