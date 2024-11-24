from huggingface_hub import InferenceClient
import gradio as gr
import fitz  # PyMuPDF

# Initialize the InferenceClient with your API key
client = InferenceClient(api_key="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")

# Parameters for the Qwen model
gen_params = {
    "max_tokens": 512,
    "temperature": 0.7
}

def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF file."""
    text = ""
    with fitz.open(pdf_file) as doc:
        for page in doc:
            text += page.get_text()
    return text

def generate_cover_letter(company_name, position_name, job_description, resume_file):
    # Extract text from the uploaded PDF resume
    resume_content = extract_text_from_pdf(resume_file.name)

    # Create the prompt for the Qwen model
    prompt = (
        f"Generate a customized cover letter using the company name: {company_name}, "
        f"the position applied for: {position_name}, and the job description: {job_description}. "
        f"Ensure the cover letter highlights my qualifications and experience as detailed in the resume content: {resume_content}. "
        f"Adapt the content carefully to avoid including experiences not present in my resume but mentioned in the job description. "
        f"The goal is to emphasize the alignment between my existing skills and the requirements of the role."
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
        gr.File(label="Resume (PDF)", file_types=[".pdf"], type="filepath"),  # Changed to File input for PDF
    ],
    outputs=gr.Textbox(label="Customized Cover Letter"),
    title="Customized Cover Letter Generator",
    description="Generate a customized cover letter by entering the company name, position name, job description, and uploading your resume in PDF format."
)

# Launch the Gradio app
if __name__ == "__main__":
    cover_letter_app.launch()
