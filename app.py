import os
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.callbacks import StreamlitCallbackHandler
import streamlit as st

load_dotenv()

llm = OpenAI(temperature=0, streaming=True,
             openai_api_key=os.getenv("OPENAI_API_KEY"))
tools = load_tools(["ddg-search"])
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)


def main():
    st.set_page_config(page_title="AI Chat App", page_icon="🤖")
    st.header("AI chat app 🤖")

    # try: "what are the names of the kids of the 44th president of america"
    # try: "top 3 largest shareholders of nvidia"
    if prompt := st.chat_input():
        st.chat_message("user").write(prompt)
        with st.chat_message("assistant"):
            st.write("🧠 thinking...")
            st_callback = StreamlitCallbackHandler(st.container())
            response = agent.run(prompt, callbacks=[st_callback])
            st.write(response)


if __name__ == '__main__':
    main()
