name=input("Enter your name:")
education=input("enter your education level(10th/Intermediate):")
marks=float(input("enter your marks/percentage:"))
goal=input("what is your carrer goal:")
subject=input("enter your favorite subject:")
min_budget=float(input("enter your minimum budget:"))
max_budget=float(input("enter yuor maximum budget:"))
state=input("which state do you prefer to study in:")
district=input("which district do you prefer to study in:")
student={
    "name":name,
    "education":education,
    "marks":marks,
    "goal":goal,
    "favorite_subject":subject,
    "min_budget":min_budget,
    "max_budget":max_budget,
    "state":state,
    "district":district
}
print("\nStudent profile:")
print(student)
prompt = f"""
You are an AI career guidance assistant.

Analyze the following student information:

Name: {name}
Education: {education}
Marks: {marks}
Career Goal: {goal}
Favorite Subject: {subject}
Budget: ₹{min_budget} - ₹{max_budget}
Preferred State: {state}
Preferred District: {district}

Suggest exactly 3 suitable career paths for this student.

For EACH career, provide:

1. Career name
2. AI Match Score out of 100
3. Suitability level: Highly Suitable, Suitable, or Possible
4. Why this career suits the student
5. Minimum and maximum estimated education cost
6. Eligibility requirements
7. Skills the student needs to learn
8. Education path
9. Future scope
10. Possible job roles
11. Approximate salary range
12. Suitable course options
13. College/course options to explore
14. What the student should focus on most to succeed
15. Step-by-step career roadmap

Important rules:
- Do not discourage the student based only on marks.
- Give importance to the student's interests and career goal.
- The match score is only an AI-generated guidance indicator, not a guarantee.
- Clearly label cost and salary as estimates.
- Do not invent exact college fees, admission requirements, or salary figures.
- If specific current information is unavailable, say that the student should verify it from official sources.
- Keep the explanation simple and understandable for a student.
"""


print("\nAI Prompt:")
print(prompt)
{
  "career_name": "Software Developer",
  "why_suitable": "Matches the student's interest in technology.",
  "education_path": "Intermediate → B.Tech/degree → Projects → Internship",
  "eligibility": "Depends on the selected course and institution.",
  "cost": {
    "minimum": "₹50,000",
    "maximum": "₹4,00,000"
  },
  "skills": [
    "Programming",
    "Data Structures",
    "SQL",
    "Git"
  ],
  "future_scope": "Opportunities in software development and related technology roles.",
  "job_roles": [
    "Software Developer",
    "Backend Developer",
    "Full Stack Developer"
  ],
  "salary": "Approximate range based on role, location and experience.",
  "course_options": [
    "B.Tech CSE",
    "BCA",
    "B.Sc Computer Science"
  ],
  "focus_areas": [
    "Programming fundamentals",
    "Problem solving",
    "Projects",
    "Communication"
  ],
  "roadmap": [
    "Learn programming basics",
    "Learn DSA and SQL",
    "Build projects",
    "Get internship experience"
  ]
}
import os
from google import genai

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

interaction = client.interactions.create(
    model="gemini-3.6-flash",
    input=prompt
)
print("\nGemini Response:")
print(interaction.output_text)
