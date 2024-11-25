from huggingface_hub import InferenceClient
import fitz  # PyMuPDF

# Initialize the InferenceClient with your API key
client = InferenceClient(api_key="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")

# Parameters for the Qwen model
gen_params = {
    "max_tokens": 10000,
    "temperature": 0.7
}

def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF file."""
    text = ""
    with fitz.open(pdf_file) as doc:
        for page in doc:
            text += page.get_text()
    return text

def polish_resume_ai(position_name, resume_file, polish_prompt):
    # Extract text from the uploaded PDF resume
    resume_content = extract_text_from_pdf(resume_file)

    # Create the prompt for the Qwen model
    if polish_prompt and polish_prompt.strip():
        prompt_use = f"Given the resume content: '{resume_content}', polish it based on the following instructions: {polish_prompt} for the {position_name} position"
    else:
        prompt_use = f"Suggest improvements for the following resume content: '{resume_content}' to better align with the requirements and expectations of a {position_name} position. Return the polished version, highlighting necessary adjustments for clarity, relevance, and impact in relation to the targeted role."

    # Prepare the messages for the Qwen model
    messages = [
        {
            "role": "user",
            "content": prompt_use
        }
    ]

    # Generate the completion using the Qwen model
    completion = client.chat.completions.create(
        model="Qwen/Qwen2.5-Coder-32B-Instruct",
        messages=messages,
        max_tokens=gen_params["max_tokens"],
        temperature=gen_params["temperature"],
    )

    # Extract the generated polished resume
    polished_resume = completion.choices[0].message['content']
    return polished_resume
