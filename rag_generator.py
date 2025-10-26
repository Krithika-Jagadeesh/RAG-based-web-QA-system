import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-pro-latest")

def generate_answer_with_citations(query, context_chunks):
    context = "\n\n".join([f"[{i+1}] {chunk}" for i, chunk in enumerate(context_chunks)])
    prompt = f"""Answer the question using the context below. Cite sources like [1], [2], etc.

Context:
{context}

Question: {query}
Answer:"""
    response = model.generate_content(prompt)
    return response.text