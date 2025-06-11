import gradio as gr
import os
from groq import Groq
from PyPDF2 import PdfReader
from docx import Document

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key="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")

def extract_text(file):
    ext = file.name.split('.')[-1].lower()
    text = ""
    if ext == 'pdf':
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    elif ext == 'docx':
        doc = Document(file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    return text

from sentence_transformers import SentenceTransformer, util

# Load once globally for performance
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

def get_resume_score(resume_text, job_description):
    resume_embed = embed_model.encode(resume_text, convert_to_tensor=True)
    jd_embed = embed_model.encode(job_description, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(resume_embed, jd_embed).item()
    score = round(similarity * 100)  # Scale to 0–100
    return score+40


def analyze_multiple_resumes(files, job_description):
    results = []
    for file in files:
        try:
            resume_text = extract_text(file)
            score = get_resume_score(resume_text, job_description)
            results.append((os.path.basename(file.name), int(score)))
        except Exception as e:
            results.append((os.path.basename(file.name), f"Error: {str(e)}"))

    sorted_results = sorted(
        [r for r in results if isinstance(r[1], int)],
        key=lambda x: x[1],
        reverse=True
    ) + [r for r in results if not isinstance(r[1], int)]

    return sorted_results




with gr.Blocks(title="Bulk Resume Scorer", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    <h1 style='text-align: center; color: #2E86C1;'> Resume Score Evaluator</h1>
    <p style='text-align: center; font-size: 16px; color: #117864;'>
        Upload multiple resumes and compare them against a job description using smart AI matching!
    </p>
    """)
    
    with gr.Row():
        resumes = gr.File(label=" Upload Resumes", file_types=['.pdf', '.docx'], file_count="multiple")
        job_desc = gr.Textbox(label=" Job Description", lines=8, placeholder="Paste job description here...")

    submit = gr.Button("Get Scores", elem_id="submit-btn")

    results_output = gr.Dataframe(headers=["Resume File", "Score"], datatype=["str", "str"], interactive=False)
    submit.click(fn=analyze_multiple_resumes, inputs=[resumes, job_desc], outputs=[results_output])


    # Add custom CSS via <style> tag
    gr.HTML("""
    <style>
        #submit-btn button {
            background-color: #2ECC71 !important;
            color: white !important;
            font-size: 16px !important;
            padding: 10px 20px !important;
            border-radius: 10px !important;
            border: none !important;
        }
    </style>
    """)



if __name__ == "__main__":
    demo.launch() 