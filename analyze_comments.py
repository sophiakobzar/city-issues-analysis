import random
import json
from datetime import datetime, timedelta
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI
import autogen
from config import AZURE_OPENAI_API_KEY, AZURE_OPENAI_API_VERSION, AZURE_OPENAI_API_BASE, AZURE_OPENAI_DEPLOYMENT_NAME
import sys
import os

# Azure OpenAI client setup
client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_API_BASE
)

# Azure OpenAI configuration for AutoGen
config_list = [
    {
        "model": AZURE_OPENAI_DEPLOYMENT_NAME,
        "api_key": AZURE_OPENAI_API_KEY,
        "base_url": AZURE_OPENAI_API_BASE,
        "api_type": "azure",
        "api_version": AZURE_OPENAI_API_VERSION,
    }
]

# AutoGen agent setup
content_creation_agent = autogen.AssistantAgent(
    name="ContentCreationAgent",
    llm_config={"config_list": config_list},
    system_message="You are an expert in analyzing comments and identifying topics, phrases, and sentiment. response in Json only"
)

user_proxy = autogen.UserProxyAgent(
    name="UserProxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=0,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "coding", "use_docker": False},
)

# Function to generate synthetic comments with timestamps
def generate_synthetic_comments(num_comments=50):
    topics = ["traffic", "homelessness", "drug use"]
    
    # Predefined comments for each topic
    traffic_comments = [
        "The traffic in the city is unbearable. It takes me hours to get to work every day. Something needs to be done about this!",
        "I've noticed less traffic on the roads lately, thanks to the improved public transit system.",
        "Traffic congestion is getting worse every day. We need better infrastructure to handle the growing number of vehicles.",
        "With more people using bikes and public transport, the traffic situation has improved significantly.",
        "The new traffic management system has really helped in reducing congestion during peak hours.",
        "Traffic jams are a daily nightmare. It's affecting my mental health and productivity.",
        "The city's traffic lights are poorly synchronized, causing unnecessary delays.",
        "Road construction projects are causing severe traffic disruptions. It's frustrating!",
        "The lack of parking spaces is making traffic even worse. We need better solutions.",
        "Rush hour traffic is unbearable. I dread driving during peak times.",
        "The constant honking and noise from traffic is driving me crazy.",
        "The pollution from all the traffic is making it hard to breathe.",
        "Traffic accidents are becoming more frequent. It's dangerous out there.",
        "The traffic situation is so bad that it's affecting local businesses.",
        "The roads are in terrible condition, adding to the traffic woes."
    ]
    
    homelessness_comments = [
        "I've noticed an increase in homelessness in our neighborhood. It's heartbreaking to see so many people without a place to live. We need more support for them.",
        "The new shelter program has really made a difference in reducing homelessness in our area.",
        "Homelessness is a growing issue that needs immediate attention from the authorities.",
        "It's great to see more community initiatives aimed at helping the homeless population.",
        "We need more affordable housing options to tackle the issue of homelessness effectively.",
        "The number of homeless people on the streets is alarming. We need urgent action.",
        "Homelessness is affecting the safety and cleanliness of our neighborhood.",
        "The lack of resources for homeless individuals is a serious problem. We need more funding.",
        "Seeing homeless families with children is heartbreaking. We must do better.",
        "Homelessness is a complex issue that requires comprehensive solutions.",
        "The increase in homeless encampments is concerning. It's not safe.",
        "The homeless crisis is getting worse, and it's impacting everyone.",
        "There are not enough shelters to accommodate the growing homeless population.",
        "The sight of homeless people sleeping on the streets is distressing.",
        "Homelessness is a humanitarian crisis that needs more attention."
    ]
    
    drug_use_comments = [
        "Drug use in public places is becoming a serious issue. It's not safe for our children to play outside anymore. We need stricter regulations.",
        "I've noticed a decrease in drug use in our neighborhood, thanks to the new community outreach programs.",
        "Public drug use is a major concern that needs to be addressed urgently.",
        "The new rehabilitation centers have really helped in reducing drug use in our area.",
        "We need more awareness programs to educate people about the dangers of drug use.",
        "Drug use is rampant in certain areas of the city. It's dangerous and needs immediate attention.",
        "The presence of drug users in parks and public spaces is unsettling. We need better enforcement.",
        "Drug-related crime is on the rise. It's affecting the safety of our community.",
        "The availability of drugs on the streets is alarming. We need stronger measures to combat this issue.",
        "Drug addiction is tearing families apart. We need more support for those affected.",
        "The sight of people using drugs openly is disturbing.",
        "Drug use is leading to an increase in petty crimes in the area.",
        "The community is suffering because of the widespread drug use.",
        "There are not enough rehab centers to help those struggling with drug addiction.",
        "The drug problem is getting out of hand. We need immediate intervention."
    ]
    
    comments = []
    current_time = datetime.now()
    for _ in range(num_comments):
        topic = random.choice(topics)
        if topic == "traffic":
            comment = random.choice(traffic_comments)
        elif topic == "homelessness":
            comment = random.choice(homelessness_comments)
        elif topic == "drug use":
            comment = random.choice(drug_use_comments)
        # Add a timestamp to each comment
        timestamp = current_time - timedelta(minutes=random.randint(0, 10080))  # Random time within the last 7 days
        comments.append({"comment": comment, "timestamp": timestamp.isoformat()})
    
    return comments

def clean_json_string(json_string):
    # Remove the triple backticks and the word 'json'
    cleaned_string = json_string.replace("```json", "").replace("```", "")
    return cleaned_string

comments = generate_synthetic_comments()
user_message = f"""
User: I need to classify the topic of the comment as either Traffic, Homelessness, or Drug Use. Additionally, I need a sentiment analysis with a numerical value ranging from -1 to 1, where -1 represents very negative, 0 represents neutral, and 1 represents very positive. The sentiment value should be distributed across the range from -1 to 1, not just at the extremes. Please include the comment, sentiment value, topic, and timestamp in the response, formatted as JSON.
Data: {json.dumps(comments)}
"""
# Suppress output
with open(os.devnull, 'w') as fnull:
    sys.stdout = fnull
    sys.stderr = fnull
    user_proxy.initiate_chat(content_creation_agent, message=user_message)
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

chat_response = content_creation_agent.last_message()["content"]
cleaned_json = clean_json_string(chat_response)
# Print only the JSON response from chat agent
print(cleaned_json)