import streamlit as st
from googlesearch import search
import requests
from bs4 import BeautifulSoup
from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import PromptTemplate
import os
from langchain.chains import LLMChain

from langchain_groq import ChatGroq
GROQ_API_KEY = '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'
llm = ChatGroq(temperature=0.8, groq_api_key=GROQ_API_KEY, model_name="llama3-70b-8192")



os.environ['SSL_CERT_FILE'] = 'C:\\Users\\RSPRASAD\\AppData\\Local\\.certifi\\cacert.pem'

def extract_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        # Extract text content
        paragraphs = soup.find_all('p')
        content = " ".join([p.get_text() for p in paragraphs])
        return content
    except Exception as e:
        return f"Error fetching content from {url}: {e}"

def get_top_search_results(query, num_results=3):
    return list(search(query, num_results=num_results, lang="en"))

def answer_question_from_content(question, content):

    # messages=[
    #        ( "system", "You are a helpful assistant skilled in solving assignment problems using linear programming.", ),
    #         ( "human",content),
    #     ]
    content = content[:5000]
    prompt = f"Based on the following content, answer the question: {content}\n\nQuestion: {question}"
    template = PromptTemplate(
                input_variables=["content"],
                template=prompt,
            )

            # Create the LLMChain to manage the model and prompt interaction
    llm_chain = LLMChain(prompt=template, llm=llm)
    response = llm_chain.invoke({
        "content" : content
    })          
        
    # messages=[
    #             {"role": "system", "content": "You are a helpful assistant."},
    #             {"role": "user", "content": f"Based on the following content, answer the question: {content}\n\nQuestion: {question}"}
    #         ]
    # response = llm.invoke(messages)
    # # st.write(response)
    # st.write(response)
    return(response["text"])
    # return(response.content)


st.title("Google Search and LLM Question Answering")

# User input
query = st.text_input("Enter your query:", "")

if query:
    st.write(f"Searching for: {query}")

    # Get top 3 search results
    search_results = get_top_search_results(query, num_results=3)
    st.write("Top 3 URLs:")
    for url in search_results:
        st.write(url)

    # Extract content from URLs
    extracted_contents = []
    for url in search_results:
        content = extract_text_from_url(url)
        extracted_contents.append(content)

    # Combine content for LLM
    combined_content = "\n\n".join(extracted_contents)

    # Ask LLM to answer question
    if combined_content.strip():
        st.write("Extracted content from top URLs:")
        # st.text_area("Content", combined_content, height=300)

        st.write("Generating answer...")
        answer = answer_question_from_content(query, combined_content)
        st.write("### Answer:")
        st.write(answer)
    else:
        st.write("No content extracted from the URLs.")
