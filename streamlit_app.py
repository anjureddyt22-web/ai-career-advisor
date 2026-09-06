import streamlit as st
import os
import json
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Load API key from .env
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

# Connect to Gemini
client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)

# -----------------------------
# Website title
# -----------------------------

st.markdown(
    """
    <div style="text-align:center; padding:20px;">
        <h1>🎯 AI Career Advisor</h1>
        <p style="font-size:20px;">
            Discover the career path that matches your
            <b>goals, interests, skills and budget.</b>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.info(
    "💡 Enter your details below and our AI will suggest "
    "3 suitable career paths."
)

# -----------------------------
# Student information
# -----------------------------

st.subheader("👤 Student Information")

name = st.text_input("Name")

education = st.selectbox(
    "Education Level",
    ["10th", "Intermediate"]
)

marks = st.number_input(
    "Marks / Percentage",
    min_value=0.0,
    max_value=100.0,
    step=0.1
)
goal=st.text_input("what is your career goal?")

subject=st.text_input("what is favorite subject?")
min_budget=st.number_input(
    "Enter your minimum budget",
    min_value=0.0,
    step=1000.0
)

max_budget = st.number_input(
    "Enter your maximum budget",
    min_value=0.0,
    step=1000.0
)

state = st.text_input(
    "Which state do you prefer to study in?"
)

district = st.text_input(
    "Which district do you prefer to study in?"
)

# -----------------------------
# Analyze button
# -----------------------------

if st.button("🚀 Analyze My Career Path"):
   
    if name and goal and subject and state and district:

        # Create AI prompt
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
3. Suitability level
4. Why it suits the student
5. Minimum and maximum estimated education cost
6. Eligibility requirements
7. Skills to learn
8. Education path
9. Future scope
10. Possible job roles
11. Approximate salary range
12. Course options
13. College/course options to explore
14. What the student should focus on most
15. Step-by-step career roadmap

Important rules:
- Do not discourage the student based only on marks.
- Consider the student's interests and career goals.
- The match score is only an AI-generated guidance indicator.
- Clearly label cost and salary as estimates.
- Do not invent exact college fees or salary figures.
- Keep the explanation simple and student-friendly.

Return the answer ONLY as valid JSON.

Use exactly this structure:

{{
  "careers": [
    {{
      "career_name": "",
      "match_score": 0,
      "suitability": "",
      "why_suitable": "",
      "cost": "",
      "eligibility": "",
      "skills": [],
      "education_path": "",
      "future_scope": "",
      "job_roles": [],
      "salary": "",
      "course_options": [],
      "college_options": [],
      "focus_areas": [],
      "roadmap": []
    }}
  ]
}}

The roadmap must contain the steps in order, from the student's current education level to the target career.

Return exactly 3 careers.
Do not add Markdown or ``` around the JSON.
"""

        # Send prompt to Gemini
        with st.spinner("🤖 Analyzing your career options..."):

            interaction = client.interactions.create(
                model="gemini-3.6-flash",
                input=prompt
            )

        # Get Gemini response
        response_text = interaction.output_text

        # Try to convert Gemini response into Python data
        try:
            career_data = json.loads(response_text)

            careers = career_data["careers"]

            st.success("Career recommendations received successfully! 🎉")
            st.write("## 🎯 Your Top 3 Career Paths")

            for number, career in enumerate(careers, start=1):

                # Career card
                st.markdown(
                    f"""
                    <div style="
                        border: 2px solid #ddd;
                        border-radius: 15px;
                        padding: 20px;
                        margin: 15px 0;
                    ">
                        <h2>🏆 {number}. {career['career_name']}</h2>
                        <h3>⭐ Match Score: {career['match_score']}/100</h3>
                        <p><b>🟢 Suitability:</b> {career['suitability']}</p>
                        <p><b>💡 Why it suits you:</b> {career['why_suitable']}</p>
                        <p><b>💰 Estimated Cost:</b> {career['cost']}</p>
                        <p><b>🎓 Education:</b> {career['education_path']}</p>
                        <p><b>📈 Future Scope:</b> {career['future_scope']}</p>
                        <p><b>💼 Salary:</b> {career['salary']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Skills
                st.write("### 📚 Skills to Learn")

                for skill in career["skills"]:
                    st.write("•", skill)

                # Job roles
                st.write("### 💼 Job Roles")

                for role in career["job_roles"]:
                    st.write("•", role)

                # Roadmap
                st.write("### 🛣️ Career Roadmap")

                roadmap = career["roadmap"]

                for i, step in enumerate(roadmap):

                    st.info(f"STEP {i + 1} → {step}")

                    if i < len(roadmap) - 1:
                        st.markdown(
                            "<div style='text-align:center; "
                            "font-size:30px;'>⬇️</div>",
                            unsafe_allow_html=True
                        )

                st.divider()

        except json.JSONDecodeError:
            st.error("Gemini did not return valid JSON. Please try again.")
