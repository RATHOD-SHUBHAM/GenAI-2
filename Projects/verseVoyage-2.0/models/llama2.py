import boto3
import json

class llama2:

    def llama2(self, user_input, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY):

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

        # Todo: API request
        model_Id = "meta.llama2-13b-chat-v1"
        content_Type = 'application/json'
        accept = 'application/json'

        # APIs body
        payload = {
            "prompt":"[INST]" + prompt + user_input + "[/INST]",
            "max_gen_len":512,
            "temperature":1.0,
            "top_p":0.9
        }

        body = json.dumps(payload)

        response = bedrock.invoke_model(
            modelId = model_Id,
            contentType = content_Type,
            accept = accept,
            body=body
        )


        response_body = json.loads(response.get("body").read())


        response_text = response_body['generation']

        return response_text


