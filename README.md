# PhiloAgent

**Dead philosophers, alive again. Arguing about AI.**

PhiloAgent resurrects historical thinkers as AI agents. Socrates questions your assumptions. Nietzsche challenges your values. Descartes doubts your reality. All while grappling with the ethics of the technology that brought them back.

---

## The Problem

Philosophy died when it became academic. We need the dead to speak—directly, personally, about the machines we've built.

---

## How It Works

PhiloAgent runs a stateful, multi-agent workflow powered by LangGraph. At its core:

1. **Philosopher Selection** — Choose which philosopher(s) to consult
2. **Context Retrieval** — RAG system pulls relevant philosophical context from embeddings
3. **Agentic Processing** — LLM generates philosopher responses using role-specific personas and historical perspectives
4. **State Management** — Conversation state is persisted across sessions with intelligent summarization
5. **Long-term Memory** — Multi-turn conversations maintain coherence through MongoDB-backed memory

The system runs as a headless backend service. Conversations are stateful—the agent remembers context and automatically summarizes long exchanges to manage token usage.

---

## Architecture Overview

### Backend Stack

```
┌─────────────────────────────────────────┐
│        Conversation Interface            │
│      (WebSocket / API Endpoints)         │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│        LangGraph Workflow Engine         │
│  ┌──────────────────────────────────┐   │
│  │  conversation_node               │   │
│  │  - LLM inference (Groq)          │   │
│  │  - Natural dialogue generation   │   │
│  └──────────────────────────────────┘   │
│  ┌──────────────────────────────────┐   │
│  │  retriever_node                  │   │
│  │  - RAG context lookups           │   │
│  └──────────────────────────────────┘   │
│  ┌──────────────────────────────────┐   │
│  │  summarizer_nodes                │   │
│  │  - Conversation summarization    │   │
│  │  - Context compression           │   │
│  └──────────────────────────────────┘   │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│    Persistence & Observability Layer     │
│  ┌──────────┐  ┌──────────┐  ┌────────┐ │
│  │ MongoDB  │  │  Opik    │  │ Comet  │ │
│  │ Storage  │  │ Tracking │  │  ML    │ │
│  └──────────┘  └──────────┘  └────────┘ │
└─────────────────────────────────────────┘
```

### Key Components

| Component | Purpose | Details |
|-----------|---------|---------|
| **PhilosopherState** | Tracks conversation history, philosopher profile, and semantic context | Maintains philosopher name, perspective, style, historical context, and conversation summary for multi-turn coherence |
| **Workflow Graph** | LangGraph-based multi-node orchestration with conditional routing | Multi-node state machine with intelligent branching: conversation → tool detection → RAG retrieval → summarization |
| **RAG Engine** | Sentence Transformers embeddings + semantic retrieval for philosopher context | Encodes philosopher knowledge bases into 384-dim vectors; retrieves top-3 contextually relevant passages per query |
| **MongoDB Client** | Type-safe, persistent storage for conversations and philosopher profiles | Generic wrapper supporting any Pydantic model; persists state checkpoints, conversation writes, and long-term memory |
| **LLM Integration** | Groq API (llama-3.3-70b) for low-latency, cost-effective inference | Primary: Llama 3.3 70B (conversation). Secondary: Llama 3.1 8B (fast summarization) |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Language** | Python 3.9+ |
| **Workflow Orchestration** | LangGraph |
| **LLM Provider** | Groq (Llama 3.3 70B) |
| **Vector DB & Storage** | MongoDB + Atlas |
| **Embeddings** | Sentence Transformers (all-MiniLM-L6-v2) |
| **API Framework** | FastAPI (infrastructure ready) |
| **Observability** | Opik + Comet ML |
| **Package Management** | Python setuptools |

---


## Installation & Setup

### Prerequisites

