import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

CHATBOT_TITLE = "ATS Resume & Career Fit Analyzer"
DOMAIN_DESCRIPTION_HINT = "resume analysis, job matching, and career improvement suggestions"


def get_ats_analysis(resume_text, jd_text, context_chunks):
    prompt = f"""
    You are an ATS (Applicant Tracking System) expert.

    Resume:
    {resume_text}

    Job Description:
    {jd_text}

    Additional Context:
    {context_chunks}

    Analyze and return in this exact format:
    MATCH_SCORE: <percentage number only>
    MISSING_KEYWORDS: <comma separated list>
    SUGGESTIONS: <3-4 bullet point improvements>
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content