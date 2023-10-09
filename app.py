import os 
import streamlit as st
import pandas as pd
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
import matplotlib.pyplot as plt
import matplotlib
from pandasai import SmartDataframe, SmartDatalake
from pandasai.responses.streamlit_response import StreamlitResponse
import time

# Define a function to clear the chat history
def clear_chat_history():
    st.session_state.messages = []

matplotlib.use('Agg')
def main():
    api_key = st.sidebar.text_input(
        label="#### Your OpenAI API key 👇",
        placeholder="Paste your openAI API key, sk-",
        type="password")
    if not api_key:
        st.warning("Please provide your OpenAI API key to run this app.")
        st.stop()  # Stop execution if API key is not provided

    llm = OpenAI(api_token=api_key)

    st.markdown("<h1 style='text-align: center; font-weight:bold; font-family:comic sans ms; padding-top: 0rem; color: grey;'>Chat2VIS</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; padding-top: 0rem; color: grey;'>Creating Visualisations using Natural Language </h2>", unsafe_allow_html=True)

    with st.sidebar:
        # Choose your dataset
        st.write(":bar_chart: Choose your data:")

        # Add facility to upload a dataset
        uploaded_file = st.file_uploader(":computer: Load a CSV file:", type="csv")

        # Add a "Reset" button
        if st.button("Reset Chat"):
            clear_chat_history()

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file, low_memory=False)
            df = SmartDatalake(
            [df],
            config={"llm": llm, "verbose": True, "response_parser": StreamlitResponse},
        )
            print("dnidbeo",df)
            # Convert SmartDatalake to DataFrame
            # df = df.to_dataframe()
            print("ecece3d",df)

            # Initialize chat history
            if "messages" not in st.session_state:
                st.session_state.messages = []

            # Display chat messages from history on app rerun
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # Accept user input
            if prompt := st.chat_input("Ask your questions?"):
                start_time = time.time()
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.spinner("Generating ...."):  # Place the spinner here
                    response = df.chat(query=prompt)
                    end_time = time.time()
                    execution_time = end_time - start_time
                    
                st.session_state.messages.append({"role": "assistant", "content": response})
                with st.chat_message("assistant"):
                    if isinstance(response, plt.Figure):
                        st.pyplot(response)
                    else:
                        st.write(response)
                st.write("Execution time:", execution_time, "seconds")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            
            
if __name__ == '__main__':
    main()
