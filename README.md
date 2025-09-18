# Mini Tech Challenge – Call Transcript Analyzer

This project is a small **FastAPI** app that uses the **Groq API** to analyze customer call transcripts.  
It can summarize conversations and detect customer sentiment, then save the results to a CSV file.  

---

## Features
- Accepts a customer transcript via API.
- Uses **Groq LLM** to:
  - Summarize the transcript in 2–3 sentences.
  - Extract the customer’s sentiment (Positive / Neutral / Negative).
- Prints the transcript, summary, and sentiment.
- Saves all results into `call_analysis.csv` with 3 columns:
