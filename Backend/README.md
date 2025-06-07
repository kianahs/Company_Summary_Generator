
# Company Summary Generator

This project extracts and summarizes structured content from company websites using a configurable pipeline. It supports both traditional LLM summarization and Retrieval-Augmented Generation (RAG), using Groq, OpenAI, and Google GenAI APIs. The final outputs are in this directory:

```
Outputs/
└── filament/
    └── Final Summary/
        ├── RAG/
        └── llama3-70b-8192/ or gpt-4.1-mini/
```


---

## ⚙️ Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/kianahs/Company_Summary_Generator.git
cd Company_Summary_Generator
```
## 2. Environment Variables

Create a `.env` file in the root folder with your API keys:

```env
GROQ_API_KEY=your-groq-api-key
GOOGLE_API_KEY=your-google-api-key
OPENAI_API_KEY=your-openai-api-key
```
### 3. Run the Setup Script

```bash
bash run.sh
```

This script will:

* Create a virtual environment
* Install all required dependencies
* Execute `main.py` using your local `config.json`

---

## 📄 Configuration (`config.json`)

You can control the pipeline flow using this JSON configuration:

```json
{
  "pipeline": {
    "RAG": {
      "active": true,
      "free_plan": true
    },
    "free_summarizer_llm": true,
    "free_merger_llm": true
  },
  "endpoints": [
    "", "features", "why-syfter", "resources",
    "about-us", "technical-information", "contact"
  ],
  "navbar": [
    "Home", "Features", "Why Syfter", "Resources",
    "About Us", "Technical Information", "Contact", "Book A Demo"
  ],
  "url": "https://filament.ai",
  "company": "filament",
  "root_dir": "Outputs"
}
```


## 📁 Output Directory Structure

```
Outputs/
└── filament/
    ├── Scraped Data/
    ├── Cleaned Scraped Data/
    ├── Summaries/
    └── Final Summary/
        ├── RAG/
        └── llama3-70b-8192/ or gpt-4.1-mini/
```

