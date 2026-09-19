from pydantic import BaseModel
from ollama import chat

class JobEvaluation(BaseModel):
    score: int
    apply: bool
    pitch: str

def evaluate_jobs(scraped_jobs, resume_text):
    print(f"Starting evaluation of {len(scraped_jobs)} jobs using local Llama 3.1\n")
    approved_jobs = []

    for job in scraped_jobs:
        print(f"Evaluating: {job['title']} at {job['company']}")
        
        prompt = f"""
        You are an expert technical recruiter. Evaluate the Job Description against the Resume.
        
        Rules:
        1. 'score': Rate the match from 0 to 100.
        2. 'apply': True if score > 75, False otherwise.
        3. 'pitch': If apply is True, write a concise 2-sentence technical pitch (max 300 chars) explaining why the candidate is a perfect fit. If False, return an empty string.
        
        Resume: {resume_text}
        
        Job Description: {job['description']}
        """
        
        try:
            response = chat(
                model='llama3.1',
                messages=[{'role': 'user', 'content': prompt}],
                format=JobEvaluation.model_json_schema(),
                options={'temperature': 0}
            )

            evaluation = JobEvaluation.model_validate_json(response.message.content)
            
            print(f"Score: {evaluation.score} | Apply: {evaluation.apply}")
            if evaluation.apply:
                print(f"Pitch: {evaluation.pitch}")
                job.update(evaluation.model_dump())
                approved_jobs.append(job)
                
            print("-" * 40)
                
        except Exception as e:
            print(f"Evaluation failed for {job['title']}: {e}")
            
    return approved_jobs

if __name__ == "__main__":
    test_jobs = [{
        "title": "AI/ML Engineer",
        "company": "TechCorp",
        "description": "Looking for an engineer to build conversational agents. Must know Python, LangChain, and Docker.",
        "url": "https://wellfound.com/jobs/123"
    }]
    
    my_resume = """
    PROFILE
    Name: VANI GUPTA[cite: 4]
    Contact: vani.gupta2405@gmail.com | +91 8368477160[cite: 4]
    Links: 
    - LinkedIn: https://www.linkedin.com/in/vani-gupta-840736293/
    - LeetCode: https://leetcode.com/u/MSc7ZS1566/
    - GitHub: https://github.com/vanig245

    EDUCATION
    Guru Gobind Singh Indraprastha University (GGSIPU), New Delhi (2023-2027)[cite: 4]
    Bachelor of Technology in Artificial Intelligence and Machine Learning[cite: 4]
    Current CGPA: 9.0/10[cite: 4]

    TECHNICAL EXPERIENCE
    AI/ML Intern - Indian Navy (WESEE), New Delhi (July 2025 - September 2025)[cite: 4]
    - Built a gender prediction system using Random Forest Classifier achieving 95-97% accuracy and deployed a real-time Flask web interface for live audio processing.[cite: 4]
    - Optimised MFCC feature extraction and preprocessing pipelines to ensure robust model performance and production-ready implementation.[cite: 4]
    - Engineered a complete ML pipeline from data preprocessing, model training, and evaluation to real-time Flask web inference.[cite: 4]

    PROJECTS
    ASTRA - Agentic Support & Triage Routing Architecture (LangGraph, LangChain, Groq, MySQL, ChromaDB)[cite: 4]
    - Built a multi-agent customer support system on LangGraph, using a state-machine architecture to route queries to isolated, task-specific worker agents and prevent tool confusion and hallucination.[cite: 4]
    - Designed a Classifier Agent using Llama 3 (via Groq) to detect intent and route requests to a RAG-based Technical Agent (ChromaDB + HuggingFace embeddings) or a Billing Agent with direct, real-time MySQL access.[cite: 4]
    - Maintained stateful conversation memory across the session while keeping each agent's data access narrowly scoped for security and deterministic behavior.[cite: 4]

    AI Data Analyst (FastAPI, LangChain, DuckDB, Groq, Docker)[cite: 4]
    - Built an autonomous data analytics agent that converts natural language queries into optimized SQL, executed live against an in-memory DuckDB database.[cite: 4]
    - Engineered LangChain agent tools for automated chart generation and Z-score-based statistical anomaly detection, invoked dynamically via function calling.[cite: 4]
    - Containerized the full application with Docker for single-command deployment, powered by low-latency inference from Groq-hosted LLMs.[cite: 4]

    CourseRAG - Dynamic RAG Assistant for PDFs (FastAPI, LangChain, ChromaDB, Groq, Hugging Face)[cite: 4]
    - Built a Retrieval-Augmented Generation (RAG) system with LangChain and an in-memory ChromaDB vector store to deliver hallucination-free, document-grounded Q&A over any uploaded PDF.[cite: 4]
    - Implemented local embedding generation using HuggingFace's all-MiniLM-L6-v2, eliminating external embedding API calls and reducing retrieval latency.[cite: 4]
    - Integrated Meta's Llama 3.1 8B via Groq's LPU inference engine into a FastAPI backend, powering a real-time chat interface with sub-second, grounded responses.[cite: 4]

    TECHNICAL SKILLS
    - Programming Languages: Python, SQL, Java[cite: 4]
    - AI/Data Science: Agentic Workflows, Deep Learning, Generative AI & LLMs, Prompt Engineering, RAG, Supervised & Unsupervised Learning, NLP (spaCy), Computer Vision[cite: 4]
    - Frameworks & High-Impact Libraries: TensorFlow, Hugging Face, LangChain, LangGraph, ChromaDB, FastAPI, Flask[cite: 4]
    - Tools & Platforms: Docker, Git, GitHub, MySQL[cite: 4]

    ACHIEVEMENTS & LEADERSHIP
    - GGSIPU Academic Excellence: Rank 1 in ADGIPS, Rank 2 across GGSIPU in 4th Semester SGPA: 9.8/10[cite: 4]
    - Hack n Chill Hackathon Finalist GDSC Club[cite: 4]
    - Head of Publicity, Kritrim Dhi (2024 - Present)[cite: 4]
    - Tech Member, GeeksforGeeks ADGIPS (2024 - Present)[cite: 4]
    """
    
    results = evaluate_jobs(test_jobs, my_resume)
    print(f"Jobs approved for application: {len(results)}")