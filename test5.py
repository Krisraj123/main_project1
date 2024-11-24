from huggingface_hub import InferenceClient
import gradio as gr
import fitz  # PyMuPDF

# Initialize the InferenceClient with your API key
client = InferenceClient(api_key="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")

# Parameters for the Qwen model
gen_params = {
    "max_tokens": 1024,
    "temperature": 0.7
}

def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF file."""
    text = ""
    with fitz.open(pdf_file) as doc:
        for page in doc:
            text += page.get_text()
    return text

def generate_career_advice(position_applied, job_description, resume_file):
    # Extract text from the uploaded PDF resume
    resume_content = extract_text_from_pdf(resume_file.name)

    # Create the prompt for the Qwen model
    prompt = (
        f"Considering the job description: {job_description}, and the resume provided: {resume_content}, "
        f"identify areas for enhancement in the resume. Offer specific suggestions on how to improve these aspects "
        f"to better match the job requirements and increase the likelihood of being selected for the position of {position_applied}."
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

    # Extract the generated advice
    advice = completion.choices[0].message['content']
    return advice

# Create a Gradio interface
career_advice_app = gr.Interface(
    fn=generate_career_advice,
    allow_flagging="never",
    inputs=[
        gr.Textbox(label="Position Applied For", placeholder="Enter the position you are applying for"),
        gr.Textbox(label="Job Description Information", placeholder="Paste the job description here", lines=10),
        gr.File(label="Your Resume (PDF)", file_types=[".pdf"], type="filepath"),  # Changed to File input for PDF
    ],
    outputs=gr.Textbox(label="Advice"),
    title="Career Advisor",
    description="Enter the position you're applying for, paste the job description, and upload your resume in PDF format to get advice on what to improve for getting this job."
)

# Launch the Gradio app
if __name__ == "__main__":
    career_advice_app.launch()
