import os
from huggingface_hub import snapshot_download
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import gradio as gr

# ── Download ChromaDB from your private dataset ──
print("Downloading ChromaDB from Hugging Face dataset...")
chroma_path = snapshot_download(
    repo_id="Shoaibkhalid65/iub-chromadb",
    repo_type="dataset",
    token=os.environ.get("HF_TOKEN")
)
print(f"ChromaDB downloaded to: {chroma_path}")

# ── Load embedding model ──
print("Loading embedding model...")
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    model_kwargs={"device": "cpu"}
)

# ── Load ChromaDB ──
vectorstore = Chroma(
    persist_directory=chroma_path,
    embedding_function=embeddings
)
print(f"ChromaDB loaded: {vectorstore._collection.count()} chunks")

# ── API key rotation across 30 Gemini keys ──
API_KEYS = [os.environ.get(f"GEMINI_KEY_{i}") for i in range(1, 31)]
API_KEYS = [k for k in API_KEYS if k]
print(f"Loaded {len(API_KEYS)} API keys")

current_key_index = 0

def get_working_llm():
    global current_key_index
    while current_key_index < len(API_KEYS):
        key = API_KEYS[current_key_index]
        try:
            os.environ["GOOGLE_API_KEY"] = key
            test_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
            test_llm.invoke("hi")
            print(f"Using API key #{current_key_index + 1}")
            return test_llm
        except Exception as e:
            print(f"Key #{current_key_index + 1} failed: {str(e)[:80]}")
            current_key_index += 1
    return None

llm = get_working_llm()

# ── Facebook-priority retriever ──
def get_priority_docs(query, k=15):
    try:
        fb_results = vectorstore.similarity_search(query, k=5, filter={"source": "facebook"})
    except:
        fb_results = []
    all_results = vectorstore.similarity_search(query, k=k)
    useful_fb = [doc for doc in fb_results if len(doc.page_content.strip()) > 100]
    if len(useful_fb) >= 2:
        seen = {doc.page_content for doc in useful_fb}
        supplementary = [doc for doc in all_results if doc.page_content not in seen]
        return useful_fb + supplementary[:k - len(useful_fb)]
    return all_results

def format_docs(docs):
    return "\n\n".join(
        f"[Source: {doc.metadata.get('source', 'website')} | Year: {doc.metadata.get('year', 'unknown')}]\n{doc.page_content}"
        for doc in docs
    )

def format_history(history, max_exchanges=5):
    if not history:
        return "This is the start of the conversation."
    recent = history[-(max_exchanges * 2):]
    lines = []
    for msg in recent:
        role = "Student" if msg["role"] == "user" else "IUB Assist"
        lines.append(f"{role}: {msg['content']}")
    return "Previous exchanges:\n" + "\n".join(lines)

prompt_template = PromptTemplate.from_template("""You are IUB Assist, the official AI support agent for Islamia University Bahawalpur (IUB), Pakistan.
CONVERSATION HISTORY:
{chat_history}
MEMORY RULE: Connect follow-up questions to the previous topic automatically.
SOURCE PRIORITY: [Source: facebook] is most recent — prefer it for announcements. Use website/PDF sources for fees and structured info.
RULES:
- Answer ONLY from context below
- Say "I don't have that information" only if context has nothing relevant
- Be polite and professional
- Respond in the same language as the question (English or Urdu)
- Never make up information
CONTEXT:
{context}
QUESTION: {question}
ANSWER:""")

def answer_with_memory(user_message, history):
    docs = get_priority_docs(user_message)
    context = format_docs(docs)
    chat_history = format_history(history)
    prompt = prompt_template.format(chat_history=chat_history, context=context, question=user_message)
    return llm.invoke(prompt).content

def chat_with_rotation(user_message, history):
    global current_key_index, llm
    try:
        return answer_with_memory(user_message, history)
    except Exception as e:
        error = str(e)
        if any(x in error for x in ["429", "403", "401", "invalid"]):
            current_key_index += 1
            llm = get_working_llm()
            if llm is None:
                return "All API keys exhausted. Please try again later."
            try:
                return answer_with_memory(user_message, history)
            except Exception as e2:
                return f"Error: {str(e2)[:200]}"
        return f"Error: {error[:200]}"

# ── Gradio UI ──
with gr.Blocks(title="IUB Assist") as demo:
    gr.HTML("""
    <div style="background:#0a1f5c; padding:20px; border-radius:10px; text-align:center;">
        <h1 style="color:white; margin:0;">🎓 IUB Assist — AI Customer Support Agent</h1>
        <p style="color:#C9A84C; margin:5px 0 0 0;">Islamia University of Bahawalpur</p>
    </div>
    """)
    gr.ChatInterface(
        fn=chat_with_rotation,
        chatbot=gr.Chatbot(height=400),
        examples=[
            "What are the admission requirements for BS programs?",
            "What scholarships are available at IUB?",
            "What is the fee structure for PhD programs?",
            "IUB mein kaunse programs available hain?",
        ],
    )

demo.launch()
