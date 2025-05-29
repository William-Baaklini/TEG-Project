# Generative AI Technologies (TEG) – Final Project

## 1. Goal
Design and build a **Python** solution that solves a real-world business problem using concepts from the course:

- Retrieval-Augmented Generation (RAG)
- Agentic / multi-agent systems (MAS)
- Model Context Protocol (MCP) servers
- Observability (LangSmith)

You will work in teams of **1–3**.

Larger teams can be approved if propsed solution is complex enough. The general idea is that the more people there are in a group the more complex and comprahensive should the final project be to account for the team size.

---

## 2. Deliverables
| Item | Where / Format |
|------|----------------|
| Source code | Public or private **GitHub** repo |
| Documentation | `README.md` with setup, usage, and architecture diagram |
| Half-time demo | Live in class – prototype + roadmap |
| Final demo | Live in class – end-to-end showcase |

---

## 3. Evaluation (max recorded score = 100)

| Category | Max pts | Notes |
|----------|---------|-------|
| Code quality | **10** | Clean, idiomatic Python; |
| Solution architecture | **20** | Frontend ↔ Backend ↔ DB ↔ MCP; scalability & security |
| RAG implementation | 20 | Chunking, vector store, prompt grounding |
| Multi-agent systems | 20 | Planner/Executor or equivalent |
| MCP integration | 20 | Custom or third-party MCP servers; safe tool calls |
| LangSmith monitoring | 5 | Monitoring implemented, runs logged |
| Git workflow | 5 | Branches, pull requests and code reviews, clear commit messages, .gitignore file |
| Half-time demo | 10 | Progress, blockers, next steps |
| Mini-projects | 20 | Submited during the semester |
| **Potential total** | **130** | Scores above 100 count as bonus buffer; final grade capped at 100 |

---

## 4. Timeline

| Date | Milestone |
|------|-----------|
| **Class 9 (Today)** | Form teams & submit project idea |
| **Class 11** | Half-time demo (10 pts) |
| **Class 12** | **Final demo & code freeze** |
| **Class 13** | Optional resubmission window closes |

---

## 5. Tech stack & constraints
- **Language**: Python 3.10+
- **LLM provider**: OpenAI (or any other online LLM provider f.e. Anthropic), or open-source model run locally on GPU
- **Frontend**: Streamlit recommended, any web/UI acceptable
- **Backend / MCP**: FastAPI or standalone MCP servers *recommended*

Projects being a single monoliths (or notebooks) are allowed, but will score significantly lower on Architecture.

---

## 6. Academic & Data Ethics
Respect licensing and privacy of any datasets or APIs. Cite all external resources. The university’s academic-integrity policy obviously applies.

Take care not to leak any API keys or sensitive data to public repositories. 
