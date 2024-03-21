import os
from langchain.llms.bedrock import Bedrock
import boto3 #import aws sdk and supporting libraries

def get_text_response(prompt_content,uploaded_content,input_content): #text-to-text client function

    bedrock = boto3.client(service_name='bedrock-runtime', region_name="us-east-1")
    
    llm = Bedrock( #create a Bedrock llm client
        # credentials_profile_name=os.environ.get("BWB_PROFILE_NAME"), #sets the profile name to use for AWS credentials (if not the default)
        # region_name=os.environ.get("BWB_REGION_NAME"), #sets the region name (if not the default)
        # endpoint_url=os.environ.get("BWB_ENDPOINT_URL"), #sets the endpoint URL (if necessary)
        client=bedrock,
        model_id="anthropic.claude-v2", #use the Anthropic model
        model_kwargs={"max_tokens_to_sample": 2000, "temperature": 0, "top_p": 1, "stop_sequences": ["\\n\\nHuman:","Question:"]}
    )
    
    print("yeah")
    
    if uploaded_content == "":
        queryString = input_content
    else:
        queryString = f"""Human: {prompt_content}
        
        <Documents>
        {uploaded_content}
        </Documents>
        
        Question:
        {input_content}
        Assistant:
        """
    
    print(queryString)
    
    return llm.predict(queryString) #return a response to the prompt

