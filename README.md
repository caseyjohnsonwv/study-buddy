# study-buddy
An AI-powered study assistant for university students.

Casey Johnson, University of Central Florida

---

## Disclaimer

Study Buddy is not a replacement for students' own thoughts & learnings. While this tool uses large language models from OpenAI to index and search provided course materials, it is purely that - a tool. It serves as a virtual study assistant. Double-check each course's Academic Dishonesty policy and any applicable AI policies before using this tool to study. **DO NOT** use this tool to generate final deliverable course assigments.

## Quickstart

1. Create a `.env` file in the project root containing:
```
OPENAI_API_KEY=
```
2. Run `poetry install` to install project dependencies.
3. Drop course materials in named subdirectories under a new `courses/`directory . For example, `courses/ENGLISH101/Chapter 1/[new file]`
4. Run `python app.py` from the project root.
5. Open the Gradio UI and start asking questions.

## Sample Usage

**Query:**

list forms of non-monetary compensation

**Response:**

Forms of non-monetary compensation include:
1. Recognition and praise: Providing employees with verbal or written recognition for their achievements and contributions.
2. Flexible work arrangements: Allowing employees to have flexible work hours, remote work options, or compressed workweeks.
3. Professional development opportunities: Offering training programs, workshops, conferences, or tuition reimbursement to support employees' career growth.
4. Work-life balance initiatives: Providing benefits such as paid time off, parental leave, or sabbaticals to help employees maintain a healthy work-life balance.
5. Employee wellness programs: Offering wellness initiatives such as gym memberships, wellness challenges, or access to mental health resources.
6. Employee assistance programs: Providing counseling services, financial planning assistance, or legal advice to support employees' well-being.
7. Employee discounts: Offering discounts on company products or services, or partnering with external vendors to provide discounts to employees.
8. Commuter benefits: Providing subsidies or reimbursements for commuting expenses, such as public transportation passes or parking fees.
9. Employee engagement activities: Organizing team-building events, social gatherings, or employee appreciation events to foster a positive work environment.
10. Career advancement opportunities: Offering opportunities for promotion, job rotation, or cross-training to help employees advance in their careers.

(Source: "Compensation & Benefits - March 23.pptx", slide 26)

## Limitations

This tool can index `.html`, `.pdf`, and `.pptx` files. Other filetypes are currently not supported.
