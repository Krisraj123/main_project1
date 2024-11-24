import os
import transformers
import torch
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.llms import HuggingFaceHub
from huggingface_hub import InferenceClient
import gradio as gr

# Initialize the InferenceClient with your API key
client = InferenceClient(api_key="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")

# Parameters for the Qwen model
gen_params = {
    "max_tokens": 512,
    "temperature": 0.7
}

# Global variables
conversation_retrieval_chain = None
llm_hub = None
embeddings = None

# Function to initialize the language model and its embeddings
def init_llm():
    global llm_hub, embeddings

    # Set up the environment variable for HuggingFace and initialize the desired model
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"
    model_id = "tiiuae/falcon-7b-instruct"
    llm_hub = HuggingFaceHub(repo_id=model_id, model_kwargs={"temperature": 0.1, "max_new_tokens": 600})

    # Initialize embeddings
    embeddings = HuggingFaceInstructEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={"device": "cuda:0" if torch.cuda.is_available() else "cpu"}
    )

# Function to process a PDF document
def process_document(document_path):
    loader = PyPDFLoader(document_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=64)
    texts = text_splitter.split_documents(documents)

    db = Chroma.from_documents(texts, embedding=embeddings)
    return db

# Function to generate a cover letter
def generate_cover_letter(company_name, position_name, job_description, resume_file):
    # Process the PDF resume
    resume_db = process_document(resume_file.name)

    # Create the prompt for the Qwen model
    prompt = (
        f"Generate a customized cover letter using the company name: {company_name}, "
        f"the position applied for: {position_name}, and the job description: {job_description}. "
        f"Ensure the cover letter highlights my qualifications and experience as detailed in the resume content extracted from the PDF."
    )

    # Prepare the messages for the Qwen model
    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    # Generate the completion using the Qwen model
    completion = client.chat.completions.create(
        model="Qwen/Qwen2.5-Coder-32B-Instruct",
        messages=messages,
        max_tokens=gen_params["max_tokens"],
        temperature=gen_params["temperature"],
    )

    # Extract the generated cover letter
    cover_letter = completion.choices[0].message['content']
    return cover_letter

# Create a Gradio interface
cover_letter_app = gr.Interface(
    fn=generate_cover_letter,
    inputs=[
        gr.Textbox(label="Company Name", placeholder="Enter the name of the company"),
        gr.Textbox(label="Position Name", placeholder="Enter the name of the position"),
        gr.Textbox(label="Job Description", placeholder="Paste the job description here", lines=10),
        gr.File(label="Upload Resume (PDF)", type="filepath"),
    ],
    outputs=gr.Textbox(label="Customized Cover Letter"),
    title="Customized Cover Letter Generator",
    description="Generate a customized cover letter by entering the company name, position name, job description, and uploading your resume in PDF format."
)

# Launch the Gradio app
if __name__ == "__main__":
    init_llm()  # Initialize the language model
    cover_letter_app.launch()
