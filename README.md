<div align="center">

# 📚 ResearchMate

### Multi-Paper Research Assistant powered by RAG

Ask questions across multiple research papers, compare them side-by-side, and discover research gaps — all in one place.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square&logo=langchain&logoColor=white)](https://www.langchain.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Store-7C3AED?style=flat-square)](https://www.trychroma.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [Architecture](#-architecture) • [Roadmap](#-roadmap)

</div>

---

## 📖 Overview

**ResearchMate** is a Retrieval-Augmented Generation (RAG) application that lets researchers, students, and academics interact with a collection of research papers conversationally. Instead of reading paper after paper to find relevant information, you can upload multiple PDFs and:

- 💬 Ask natural-language questions across **all** papers at once
- 📊 Generate structured **comparison tables** between papers
- 🔍 Identify **research gaps** in your paper collection
- 📄 Trace every answer back to its **source chunks and papers**

Built as a semester/capstone project, ResearchMate demonstrates a complete RAG pipeline — from PDF ingestion and chunking, to embedding and vector search, to LLM-based synthesis — wrapped in a clean, tabbed Streamlit interface.

---

## ✨ Features

| Feature | Description |
|---|---|
| 💬 **Cross-Paper Q&A** | Ask a question once and get answers synthesized across your entire paper collection, with sources cited |
| 📊 **Paper Comparison** | Automatically generate a comparison table across uploaded papers (methods, datasets, results, etc.) |
| 🔍 **Research Gap Finder** | Analyzes your knowledge base to surface potential gaps or under-explored areas across papers |
| 📄 **Chunk-Level Traceability** | Every answer links back to the exact document chunks used to generate it |
| 🗂️ **Persistent Knowledge Base** | Papers are chunked, embedded, and stored in a persistent vector database (ChromaDB) |
| 🧵 **Chat History** | Full conversational history retained within a session, tab-organized UI |
| 🖥️ **Clean Tabbed UI** | Ask, Compare, and Analyze — organized into dedicated tabs for a focused workflow |

---

## 🎬 Demo

<div align="center">

*Add a screenshot or GIF of the app here*

```
[ screenshot: main chat interface ]
[ screenshot: paper comparison table ]
[ screenshot: research gap analysis ]
```

</div>

---

## 🏗️ Architecture

```
                         ┌─────────────────────┐
                         │     PDF Uploads       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Document Loader &   │
                         │   Chunking Pipeline    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  Embedding Manager     │
                         │  (Sentence/LLM Embeds) │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   ChromaDB Vector      │
                         │   Store (Persistent)   │
                         └──────────┬───────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              ▼                     ▼                     ▼
     ┌────────────────┐   ┌──────────────────┐   ┌──────────────────┐
     │   Retriever      │   │ Comparison Engine  │   │   Gap Finder       │
     │   + QA Engine     │   │                    │   │                    │
     └────────┬─────────┘   └─────────┬──────────┘   └─────────┬──────────┘
              │                       │                        │
              └───────────────────────┼────────────────────────┘
                                       ▼
                         ┌─────────────────────┐
                         │   Streamlit UI         │
                         │   (Tabbed Interface)   │
                         └─────────────────────┘
```

---

## 🛠️ Tech Stack

- **Frontend / App Framework:** [Streamlit](https://streamlit.io/)
- **Orchestration:** [LangChain](https://www.langchain.com/)
- **Vector Database:** [ChromaDB](https://www.trychroma.com/)
- **Language:** Python 3.10+
- **Embeddings & LLM:** *(add your specific provider — e.g. OpenAI, HuggingFace, Ollama)*

---

## 📂 Project Structure

```
ResearchMate/
├── app.py                     # Application entry point
├── core/
│   ├── embedding_manager.py   # Handles text embedding generation
│   ├── vector_store.py        # ChromaDB persistence & search logic
│   ├── retriever.py           # Retrieval logic across papers
│   ├── qa_engine.py           # Question-answering / synthesis engine
│   ├── comparison_engine.py   # Paper comparison table generation
│   └── gap_finder.py          # Research gap analysis logic
├── ui/
│   ├── pages.py                # Main page layout (tabs: Ask / Compare / Gaps)
│   ├── chat.py                 # Chat input & rendering components
│   └── components.py           # Sidebar & shared UI components
├── vectorstore/                # Persistent ChromaDB storage (generated)
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### Prerequisites

- Python 3.10 or higher
- pip / virtualenv

### Setup

```bash
# Clone the repository
git clone https://github.com/<your-username>/ResearchMate.git
cd ResearchMate

# Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root and add any required API keys:

```env
OPENAI_API_KEY=your_api_key_here
```

> ⚠️ Never commit your `.env` file or API keys to GitHub. Ensure `.env` is listed in `.gitignore`.

---

## 🚀 Usage

1. **Run the app**

   ```bash
   streamlit run app.py
   ```

2. **Upload papers** — Use the sidebar to upload one or more PDF research papers.

3. **Process documents** — Click **"Process Documents"** to chunk, embed, and store papers in the vector database.

4. **Explore via tabs:**
   - 💬 **Ask ResearchMate** — Ask questions across all uploaded papers
   - 📊 **Compare Papers** — Generate a structured comparison table
   - 🔍 **Research Gaps** — Run gap analysis across your knowledge base

---

## 🗺️ Roadmap

- [ ] Support for additional file formats (DOCX, TXT, web URLs)
- [ ] Export chat history & comparison tables (PDF / CSV)
- [ ] Multi-user / multi-session support
- [ ] Citation-aware answer generation (APA/MLA formatted)
- [ ] Advanced filtering by publication year, author, or topic
- [ ] Deployment guide (Streamlit Cloud / Docker)

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Aditya**
Third-year Computer Science & Robotics student | AI/ML & Software Engineering

- GitHub: [Aditya529-ux](https://github.com/Aditya529-ux)

---

<div align="center">

⭐ If you found this project useful, consider giving it a star!

</div>
