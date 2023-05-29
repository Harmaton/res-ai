# Import dependencies
import os
import PyPDF2
import docx2txt
from apikey import apikey
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS, Pinecone
from langchain.text_splitter import CharacterTextSplitter
import pinecone
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
import streamlit as st


os.environ['OPENAI_API_KEY'] = apikey


# Initialize PineCone
pinecone.init(
    api_key="5a806557-5de4-443d-ab12-414e25957273",
    environment='northamerica-northeast1-gcp'
)
index_name = "resufix"


st.title("Resufix")

menu = ["Home", "Login", "SignUp"]
choice = st.sidebar.selectbox("menu", menu)

if choice == "Home":
    st.subheader("Landing Page 😎 ...")
    st.text("Loading ")
    
elif choice == "Login":
    st.subheader("Login Section 🤖")
    st.text("Interactive components ...")

    username = st.sidebar.text_input("User Name")
    password = st.sidebar.text_input("Password", type = 'password')

    if st.sidebar.checkbox("Login"):

        st.title('Resume Analyzer 📙 😎')
        st.subheader('Only PDF, Word and text formats are accepted! 🤖')
        uploaded_file = st.file_uploader("Upload your resume and ask about it", type=['pdf', 'docx', 'txt'])

        if uploaded_file:
            # Read data from the uploaded file
            file_extension = uploaded_file.name.split('.')[-1]

            if file_extension == 'pdf':
                doc_reader = PyPDF2.PdfFileReader(uploaded_file)
                raw_text = ''
                for i, page in enumerate(doc_reader.pages):
                    text = page.extract_text()
                    if text:
                        raw_text += text
            elif file_extension == 'docx':
                raw_text = docx2txt.process(uploaded_file)
            else:  # txt file
                raw_text = uploaded_file.read().decode("utf-8")

            # Splitting the Text
            text_splitter = CharacterTextSplitter(
                separator="\n",
                chunk_size=1000,
                chunk_overlap=20,  # striding over the text
                length_function=len
            )
            texts = text_splitter.split_text(raw_text)

            # Making the embeddings
            embeddings = OpenAIEmbeddings()

            cvSearch = Pinecone.from_texts(texts, embeddings, index_name=index_name)

            #1. Static Query on the Docs
            llm = OpenAI(temperature=1, openai_api_key=apikey)
            chain = load_qa_chain(llm, chain_type="stuff")

            #Contact details
            st.divider()
            Contact_details = "Contact details"
            st.header(Contact_details)
            query = "What are the contact details of this resume owner?"
            search = cvSearch.similarity_search(query, include_metadata=True)
            st.write(chain.run(input_documents=search, question=query))

            #Spelling Errors
            st.divider()
            spelling_errors = "Spelling Errors"
            st.header(spelling_errors)
            query2 = "Are there any spelling errors in this resume/document?"
            search2 = cvSearch.similarity_search(query2, include_metadata=True)
            st.write(chain.run(input_documents=search2, question=query2))

            #Grammatical Errors
            st.divider()
            grammatical_errors = "Grammatical Errors"
            st.header(grammatical_errors)
            query3 = "what are the grammatical_errors errors in this resume/document?"
            search3 = cvSearch.similarity_search(query3, include_metadata=True)
            st.write(chain.run(input_documents=search3, question=query3))

            #My Improvements on the CV
            st.divider()
            my_version = "My Improvements on the CV"
            st.header(my_version)
            query4= "Paraphrase the document and edit to improve the grammar, any spelling errors, add any other correction to make the CV better in the eyes of the employer or HR. Improve everything from Introduction to finish"
            search4 = cvSearch.similarity_search(query4, include_metadata=True)
            st.write(chain.run(input_documents=search4, question=query4))

            st.text('🤠😕')

            #2. Chat on the Docs
            st.divider()
            st.divider()
            st.header("Q & A")
            label1 = "✍️ Write down your question Question:"
            quiz1 = st.text_input(label = label1, value = "Any Question you want me to answer based on your CV ?", max_chars=20, placeholder= "Any Question you want me to answer based on your CV")
            search5 = cvSearch.similarity_search(quiz1, include_metadata=True)
            st.write(chain.run(input_documents=search5 , question=query4))



