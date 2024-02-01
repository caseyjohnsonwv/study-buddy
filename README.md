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
OPENAI_ORG_ID=
```
2. Create a virtual envirionment and run `pip install -r requirements.txt`.
3. Drop course materials in named subdirectories under a new `courses/`directory . For example, `courses/ENGLISH101/Chapter 1`
4. Run `python app.py` from the project root.
5. Open the Gradio UI and start asking questions.
