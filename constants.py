UPLOAD_FOLDER = r"media"
ALLOWED_EXTENSIONS = {"pdf"}

SYSTEM_PROMPT = """
Act as an expert in resume analysis and recruitment support for the job role {job_role} and give following support for given resume.
Today's date is: {date_today}

Guidlines:
- analyse full resume at once.
- formatting is not important for this resume.
- calculation of experience and resume score is the most important.
- extract desired information.
- make proper markdown on full information.
- give accurate response with markdown.

Job Discription:
{job_description}
"""
TECHNICAL_HUMAN_PROMPT = """
Please summurize this resume and give following points:
1. First section:-
- Give a summary of the resume in short so we can get proper idea about profile


2. Second section:-
- Please provide any mistakes that you have found in this resume.
- don't give date related mistakes.
- Ignore resume formatting mistakes.

Overall resume score by comparing resume with the Job discription(out of 100%):
- Also give reason why you give this score

Coclusion:
- your analysis can we go futher with this profile or not? and why?


RESUME:
'{resume}'
"""
# TECHNICAL_HUMAN_PROMPT = """
# Please summurize this resume and give following points:
# 1. First section (give point vise answers):-
# - Detailed summary of the full resume:
# - Course: e.g btech/bca/bsc
# - Passout year:
# - Marks:
# - Total year of Experience:

# 2. Second section:-
# details of all project with their involved technologies.(don't give numbers for project)
# - project (involved technologies): project discription

# 3. Third section:-
# - Please provide any mistakes that you have found in this resume.
# - don't give date related mistakes.
# - Ignore resume formatting mistakes.

# 4. Fourth section:-
# Please come up with five non codding questions from the resume.(don't give numbers for questions)

# 5. Fifth Section:(Important)
# Please generate two distinct technical (logical) questions with varying difficulty levels. These questions should be thoroughly explained and accompanied by their respective answers. Ensure that the questions are specifically tailored to coding challenges and refrain from providing common questions readily available on the Internet.

# - Difficulty Level of Questions: {level} (questions sholud be based on difficulty level)
# - Time to Solve the Question: 15 minutes.
# - One qustion codding based and one question scenario based.

# Note: Provide only coding questions, along with their answers and explanations.

# follow this notes for fifth section
# Notes:
# - quetions and answers both are explained in detail.
# - Please give all the technical (logical) questions with proper answers.
# - Don't use common and famous technical (logical) questions.

# 6. Sixth section:
# - What are the skills required for the job role that the candidate lacks based on their experience and job discription?


# Overall resume score based on the Job Discription(out of 100%):
# - Also give reason why you give this score
# - Give score accuratly not randomally.

# RESUME:
# {resume}
# """

HR_HUMAN_PROMPT = """
Please summurize this resume and accurate answers of the following points for difficulty level {level}:
1. First section:-
- Detailed summary of the full resume:
- Course: e.g btech/bca/bsc
- Passout year: 
- Marks: 
- Total year of Experience:
- Soft skills: 

2. Second section:-
details of all project with their involved technologies.(don't give numbers for project)
- project (involved technologies): project discription

3. Third section:- 
- Please provide any mistakes that you have found in this resume.
- Ignore resume formatting mistakes.

4. Fourth section:-
Please come up with five non codding questions from the resume for HR round support.(don't give numbers for questions)

5. Fifth section:
- What are the skills required for the job role that the candidate lacks based on their experience?

Overall resume score based on the Job Discription(out of 100%):
- Also give reason why you give this score
- Give score accuratly not randomally.

RESUME:
{resume}
"""

PROMPT_SWITCHER = {
    "Technical interview round": TECHNICAL_HUMAN_PROMPT,
    "HR interview round": HR_HUMAN_PROMPT,
}

LEVELS_SWITCHER = {
    "1": "Low",
    "2": "Medium",
    "3": "High",
}

OPEN_AI = "OPEN_AI_KEY"
OPEN_AI_ORGANIZATION = "OPEN_AI_ORGANIZATION"
COMPLETIONS_TOKEN = 2000
CHATGPT_TOP_P = 1.0
CHATGPT_FREQ_PENALTY = 0.0
CHATGPT_PRE_PENALTY = 0.0


# =============================== Error response =====================================

NO_FILE_ERROR = {
    "error": True,
    "error_message": "Please Upload your resume",
}

AI_FAILED_ERROR = {
    "error": True,
    "error_message": "Sorry😟, AI failed please try after some time!",
}

WRONG_PDF_ERROR = {
    "error": True,
    "error_message": "Please upload valid PDF!",
}

DEFAULT_INDEX_ERROR = {
    "error": False,
    "error_message": "",
}
