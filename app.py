import os 
import streamlit as st
import pandas as pd
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
import matplotlib


matplotlib.use('TkAgg')
def main():
    api_key = st.sidebar.text_input(
        label="#### Your OpenAI API key 👇",
        placeholder="Paste your openAI API key, sk-",
        type="password")

    llm = OpenAI(api_token=api_key)
    pandas_ai = PandasAI(llm)

    st.markdown("<h1 style='text-align: center; font-weight:bold; font-family:comic sans ms; padding-top: 0rem; color: grey;'>Chat2VIS</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; padding-top: 0rem; color: grey;'>Creating Visualisations using Natural Language with ChatGPT </h2>", unsafe_allow_html=True)

    with st.sidebar:
        # Choose your dataset
        st.write(":bar_chart: Choose your data:")

        # Add facility to upload a dataset
        uploaded_file = st.file_uploader(":computer: Load a CSV file:", type="csv")

    if uploaded_file:
        # Read in the uploaded CSV file and add it to the list of available datasets
        file_name = uploaded_file.name[:-4].capitalize()
        df = pd.read_csv(uploaded_file)
        
        # Display the first 5 rows of the loaded dataset
        st.write(df.head(5))
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Accept user input
        if prompt := st.chat_input("Ask your questions?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.spinner("Generating ...."):  # Place the spinner here
                response = pandas_ai.run(df, prompt=prompt)
                
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.write(response)
            
if __name__ == '__main__':
    main()
