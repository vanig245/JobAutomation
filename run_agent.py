from scraper import scrape_jobs
from evaluator import evaluate_jobs

def run_agent():
    print("Step 1: Launching Playwright to scrape Wellfound")
    live_jobs = scrape_jobs()
    
    if not live_jobs:
        print("No jobs were extracted. Check your CSS selectors in scraper.py.")
        return

    print(f"\nStep 2: Sending {len(live_jobs)} jobs to local Llama 3.1")

    my_resume = """
    PROFILE
    Name: VANI GUPTA
    Contact: vani.gupta2405@gmail.com | +91 8368477160
    Links: 
    - LinkedIn: https://www.linkedin.com/in/vani-gupta-840736293/
    - LeetCode: https://leetcode.com/u/MSc7ZS1566/
    - GitHub: https://github.com/vanig245

    EDUCATION
    Guru Gobind Singh Indraprastha University (GGSIPU), New Delhi (2023-2027)
    Bachelor of Technology in Artificial Intelligence and Machine Learning
    Current CGPA: 9.0/10

    TECHNICAL EXPERIENCE
    AI/ML Intern - Indian Navy (WESEE), New Delhi (July 2025 - September 2025)
    - Built a gender prediction system using Random Forest Classifier achieving 95-97% accuracy and deployed a real-time Flask web interface for live audio processing.
    - Optimised MFCC feature extraction and preprocessing pipelines to ensure robust model performance and production-ready implementation.
    - Engineered a complete ML pipeline from data preprocessing, model training, and evaluation to real-time Flask web inference.

    PROJECTS
    ASTRA - Agentic Support & Triage Routing Architecture (LangGraph, LangChain, Groq, MySQL, ChromaDB)
    - Built a multi-agent customer support system on LangGraph, using a state-machine architecture to route queries to isolated, task-specific worker agents and prevent tool confusion and hallucination.
    - Designed a Classifier Agent using Llama 3 (via Groq) to detect intent and route requests to a RAG-based Technical Agent (ChromaDB + HuggingFace embeddings) or a Billing Agent with direct, real-time MySQL access.
    - Maintained stateful conversation memory across the session while keeping each agent's data access narrowly scoped for security and deterministic behavior.

    AI Data Analyst (FastAPI, LangChain, DuckDB, Groq, Docker)
    - Built an autonomous data analytics agent that converts natural language queries into optimized SQL, executed live against an in-memory DuckDB database.
    - Engineered LangChain agent tools for automated chart generation and Z-score-based statistical anomaly detection, invoked dynamically via function calling.
    - Containerized the full application with Docker for single-command deployment, powered by low-latency inference from Groq-hosted LLMs.

    CourseRAG - Dynamic RAG Assistant for PDFs (FastAPI, LangChain, ChromaDB, Groq, Hugging Face)
    - Built a Retrieval-Augmented Generation (RAG) system with LangChain and an in-memory ChromaDB vector store to deliver hallucination-free, document-grounded Q&A over any uploaded PDF.
    - Implemented local embedding generation using HuggingFace's all-MiniLM-L6-v2, eliminating external embedding API calls and reducing retrieval latency.
    - Integrated Meta's Llama 3.1 8B via Groq's LPU inference engine into a FastAPI backend, powering a real-time chat interface with sub-second, grounded responses.

    TECHNICAL SKILLS
    - Programming Languages: Python, SQL, Java
    - AI/Data Science: Agentic Workflows, Deep Learning, Generative AI & LLMs, Prompt Engineering, RAG, Supervised & Unsupervised Learning, NLP (spaCy), Computer Vision
    - Frameworks & High-Impact Libraries: TensorFlow, Hugging Face, LangChain, LangGraph, ChromaDB, FastAPI, Flask
    - Tools & Platforms: Docker, Git, GitHub, MySQL

    ACHIEVEMENTS & LEADERSHIP
    - GGSIPU Academic Excellence: Rank 1 in ADGIPS, Rank 2 across GGSIPU in 4th Semester SGPA: 9.8/10
    - Hack n Chill Hackathon Finalist GDSC Club
    - Head of Publicity, Kritrim Dhi (2024 - Present)
    - Tech Member, GeeksforGeeks ADGIPS (2024 - Present)
    """
    approved_jobs = evaluate_jobs(live_jobs, my_resume)
    print(f"Total jobs approved for auto-apply: {len(approved_jobs)}")
    for job in approved_jobs:
        print(f" {job['company']} - {job['title']} (Score: {job['score']})")

if __name__ == "__main__":
    run_agent()