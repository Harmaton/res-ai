# Resufix

## Overview
Resufix is an intelligent resume analyzer built using Natural Language Processing (NLP) capabilities. The application uses OpenAI's GPT-4 API to understand the context of uploaded documents (resumes) and answer questions related to it.

## How it Works

- Users log in and upload their resumes in PDF, DOCX, or TXT formats.
- The app reads the uploaded resume and extracts the text content.
- The extracted text is split into smaller chunks.
- Each text chunk is encoded into an embedding using the GPT-4 model and stored in a Pinecone vector index for similarity search.
- The app runs a series of predefined queries on the index to extract specific information like contact details and to identify spelling or grammatical errors.
- It can also generate an improved version of the resume based on its analysis.
- Additionally, the app provides an interface for users to ask custom questions about their resumes.

## Installation & Setup

1. Clone this repository:


2. Navigate to the directory: 

```   cd resufix ```


3. Install the required packages:

 ``` pip install -r requirements.txt ```

4. Ensure you have a Pinecone API key and initialize Pinecone:

```python
pinecone.init(
    api_key="your-pinecone-api-key",
    environment='northamerica-northeast1-gcp'
)
```

## Usage 

``` python -m streamlit app.py```

enter any login detail and proceed

