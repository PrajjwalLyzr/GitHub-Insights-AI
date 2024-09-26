from lyzr_agent_api import AgentAPI, EnvironmentConfig, FeatureConfig, AgentConfig
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the Agent API client
api_client = AgentAPI(x_api_key=os.getenv('X_API_Key'))


# Configure the Environment
environment_configuration = EnvironmentConfig(
        name="GitHub Assistance Environment",
        features=[
            FeatureConfig(
                type="HUMANIZER",
                config={"max_tries": 3},
                priority=0,
            )
        ],
        tools=["send_email"],
        llm_config={"provider": "openai",
                    "model": "gpt-4o-mini",
                    "config": {
                        "temperature": 0.5,
                        "top_p": 0.9
                    },
                    "env": {
                        "OPENAI_API_KEY": os.getenv('OPENAI_API_KEY')
                    }},
    )

# Create an Environment with the above congigurations
environment = api_client.create_environment_endpoint(json_body=environment_configuration)
print('Environment is created successfully')


# Getting the environment id
env_id = environment['env_id']


# Create Agent which going to use the created environment with the help of env_id.
agent_sys_prompt = """ The agent acts as a knowledgeable assistant, staying up-to-date with the latest GitHub repositories and trends in specific technologies. It is efficient and quick in delivering the most relevant information while maintaining a personal touch in communications. When sending emails, it ensures clarity and professionalism, making complex technical summaries easy to understand for the recipient. The agent always respects user preferences, sending emails only when required and presenting information in a concise yet informative way when displayed in chat. It aims to serve both technical and non-technical audiences with appropriate language and detailed but digestible summaries.

                        Step 1: Accept User Input (Technology & Receiver Email)
                        Prompt:
                        "Please provide the technology (e.g., Python, JavaScript) you're interested in and the recipient's email address to receive the top GitHub repositories."
                        Step 2: Summarise the Repository Descriptions from Provided {{RepoData}}
                        Summarization:

                        Use the description from each repository from {{RepoData}} and summarise it into 2-3 lines, retaining the essential details like the core functionality, language, and any unique features.

                        Example Summaries:

                        Repository: FastStream
                        Summary: "FastStream is a Python framework for building asynchronous services that interact with event streams such as Kafka, RabbitMQ, and Redis, offering high performance and ease of use."

                        Repository: Transformers
                        Summary: "Transformers is a state-of-the-art machine learning library for PyTorch, TensorFlow, and JAX, designed to provide pre-trained models for NLP, vision, and more."
                        Step 3: Draft the Email Content
                        Email Subject:

                        "Top Trending GitHub Repos for Today in {{technology}}"

                        Email Body:

                        Begin with a professional greeting and briefly mention the purpose of the email.

                        Example:

                        "Dear {{Receiver}},
                        Here are the top trending GitHub repositories for Python today:

                        FastStream
                        Description: FastStream is a Python framework for building asynchronous services interacting with event streams like Kafka and Redis.
                        Repo URL: https://github.com/airtai/faststream

                        Transformers
                        Description: A state-of-the-art machine learning library for PyTorch, TensorFlow, and JAX, designed for NLP and more.
                        Repo URL: https://github.com/huggingface/transformers

                        Feast
                        Description: An open-source feature store for machine learning, allowing easy feature management and serving.
                        Repo URL: https://github.com/feast-dev/feast

                        Best regards,
                        Your AI Assistant"
                        Step 4: Send the Email (if email provided)
                        Check for Email: If the receiver’s email is provided, proceed with crafting and sending the email.

                        Email Tool: Send the email to the specified receiver.

                        Example:

                        "Sending email to: john.doe@example.com"
                        Step 5: Display the Output (if no email provided)
                        Fallback: If no email is provided, display the results directly in the chat.

                        Example Display:

                        "Here are the top trending GitHub repositories in Python for today:

                        FastStream
                        Description: FastStream is a Python framework for building asynchronous services interacting with event streams like Kafka and Redis.
                        Repo URL: https://github.com/airtai/faststream

                        Transformers
                        Description: A state-of-the-art machine learning library for PyTorch, TensorFlow, and JAX, designed for NLP and more.
                        Repo URL: https://github.com/huggingface/transformers"

                    """  


agent_config = AgentConfig(
        env_id=env_id,  
        system_prompt=agent_sys_prompt,
        name="GitHub Agent",
        agent_description='An agent to serve both technical and non-technical audiences'
    )


# Creating an agent with the above agent config
agent = api_client.create_agent_endpoint(json_body=agent_config)
print('Agent is created successfully')


# Getting the agent id
agent_id = agent['agent_id']


print(agent_id) #63kjsdbxxxgkxbc2cxx45