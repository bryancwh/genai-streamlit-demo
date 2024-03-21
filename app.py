import streamlit as st
import json
import boto3

bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)

def claude_prompt_format(prompt: str) -> str:
    # Add headers to start and end of prompt
    prompt_start = "The following is converstation data between Human and AI Assistant "
    return "\n\nHuman: " + prompt_start + prompt + "\n\nAssistant:"
    

def call_claude(prompt):
    prompt_config = {
        "prompt": claude_prompt_format(prompt),
        "max_tokens_to_sample": 4096,
        "temperature": 0.7,
        "top_k": 250,
        "top_p": 0.5,
        "stop_sequences": [],
    }

    body = json.dumps(prompt_config)

    modelId = "anthropic.claude-v2"
    accept = "application/json"
    contentType = "application/json"

    response = bedrock_runtime.invoke_model(
        body=body, modelId=modelId, accept=accept, contentType=contentType
    )
    response_body = json.loads(response.get("body").read())

    results = response_body.get("completion")
    return results

# use SNS to send email to topic
def send(result):
    sns = boto3.client(
        service_name='sns',
        region_name="us-east-1"
    )
    topic_arn = 'arn:aws:sns:us-east-1:889841231043:demoTopic'
    sns.publish(TopicArn=topic_arn, Message=result)
    return result

st.title("Claude AI Demo")
prompt = st.text_area("Enter prompt")

if 'button' not in st.session_state:
    st.session_state['button'] = False

if st.button('Run'):
    if st.session_state.get('button') != True:
        st.session_state['button'] = True

        with st.spinner("Calling Bedrock..."):
            bedrock_result = call_claude(prompt)
            st.session_state['bedrock_result'] = bedrock_result
            st.subheader("Generated response:")
            st.write(bedrock_result)

if st.session_state['button'] == True:

    if st.button("Send Results"):
        send(st.session_state.bedrock_result)
        st.success("Results sent to SQS!")
        st.balloons()
        st.session_state['button'] = False    
    
