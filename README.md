# 🎓 IUB Assist — AI Customer Support Agent

An AI-powered customer support chatbot built specifically for
**Islamia University of Bahawalpur (IUB)**, Pakistan.
Answers student and faculty queries about admissions, fees,
scholarships, departments, and facilities — in English and Urdu.

---

## 🔗 Live Demo

👉 [Try IUB Assist on Hugging Face](https://huggingface.co/spaces/Shoaibkhalid65/iub-assist)

---

## 📌 Problem Statement

IUB serves thousands of students across multiple campuses.
Students have no instant way to get answers about admissions,
fee structures, scholarship eligibility, or exam schedules.
The only options are calling a helpline or visiting campus in person.
IUB Assist solves this with a 24/7 AI support agent.

---

## 🏗️ Architecture

User Question (English or Urdu)
↓
Gradio Web UI
↓
LangChain Agent + Conversational Memory (last 5 exchanges)
↓
sentence-transformers → ChromaDB (121,971 chunks)
Facebook-priority retrieval
↓
Google Gemini 2.5 Flash
↓
Answer displayed to user

---

## 📊 Dataset

| Source | Files | Size |
|---|---|---|
| IUB website scraped | 5,272 pages | 29.1 MB |
| Official PDF documents | 1,339 files | 29.0 MB |
| Facebook posts (2025–2026) | 3,324 posts | ~5 MB |
| Synthetic Q&A pairs | 3,160 pairs | ~1 MB |
| **Total** | **6,888+ files** | **~59 MB** |

📂 [Full dataset + notebooks on Google Drive](https://drive.google.com/drive/folders/1TCwv4Ri9CarXC8SAA8WcfLUSaN5awDqi)

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| LLM | Google Gemini 2.5 Flash |
| RAG Framework | LangChain |
| Vector Database | ChromaDB |
| Embeddings | sentence-transformers (multilingual-MiniLM-L12-v2) |
| Web UI | Gradio |
| Web Scraping | crawl4ai |
| PDF Processing | PyMuPDF + Gemini Vision OCR + Tesseract |
| Social Media Data | Apify Facebook Posts Scraper |
| Deployment | Hugging Face Spaces (CPU Basic) |
| Development | Google Colab + Google Drive |

---

## 📁 Repository Structure

IUB-Assist/
├── app.py                   # Hugging Face deployment file
├── requirements.txt         # Python dependencies
├── Conver_Impl.ipynb        # Main RAG pipeline + chatbot
├── DataCollection1.ipynb    # Data collection pipeline
└── README.md                # This file

---

## ✨ Key Features

- **RAG-based answering** — answers grounded strictly in real IUB data
- **Facebook-priority retrieval** — most recent posts retrieved first
- **Conversational memory** — remembers last 5 exchanges per session
- **Multilingual** — responds in English or Urdu based on user input
- **30-key API rotation** — uninterrupted availability on free tier
- **Honest fallback** — says "I don't have that information" when data is unavailable

---

## 🚀 How to Run Locally

```bash
# Clone this repository
git clone https://github.com/Shoaibkhalid65/IUB-Assist.git
cd IUB-Assist

# Install dependencies
pip install -r requirements.txt

# Download ChromaDB from Hugging Face dataset
# (see Conver_Impl.ipynb for full setup instructions)

# Run the app
python app.py
```

---

## 👤 Author

**Muhammad Shoaib Khalid**
BS Software Engineering — Islamia University of Bahawalpur
[LinkedIn](https://www.linkedin.com/in/muhammad-shoaib-khalid-864502297) | [Hugging Face](https://huggingface.co/Shoaibkhalid65)
