import streamlit as st
import os
from lyzr_agent_api import AgentAPI, ChatRequest
from template import emailtemplate
from scrapper import scrape_repos_and_get_readme, repo_scrapper
from utils import page_config, style_app, template_end, about_app, social_media

from dotenv import load_dotenv

load_dotenv()

LYZR_API_KEY = os.getenv('X_API_Key')
Agent_ID = os.getenv('AGENT_ID')
User_ID = os.getenv('USER_ID')
Session_ID = os.getenv('SESSION_ID')


page_config()
style_app()


image = "src/logo/lyzr-logo-light.png"
st.image(image=image, width=200)

st.header("GitHub Insights Assistant")
st.markdown("##### Powered by [Lyzr Agent API](https://agent.api.lyzr.app/docs#overview)")
st.markdown('---')



col1, col2 = st.columns(2)
with col1:
    Receiveremail = st.text_input(label="Provide receiver email", placeholder="example@google.com")

with col2:
    Technology = st.text_input(label='Provide your technology', placeholder="Like.. (Python, JavaScript, Java)")
    

if st.button('Send Email'):
    if (Receiveremail and Technology):
        with st.spinner(f'🤖 Agent is Getting Data regarding {Technology}'):
            tech = Technology.lower()
            EmailTemplate = emailtemplate()
            scrapped_repo_data = repo_scrapper(technology=tech)
            RepoData = scrape_repos_and_get_readme(repo_data=scrapped_repo_data)
            if RepoData:
                with st.spinner(f'🤖Agent Sending Mail to {Receiveremail}'):
                    api_client = AgentAPI(x_api_key=LYZR_API_KEY)

                    chatpayload = ChatRequest(
                        user_id=User_ID,
                        agent_id=Agent_ID,
                        message=f"Summarise the repository description from this data:{RepoData}, use this email template to draft an email: {EmailTemplate},and send mail to:{Receiveremail}",
                        session_id=Session_ID
                    )

                    response = api_client.chat_with_agent(json_body=chatpayload)
                    if response:
                        st.write('🤖Agent Successfully send the mail')

    else:
        st.warning('Please provide the data first')


template_end()
st.sidebar.markdown('---')
about_app()
st.sidebar.markdown('---')
social_media(justify="space-evenly")