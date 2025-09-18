import csv
from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()  #Load environment variables from .env file
app = FastAPI()

#Initialize Groq client

#Initialize Groq client properly
client = Groq(api_key=os.getenv("groq_api"))


#For API input
class TranscriptInput(BaseModel):
    transcript: str

#Utility to save output to CSV
def save_to_csv(transcript, summary, sentiment, filename="call_analysis.csv"):
    header = ["Transcript", "Summary", "Sentiment"]
    row = [transcript, summary, sentiment]

    try:
        with open(filename, "x", newline="", encoding="utf-8") as f:  # create file if not exists
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerow(row)
    except FileExistsError:
        with open(filename, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(row)

# Function to analyze transcript using Groq API
def analyze_transcript(transcript:str):
    prompt = f"""
Summarize the customer conversation in 2–3 sentences and state the sentiment.
Conversation: {transcript}

Respond EXACTLY in this format:

Summary: <your summary here>
Sentiment: <Positive/Neutral/Negative>
"""



    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # change if needed
        messages=[{"role": "user", "content": prompt}],
    )

    reply = response.choices[0].message.content
  

    #Handle JSON output parsing safely
    import json
    summary = "N/A"
    sentiment = "N/A"

    for line in reply.splitlines():
        if line.lower().startswith("summary:"):
            summary = line.split(":", 1)[1].strip()
        elif line.lower().startswith("sentiment:"):
            sentiment = line.split(":", 1)[1].strip()

    return summary, sentiment


#API endpoint
@app.post("/analyze/")
def analyze(transcript_input: TranscriptInput):
    transcript = transcript_input.transcript
    summary, sentiment = analyze_transcript(transcript)

    #Print results
    print(f"Transcript: {transcript}")
    print(f"Summary: {summary}")
    print(f"Sentiment: {sentiment}")

    #Save to CSV
    save_to_csv(transcript, summary, sentiment)

    return {
        "Transcript": transcript,
        "Summary": summary,
        "Sentiment": sentiment
    }
