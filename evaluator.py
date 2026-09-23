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
        You are a highly critical technical recruiter. Evaluate the candidate's resume against the provided job description.

        SCORING RUBRIC (0-100):
        - Start at 0.
        - Add points ONLY for exact technical skill matches.
        - Deduct points heavily if years of experience do not match or if the candidate lacks core required frameworks.
        - Be harsh. A standard match should score around 50-60. Only true perfect matches should score above 75.

        OUTPUT RULES:
        1. 'score': Integer between 0 and 100 based on the strict rubric.
        2. 'apply': Boolean True if score is 75 or higher, else False.
        3. 'pitch': If apply is True, write a highly technical, 2-sentence cover note in the FIRST PERSON perspective (using "I", "my"). 
           - NEVER use the name "Vani" or refer to the candidate in the third person. 
           - Example: "I want to apply for this role because my experience building LangGraph state machines directly aligns with your need for AI agents."
        
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
    AI/ML Intern - Indian Navy (WESEE), New Delhi (July 2025 - September 2025
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
    
    results = evaluate_jobs(test_jobs, my_resume)
    print(f"Jobs approved for application: {len(results)}")