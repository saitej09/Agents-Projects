import os
import streamlit as st
from crewai import Agent, Crew, Process, Task, LLM
from crew import AgenticRag
from tools.document_search_tool import DocumentSearchTool
import time
import base64
import tempfile
import gc

st.set_page_config(page_icon="🔍", layout="wide")


# class AgentCrew:

#     def __init__(self, query, temperature=0.7, model="gpt-4o-mini"):
#         self.query = query
#         self.temperature = temperature
#         self.model = model
#         self.output = st.empty()
#         pass

#     def run(self):
#         """
#         Run the crew.
#         """
#         inputs = {"query": self.query}

#         try:
#             query_response = (
#                 AgenticRag(temperature=self.temperature, model=self.model)
#                 .crew()
#                 .kickoff(inputs=inputs)
#             )
#             self.output.markdown(query_response)
#         except Exception as e:
#             raise Exception(f"An error occurred while running the crew: {e}")

#         return self.output


if __name__ == "__main__":

    if "messages" not in st.session_state:
        st.session_state.messages = []  # Chat history

    if "crew" not in st.session_state:
        st.session_state.crew = None  # Store the Crew object

    if "vector_search_tool" not in st.session_state:
        st.session_state.vector_search_tool = None  # Store the DocumentSearchTool

    def reset_chat():
        st.session_state.messages = []
        gc.collect()

    def display_pdf(file_bytes: bytes, file_name: str):
        """Displays the uploaded PDF in an iframe."""
        base64_pdf = base64.b64encode(file_bytes).decode("utf-8")
        pdf_display = f"""
        <iframe 
            src="data:application/pdf;base64,{base64_pdf}" 
            width="100%" 
            height="600px" 
            type="application/pdf"
        >
        </iframe>
        """
        st.markdown(f"### Preview of {file_name}")
        st.markdown(pdf_display, unsafe_allow_html=True)

    with st.sidebar:
        st.header("Add Your PDF Document")
        uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

        if uploaded_file is not None:
            # If there's a new file and we haven't set pdf_tool yet...
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_file_path = os.path.join(temp_dir, uploaded_file.name)
                with open(temp_file_path, "wb") as f:
                    f.write(uploaded_file.getvalue())
                with st.spinner("Indexing PDF... Please wait..."):
                    st.session_state.vector_search_tool = DocumentSearchTool(
                        doc_file_path=temp_file_path
                    )
                    
                
            st.success("PDF indexed! Ready to chat.")
            print(
                f"collections after indexing:  {st.session_state.vector_search_tool.client.get_collections()}"
            )
        st.button("Clear Chat", on_click=reset_chat)

    st.markdown("Chat powered by Agentic RAG ..")
    # if uploaded_file is not None:
    #     display_pdf(uploaded_file.getvalue(), uploaded_file.name)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    query = st.chat_input("Ask a question about your PDF...")

    if query:
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        if st.session_state.crew is None:
            st.session_state.crew = AgenticRag(st.session_state.vector_search_tool)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            with st.spinner("Thinking..."):
                inputs = {"query": query}
                result = st.session_state.crew.crew().kickoff(inputs=inputs).raw

            # Split by lines first to preserve code blocks and other markdown
            lines = result.split("\n")
            for i, line in enumerate(lines):
                full_response += line
                if i < len(lines) - 1:  # Don't add newline to the last line
                    full_response += "\n"
                message_placeholder.markdown(full_response + "▌")
                time.sleep(0.15)  # Adjust the speed as needed

            message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": result})
