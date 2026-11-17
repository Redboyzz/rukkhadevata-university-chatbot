# Rukkhadevata University Enquiry Chatbot

A beginner-friendly chatbot demonstration for the fictional Rukkhadevata University. All college information is sample content and does not describe a real institution.

## Requirements

- Python 3.10 or newer
- Packages listed in `requirements.txt`

## Start the app on macOS

Open Terminal and run:

```bash
cd ~/Documents/sihe-college-chatbot
source .venv/bin/activate
streamlit run app.py
```

Ask a question in the chat box. The app compares it with sample FAQ questions using TF-IDF and cosine similarity. If no FAQ is close enough, it asks you to rephrase or choose a supported topic.

To stop the app, return to Terminal and press **Control-C**.

## Project layout

- `app.py` — Streamlit chat screen
- `src/chatbot.py` — FAQ matching functions
- `data/faq.json` — fictional demonstration questions and answers
- `requirements.txt` — Python packages used by the project
