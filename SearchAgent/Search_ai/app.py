# import streamlit as st
# from langchain_groq import ChatGroq
# from langchain_community.utilities import ArxivAPIWrapper,WikipediaAPIWrapper
# from langchain_community.tools import ArxivQueryRun,WikipediaQueryRun,DuckDuckGoSearchRun
# from langchain.agents import initialize_agent,AgentType
# from langchain.callbacks import StreamlitCallbackHandler
# import os
# from dotenv import load_dotenv

# ## Arxiv and wikipedia Tools
# arxiv_wrapper=ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=200)
# arxiv=ArxivQueryRun(api_wrapper=arxiv_wrapper)

# api_wrapper=WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=200)
# wiki=WikipediaQueryRun(api_wrapper=api_wrapper)

# search=DuckDuckGoSearchRun(name="Search")


# st.title("🔎 LangChain - Chat with search")
# """
# In this example, we're using `StreamlitCallbackHandler` to display the thoughts and actions of an agent in an interactive Streamlit app.
# Try more LangChain 🤝 Streamlit Agent examples at [github.com/langchain-ai/streamlit-agent](https://github.com/langchain-ai/streamlit-agent).
# """

# ## Sidebar for settings
# st.sidebar.title("Settings")
# api_key=st.sidebar.text_input("Enter your Groq API Key:",type="password")

# if "messages" not in st.session_state:
#     st.session_state["messages"]=[
#         {"role":"assisstant","content":"Hi,I'm a chatbot who can search the web. How can I help you?"}
#     ]

# for msg in st.session_state.messages:
#     st.chat_message(msg["role"]).write(msg['content'])

# if prompt:=st.chat_input(placeholder="What is machine learning?"):
#     st.session_state.messages.append({"role":"user","content":prompt})
#     st.chat_message("user").write(prompt)

#     llm=ChatGroq(groq_api_key=api_key,model_name="Llama3-8b-8192",streaming=True)
#     tools=[search,arxiv,wiki]

#     search_agent=initialize_agent(tools,llm,agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,handling_parsing_errors=True)

#     with st.chat_message("assistant"):
#         st_cb=StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
#         response=search_agent.run(st.session_state.messages,callbacks=[st_cb])
#         st.session_state.messages.append({'role':'assistant',"content":response})
#         st.write(response)

import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, DuckDuckGoSearchRun
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler

st.set_page_config(page_title="LangChain Chat with Search", page_icon="🔎")

st.title("🔎 LangChain - Chat with search")
st.markdown("""
In this example, we're using `StreamlitCallbackHandler` to display the thoughts and actions of an agent in an interactive Streamlit app.
Try more LangChain 🤝 Streamlit Agent examples at [github.com/langchain-ai/streamlit-agent](https://github.com/langchain-ai/streamlit-agent).
""")

# Sidebar for settings
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your Groq API Key:", type="password")

# Initialize tools
arxiv_wrapper = ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=200)
arxiv = ArxivQueryRun(api_wrapper=arxiv_wrapper)

wiki_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=200)
wiki = WikipediaQueryRun(api_wrapper=wiki_wrapper)

search = DuckDuckGoSearchRun(name="Search")

tools = [search, arxiv, wiki]

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a chatbot who can search the web, Wikipedia, and academic papers. How can I help you?"}
    ]

# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Chat input
if prompt := st.chat_input(placeholder="Ask me anything!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if not api_key:
        st.warning("Please enter your Groq API Key in the sidebar.")
    else:
        try:
            llm = ChatGroq(
                groq_api_key=api_key,
                model_name="Llama3-8b-8192",
                streaming=True
            )
            search_agent = initialize_agent(
                tools,
                llm,
                agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                handle_parsing_errors=True
            )

            with st.chat_message("assistant"):
                st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
                # Only pass the latest prompt, not the whole history!
                response = search_agent.run(prompt, callbacks=[st_cb])
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.write(response)
        except Exception as e:
            st.error(f"⚠️ Error: {e}")