- Python 3.9 or higher
- MongoDB Atlas account (or local MongoDB instance)
- API Keys:
  - **Groq API Key** — Get at [console.groq.com](https://console.groq.com)
  - **OpenAI API Key** (optional, for evaluation)
  - **Comet ML Key** (optional, for observability)

### Quick Start

#### 1. Clone & Install

```bash
git clone https://github.com/yourusername/philoagent.git
cd philoagent
pip install -e .
```

#### 2. Configure Environment

Create a `.env` file in the project root:

```env
# LLM Configuration
GROQ_API_KEY=your_groq_api_key_here
GROQ_LLM_MODEL=llama-3.3-70b-versatile
GROQ_LLM_MODEL_CONTEXT_SUMMARY=llama-3.1-8b-instant

# OpenAI (optional, for evaluation)
OPENAI_API_KEY=your_openai_key_here

# MongoDB
MONGO_URI=mongodb+srv://user:password@cluster.mongodb.net/philoagent?retryWrites=true&w=majority
MONGO_DB_NAME=philoagent

# Observability (optional)
COMET_API_KEY=your_comet_key_here
COMET_PROJECT=philoagents_course

# Agent Behavior
TOTAL_MESSAGES_SUMMARY_TRIGGER=30
TOTAL_MESSAGES_AFTER_SUMMARY=5

# RAG Configuration
RAG_CHUNK_SIZE=256
RAG_TOP_K=3
```


## Project Structure

```
philoagent/
├── config.py                          # Pydantic settings & configuration
├── domain/
│   ├── philosopher.py                 # Philosopher model & schema
│   ├── philosopher_factory.py          # Factory for creating philosopher instances
│   ├── prompts.py                      # Prompt templates with Opik versioning
│   └── exceptions.py                   # Custom exceptions
├── application/
│   ├── long_term_memory.py             # Memory abstraction layer
│   ├── conversation_service/
│   │   └── workflow/
│   │       ├── graph.py               # LangGraph workflow definition
│   │       ├── nodes.py               # Individual workflow nodes
│   │       ├── edges.py               # Conditional routing logic
│   │       ├── state.py               # PhilosopherState definition
│   │       ├── chain.py               # Planning chains
│   │       ├── tools.py               # Tool definitions
│   │       └── settings.py            # Workflow-specific settings
│   ├── infrastructure/
│   │   ├── api.py                     # FastAPI application (skeleton)
│   │   ├── opik_utils.py              # Opik integration helpers
│   │   └── mongodb/
│   │       ├── client.py              # Type-safe MongoDB wrapper
│   │       └── index.py               # Database indexes & setup
│   ├── data/
│   │   ├── extract.py                 # Philosopher data extraction
│   │   └── deduplicate_documents.py   # Document deduplication
│   └── rag/
│       ├── embeddings.py              # Embedding model initialization
│       ├── retrievers.py              # RAG retrieval logic
│       └── splitters.py               # Text splitting strategies
```

---

## Development Workflow

### Running Tests

```bash
pytest tests/ -v
```

### Building the Package

```bash
pip install build
python -m build
```

### Updating Configuration

All settings live in `.env`. The `config.py` file auto-loads them via Pydantic:

```python
from philoagent.config import settings
print(settings.GROQ_LLM_MODEL)  # Loads from .env
```

## Visual Workflow Diagram

The diagram below illustrates the core agentic loop:

```
User Message
    ↓
[conversation_node]
    ├─→ LLM generates philosopher response
    ├─→ Detects tool usage
    └─→ Routes conditionally...
    
    ├─ If tools needed → [retriever_node]
    │                      ├─→ Semantic search for context
    │                      └─→ [summarizer_context_node]
    │                           └─→ Back to conversation_node
    │
    └─ If complete → [connector_node]
                        └─→ Checks message count...
                            ├─ If > 30 msgs → [conversation_summarizer]
                            │                  └─→ END
                            └─ Else → END

Response sent to user via API/WebSocket
↓
[MongoDB Storage] persists state + messages
↓
[Opik Tracking] logs metrics & quality signals
```

---

## Key Concepts

### PhilosopherState

The core state object that maintains conversation coherence:

```python
class PhilosopherState(MessagesState):
    philosopher_context: str          # Historical/biographical context (e.g., "Greek philosopher, 470-399 BC")
    philosopher_name: str              # "Socrates", "Nietzsche", "Descartes", etc.
    philosopher_perspective: str       # Their unique AI/technology viewpoint grounded in their philosophy
    philosopher_style: str             # Communication style (e.g., "Questioning, dialectical, educational")
    summary: str                        # Auto-generated conversation summary (updated every 30 messages)
```

**Purpose**: Extends LangGraph's MessagesState to preserve philosopher identity and context across the multi-turn conversation. This allows the LLM to maintain character consistency while building on previous exchanges.

### Intelligent Summarization

After 30 messages, the system auto-summarizes conversation to reduce token usage:

```
Before: All 30+ previous messages (high token cost)
         ↓
After:  Single compressed summary + last 5 messages (90% reduction)
```

**Benefits**: Dramatically reduces API costs, maintains context window for longer conversations, prevents context bloat.

**Implementation**: When `TOTAL_MESSAGES_SUMMARY_TRIGGER` is reached, the `summarize_conversation_node` condenses all chat history using Llama 3.1 8B (fast & cheap), then replaces full history with summary in state.

### RAG-Augmented Responses

The retriever node performs semantic search over philosopher knowledge bases:

1. **User Query** → Encoded to 384-dim vector (Sentence Transformers)
2. **Semantic Search** → Top-3 similar passages retrieved from MongoDB
3. **Prompt Injection** → Retrieved context injected into LLM prompt
4. **Authentic Response** → LLM generates response grounded in philosopher's writings

**Result**: Responses are historically accurate and traceable to source material.

### Workflow Conditional Routing

LangGraph's `tools_condition` and custom edge functions enable intelligent branching:

```
- If LLM requests tools → Call retriever_node (RAG lookup)
- If response complete → Route to connector_node (check message count)
- If 30+ messages → Summarize and END
- Else → END (return response to user)
```

**Benefit**: Automatic decision-making without explicit if/else code; scales to complex multi-node pipelines.

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Acknowledgments

- **LangGraph** for the elegant workflow orchestration
- **Groq** for lightning-fast LLM inference
- **MongoDB** for reliable data persistence
- Philosophy community for timeless wisdom

---
