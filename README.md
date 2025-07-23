# Offline Assistant (RAG-Ready Backend Core)

Build your own AI-powered assistant that *actually* stays private.  
No cloud. No data ever leaves your machine.  
Works with your favorite local LLMs (Ollama, LM Studio, LocalAI, llama.cpp—you pick).

---

## What Does It Do?

- Search your files and notes using AI (Retrieval-Augmented Generation, aka RAG)
- Ingests all kinds of files (PDF, TXT, DOCX, CSV, you name it)
- Plug-and-play with any local LLM—swap in whatever’s running
- Modular code: every core piece is a class, easy to hack/extend
- All data and embeddings are stored locally (ChromaDB, by default)
- FastAPI backend—REST API ready to go, or build your own UI on top
- Built-in health check so you know if things are working
- Utilities for scanning folders, extracting text, and queueing up stuff to learn

---

## Quickstart

**Works on macOS, Linux, Windows—wherever you want.**

1. **Get the code and install dependencies:**

    ```sh
    git clone https://github.com/YOURUSERNAME/offline_assistant.git
    cd offline_assistant
    python -m venv venv
    source venv/bin/activate  # or 'venv\Scripts\activate' on Windows
    pip install -r requirements.txt
    ```

2. **Pick your folders to scan:**  
   Edit `config.yaml` with whatever you want indexed.

3. **(Optional) Set up your LLM backend:**  
   Ollama, LM Studio, etc.—just run it locally and set `embedding_url` + `embedding_model` in `config.yaml`.

4. **Fire up the backend:**

    ```sh
    uvicorn app.main:app --reload
    ```

   The API is at [http://localhost:8000](http://localhost:8000) (Swagger docs included).

---

## For Developers: How to Actually Use It

Everything is class-based and modular.  
You don’t have to use the CLI scripts—just wire up what you want:

```python
from app.embeddings import Embedder
from app.db import ChromaDatabase
from app.learn import Learner
from app.queue import IngestQueue

embedder = Embedder()
db = ChromaDatabase()
learner = Learner(embedder, db)
queue = IngestQueue()

# Learn something
learner.learn_text("Hydrate the plants", {"type": "note"})

# Search your knowledge base
results = db.query_similar(embedder.embed("watering routine"))
print(results)
```

**Want to swap out the DB, embedder, or queue?**  
Just write a class with the same methods (`embed`, `add_entry`, etc.), and drop it in.

---

## API Endpoints

All the basics (and you can add more):

- **POST /add:** Add a note, log, or doc
- **POST /search:** Semantic search your stuff
- **POST /learn:** Add text from any source
- **POST /scan:** Scan folders and ingest files
- **GET /health:** Check if the LLM, DB, and queue are alive

Check [http://localhost:8000/docs](http://localhost:8000/docs) for the Swagger playground.

---

## Configuration

Edit `config.yaml` for everything:  
- Folders to index  
- File types to skip  
- ChromaDB location  
- Which LLM to use (Ollama, LM Studio, etc.)  
Or use environment variables if you want to override stuff.

---

## Extending & Customization

The Offline Assistant backend is designed to be **modular and developer-friendly**.  
Every major piece—the embedder, database, queue, and skills—can be replaced or extended with your own classes or APIs.

- Add your own FastAPI routes for new skills or integrations
- Subclass or swap out pipeline pieces (embedding, DB, queue, etc.)
- All you need to do is match the method signatures (like `.embed`, `.add_entry`, etc.)

If you want to contribute an extension, add to the docs, or just share your workflow, open an issue or pull request!


```python
@app.post("/summarize")
def summarize(payload: dict = Body(...)):
    text = payload.get("text")
    summary = my_summary_func(text)
    return {"summary": summary}
```

You can subclass anything, or replace any pipeline piece (embedding, DB, etc.).  
If you build something cool, make a PR or just show it off in the docs.

---

## Health Check

Not sure if stuff is running?  
`curl http://localhost:8000/health`  
…or just hit the `/health` endpoint in your browser.

---

## Contribution & Feedback

Open to feedback, bug reports, and especially new modules or docs.  
If you’re stuck or want to add something, open an issue or just reach out.

---

## License

MIT, use it however you want.

---

## Roadmap

- [ ] Plugin hot-reloading
- [ ] Auth/user management
- [ ] More built-in skills (summarize, reminders, etc.)
- [ ] Whatever else makes this more useful—suggest away!


