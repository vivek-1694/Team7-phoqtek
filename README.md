RESUME SCORER

This tool helps you compare multiple resumes against a given job description using AI.

Features
- Upload multiple resumes (.pdf or .docx).
- Paste your job description.
- Get a smart score (0–100) for each resume based on relevance.

How It Works
- Extracts text from each resume.
- Uses a pre-trained model (MiniLM) to compute similarity(co-sine similarity) with the job description.
- Displays results in a ranked table

Technologies Used
- Python
- Gradio for UI
- Sentence Transformers (all-MiniLM-L6-v2)
- PyPDF2 and python-docx for file parsing
