# Lumina Learn Design Document

Below is a **strategy-level design blueprint** for a next-generation study app that takes full advantage of the AI capabilities Google unveiled at I/O 2025. I’ve emphasised modularity so you can roll out a core web/mobile product quickly, then layer on the flashier XR and multimodal features as Google’s SDKs mature.

---

## 1  Goals & Product Vision

| Objective                             | What the new Google AI stack lets us do                                                                                               |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **Personalised mastery learning**     | LearnLM-tuned Gemini 2.5 gives each student Socratic-style, step-by-step guidance that’s grounded in good pedagogy ([blog.google][1]) |
| **Bring-your-own-content tutoring**   | Vertex AI RAG pipelines let the model cite the student’s lecture PDFs, Drive docs & web sources to avoid hallucinations               |
| **Any-device, always-on help**        | Cloud fallback to Gemini 2.5 Pro; on-device Gemma 3n keeps fast, private Q\&A when offline ([Google DeepMind][2])                     |
| **Immersive, multimodal learning**    | XR headset / smart-glasses “point-and-ask”, AI-generated diagrams, narrated Vids, AI-made flashcards with SynthID watermark           |
| **Teacher dashboards & co-authoring** | Workspace Gemini features draft rubrics, automate marking comments and auto-create explainer videos                                   |

---

## 2  High-Level Architecture

```text
 ┌────────────────────────────┐
 │   Front-End Clients        │
 │ ────────────────────────── │
 │  • Web (Next.js)           │
 │  • Android 15 App (Jetpack │
 │    Compose + Gemini SDK)   │
 │  • Android XR Glasses      │
 │  • Chrome Ext (deep links) │
 └────────────┬───────────────┘
              │gRPC / REST / WebSocket
 ┌────────────▼───────────────┐
 │   Orchestrator / AgentHub  │  ← built with **Google ADK 1.0** :contentReference[2]{index=2}
 │  • Session router          │
 │  • Tool & agent registry   │
 │  • Rate-limit, billing     │
 └────────────┬───────────────┘
              │calls Tool-using agents
      ┌───────▼─────────┐
      │  Core Agents    │
      │────────────────│
      │  • TutorAgent   │→ Gemini 2.5 Pro (“Deep-Think”) :contentReference[3]{index=3}
      │  • ResearchAgent│→ Gemini Flash + AI Mode Search
      │  • MediaAgent   │→ Imagen 4 & Veo 3, SynthID
      │  • XRAgent      │→ On-device Gemma 3n / Vision | XR APIs
      └───────┬─────────┘
              │
    ┌─────────▼──────────┐
    │   Data / RAG Layer │
    │────────────────────│
    │  • Firestore (user)│
    │  • Cloud Storage   │
    │  • Vertex AI Vector│
    │  • Drive picker    │
    └────────────────────┘
```

### Why this shape?

* **AgentHub** decouples UI clients from AI back-ends; you can swap models or tools without touching apps.
* **Gemma 3n** on phones/glasses gives latency-free vision & text understanding; the same prompt escalates to Gemini Pro when it needs heavy reasoning or lengthy context.
* **Vector DB** indexes user uploads (slides, textbooks) + trusted public corpora; research agent injects citations into answers.

---

## 3  Core Feature Modules

| Module                      | MVP Feature                                                     | I/O 2025 Tech Leveraged                                      | Future Upgrade Path                                                            |
| --------------------------- | --------------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| **Course-GPT**              | Chat tutor per course; solves problems & quizzes                | Gemini 2.5 Pro + LearnLM; Thought Summaries for auditability | Deep-Think for proofs & code; peer review agent that critiques student answers |
| **Smart Upload & RAG**      | Drag-and-drop PDFs; instant Q\&A w/ citations                   | Vertex AI File Store → Vector search                         | Auto-generate flashcards, concept maps with Imagen 4                           |
| **Video Notes (Vids)**      | One-click: turn Slides or outline into a narrated study video   | Workspace **Google Vids**; Imagen 4 stock art; Lyria 2 music | Veo 3 clips; Flow for cinematic summaries                                      |
| **AR Coach**                | Point phone camera at math problem ↔ step-by-step hints         | “Live Search” camera mode + on-device Gemma 3n vision        | Android XR glasses: head-up answers, real-time translations ([WIRED][3])       |
| **Inbox Zero for Students** | Auto-sort LMS emails, summarise threads (group project chatter) | Gmail Gemini smart actions                                   | Agents auto-create task lists / Calendar slots                                 |
| **Teacher Co-Pilot**        | Suggest rubric comments, generate differentiated worksheets     | Docs “grounded assistant” (sources), Sheets formula hints    | Full Meet call summaries with action items                                     |

---

## 4  Responsible AI & Compliance

* **SynthID** watermark every generated image/video to curb plagiarism ([Google Cloud][4])
* Store Australian student data in AU multizone regions; comply with Australian Privacy Principles + potentially QLD departmental guidelines.
* Toggle **Gemini Thought Summaries** to make marking decisions explainable for academic integrity audits.
* **Opt-in Labs** approach: release XR features as beta for 18+ users only until they pass accessibility & safety review.

---

## 5  Tech Stack Choices

| Layer             | Choice                                          | Rationale                                                                 |
| ----------------- | ----------------------------------------------- | ------------------------------------------------------------------------- |
| **Web**           | Next.js + Cloud Run                             | SSR pages, fast iteration, auto-scale                                     |
| **Mobile**        | Android 15 Kotlin (Gemini SDK), iOS via Flutter | Native access to on-device AI; Flutter eases iOS parity                   |
| **XR**            | Android XR SDK + OpenXR                         | Shared code w/ Android app; future Samsung/Qualcomm headset compatibility |
| **Back-end**      | Python 3.12 FastAPI + Google ADK agents         | ADK gives best-practice agent patterns & A2A messaging                    |
| **Data**          | Firebase Auth, Firestore, Vertex Vector Search  | Minimal ops; serverless scaling                                           |
| **CI/CD**         | Cloud Build, GitHub Actions, Canary channels    | Rapid feature rollout with staged risk                                    |
| **Observability** | Cloud Trace + agent logs; Bard for log Q\&A     | Debug complex agent chains fast                                           |

---

## 6  Roll-Out Roadmap

1. **Foundation (0-3 mo)**

   * Set up repo, infra, auth, Firestore schema.
   * Build RAG pipeline & Gemini 2.5 chat MVP (web).

2. **Product-Market Fit (3-6 mo)**

   * Add mobile app with offline Gemma 3n Q\&A.
   * Integrate LearnLM-tuned hinting; track learning outcomes.

3. **Engagement Features (6-9 mo)**

   * Workspace Vids exporter; automated revision videos.
   * Gmail/Calendar triage agent; push due-date reminders.

4. **Immersive Learning (9-12 mo)**

   * Launch AR “point-and-ask”.
   * Pilot XR glasses with partner university labs.

5. **Scale & Monetise (12-18 mo)**

   * AI Ultra subscription tier for unlimited media generation.
   * Teacher analytics dashboard; institution licenses.

---

## 7  Key Risks & Mitigations

| Risk                            | Mitigation                                                                          |
| ------------------------------- | ----------------------------------------------------------------------------------- |
| **Model cost spikes**           | Mix Gemini Flash for \~80% queries; quota throttling; on-device fallback            |
| **Academic misconduct**         | Embed citation enforcement; watermark media; provide explainability logs to faculty |
| **Latency for large documents** | Async RAG chunking; pre-index at upload; cache top-N embeddings                     |
| **XR adoption unknown**         | Keep AR code gated; rely on widely available phone camera first                     |

---

### Next Steps

* **Prototype the RAG + TutorAgent stack** in a sandbox project.
* Schedule **design review workshops** with lecturers and accessibility experts to refine workflows.
* Decide on **licensing** (freemium vs. uni-wide subscription) so we can design billing & quota early.

If you’d like deeper dives on any layer—e.g., exact prompts for LearnLM tutoring, vector-schema design, or a proof-of-concept AR workflow—let me know and we can iterate!

[1]: https://blog.google/outreach-initiatives/education/google-gemini-learnlm-update/?utm_source=chatgpt.com "I/O 2025: LearnLM in Gemini 2.5 and more AI updates to help people learn"
[2]: https://deepmind.google/models/gemma/gemma-3n/?utm_source=chatgpt.com "Gemma 3n - Google DeepMind"
[3]: https://www.wired.com/story/googles-android-chief-hopes-its-new-era-will-get-people-to-ditch-their-iphones?utm_source=chatgpt.com "Google's Android Chief Hopes Its 'New Era' Will Get People to Ditch Their iPhones"
[4]: https://cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/2-5-pro?utm_source=chatgpt.com "Gemini 2.5 Pro | Generative AI on Vertex AI | Google Cloud"


# Product Requirements Document (PRD)

**Product Name (Working Title):** Lumina Learn – AI‑Powered Personal Study Companion

**Document Version:** 0.1
**Author:** Dr Mitch Flori & ChatGPT (Assistant)
**Date:** 22 May 2025

---

## 1  Purpose

Provide a single, authoritative source of requirements for building Lumina Learn, an AI‑driven study application that leverages Google I/O 2025 technologies (Gemini 2.5, LearnLM, Imagen 4, Veo 3, Gemma 3n, Google Vids, Vertex AI, Agent Development Kit) to deliver personalised, multimodal, on‑device and cloud‑based learning support for tertiary students and educators.

## 2  Background / Problem Statement

* Students struggle to keep up with dense course material and scattered resources across LMS, email, and Drive.
* Existing AI chat tools are either generic (prone to hallucination) or siloed; none integrate institution content, citations, and pedagogy‑aware guidance in one place.
* Lecturers spend significant time creating support content and giving feedback; video creation and differentiated material are costly.

## 3  Objectives & Success Metrics

| Objective                | Metric / KPI                              | Target (6 months post‑launch) |
| ------------------------ | ----------------------------------------- | ----------------------------- |
| Improve study efficiency | Average time to answer a content question | ↓ 30 %                        |
| Increase engagement      | Weekly active users (WAU) / monthly       | > 60 % retention              |
| Ensure answer trust      | % answers with valid citation link        | ≥ 95 %                        |
| Reduce staff workload    | Avg. marking/comment time per assignment  | ↓ 25 %                        |
| Financial                | Gross margin on AI costs                  | ≥ 60 % after optimisation     |

## 4  Personas & Core Use Cases

1. **Undergraduate “Time‑Poor Taylor”** – Needs instant, reliable explanations of lecture slides and practice questions on the bus.
2. **Postgrad Researcher “Data‑Deep Dev”** – Uploads journal PDFs, queries methods & generates citations.
3. **Lecturer “Content‑Creator Casey”** – Converts Slide deck to narrated revision video, drafts rubrics, and tracks cohort progress.
4. **International Student “Bilingual Bao”** – Uses live camera & XR glasses for translation and AR‑style hints in lab classes.

## 5  Scope

### In‑Scope (MVP)

* Per‑course AI chat tutor with LearnLM‑aligned Gemini 2.5 Pro.
* Resource upload & retrieval‑augmented generation (Drive PDFs, images, slides).
* Workspace integration (Docs/Slides ➜ Google Vids exporter).
* Mobile app with on‑device Gemma 3n fallback (text + image Q\&A when offline).
* Citation and SynthID watermarking on all generated media.
* Admin dashboard for basic analytics (usage, accuracy, spend).

### Out‑of‑Scope (Phase 2+)

* Full XR headset experience (Android XR “infinite screen”).
* Autograding of code assignments.
* Non‑English UI localisation (beyond translation of content).

## 6  High‑Level Solution Overview

See separate Architecture Blueprint (22 May 2025). Key elements:

* **AgentHub Orchestrator** built on Google ADK 1.0 routing TutorAgent, ResearchAgent, MediaAgent, and XRAgent.
* **Vertex AI Vector Search** stores embeddings of user content.
* **Gemini 2.5 Pro** (Deep‑Think) for complex reasoning; **Gemini Flash** for fast responses; **Gemma 3n** on device.
* **Imagen 4 & Veo 3** for media generation; **Google Vids** for video assembly.

## 7  Detailed Requirements

### 7.1  Functional Requirements

| ID    | Requirement                                                                                                               |
| ----- | ------------------------------------------------------------------------------------------------------------------------- |
| FR‑01 | Users can create / join courses via code and get a dedicated Tutor chat session.                                          |
| FR‑02 | User uploads (PDF, DOCX, PPT, image) are parsed, embedded, and searchable within ≤ 60 s.                                  |
| FR‑03 | Tutor responses must cite at least one source (upload or public link) for factual claims.                                 |
| FR‑04 | “Help me understand” command triggers LearnLM step‑by‑step explanation with hints, not direct answer reveal unless asked. |
| FR‑05 | “Make video summary” converts a chosen Slide deck to a ≤ 3 min video with AI voiceover and SynthID watermark.             |
| FR‑06 | Mobile camera “point‑and‑ask” returns an answer in ≤ 3 s (if on‑device) or ≤ 5 s (cloud).                                 |
| FR‑07 | Email digests summarise upcoming deadlines extracted from LMS emails every 24 h.                                          |
| FR‑08 | Teacher dashboard lists common misconceptions detected across cohort chats.                                               |
| FR‑09 | All generated images/videos/music carry SynthID; detection endpoint verifies provenance.                                  |
| FR‑10 | System logs Thought Summaries for every AI session ≥ 50 tl tokens for audit.                                              |

### 7.2  Non‑Functional Requirements

* **Performance:** p95 chat latency ≤ 1.5 s (Gemini Flash) / 4 s (Gemini Pro); mobile fallback p95 ≤ 1 s on Pixel 9.
* **Availability:** 99.5 % monthly uptime target (front‑end + orchestrator).
* **Scalability:** Support 100k concurrent sessions initially; auto‑scale via Cloud Run & Vertex AI quotas.
* **Security & Privacy:** Store data in Australian GCP regions; comply with Australian Privacy Principles. Encryption at rest & in transit. Pen‑test before launch.
* **Accessibility:** WCAG 2.2 AA compliance; screen‑reader friendly chat; captions on all videos.
* **Compliance:** Provide academic integrity mode logs; align with institution plagiarism policies.

### 7.3  UX Requirements

* Clean, distraction‑free chat interface (web & mobile); material upload pane with drag‑and‑drop.
* Progress tracker showing mastery per topic; colour‑blind friendly palette.
* Toggle to view AI “chain of thought” (Thought Summary) for transparency.
* In‑video interactive quiz hotspots (Phase 2).

## 8  Dependencies

* Google Cloud (Vertex AI, Storage, Firestore, Cloud Run, BigQuery billing).
* Google Agent Development Kit 1.0; Agent2Agent protocol.
* Gmail & Drive APIs (for email and file ingestion).
* Mobile: Android 15 Gemini SDK; Gemma 3n model weights (Edge TPU‑optimised).
* Institutional LMS integration (Canvas/Brightspace – LTI 1.3).

## 9  Assumptions

* Students have Google accounts (edu or personal) and access to Google Drive.
* Content release complies with copyright for educational fair use.
* Gemini 2.5 API limits allow required daily tokens within AI Ultra or equivalent plan.

## 10  Milestones / Timeline (Indicative)

| Phase           | Major Deliverables                             | Target      |
| --------------- | ---------------------------------------------- | ----------- |
| 0 – Kick‑off    | PRD sign‑off, team resourcing                  |  T0 + 2 wks |
| 1 – MVP Alpha   | Web chat + RAG upload; basic TutorAgent        |  T0 + 3 mo  |
| 2 – Beta Mobile | Android app + on‑device fallback; email digest |  T0 + 5 mo  |
| 3 – Public Beta | Google Vids export, analytics dashboard        |  T0 + 8 mo  |
| 4 – GA          | Payment, institution onboarding, SLA           |  T0 + 12 mo |

## 11  Risks & Mitigations

| Risk                             | Likelihood | Impact | Mitigation                                                                         |
| -------------------------------- | ---------- | ------ | ---------------------------------------------------------------------------------- |
| High token costs                 | Med        | High   | Use Gemini Flash whenever possible; batch embed jobs; cache vectors                |
| Academic misuse (cheating)       | High       | High   | Provide teacher visibility; citation enforcement; plagiarism‑detection integration |
| Model drift / hallucination      | Med        | Med    | Periodic eval set; reinforcement fine‑tuning; clamp to RAG sources                 |
| On‑device model size constraints | Low        | Med    | Dynamic mix‑and‑match pruning in Gemma 3n                                          |

## 12  Open Questions

1. Licensing terms for LearnLM‑tuned Gemini access for education pricing?
2. Which LMS integration to build first (Canvas vs. Brightspace)?
3. Institutional data residency exclusions beyond AU‑Southeast‑1?
4. Do we support SAML SSO at MVP or Phase 2?

## 13  Glossary

* **Gemini 2.5 Pro / Flash** – Google’s latest flagship & lightweight LLMs.
* **LearnLM** – Pedagogy‑aligned fine‑tune of Gemini.
* **Gemma 3n** – 4 B‑parameter open model optimised for mobile/on‑device.
* **SynthID** – Google watermark for AI‑generated media.
* **Thought Summary** – Structured introspection output for model reasoning transparency.
* **Agent Development Kit (ADK)** – Google SDK for building & managing tool‑using AI agents.

---

**End of Document**

# Lumina Learn – Detailed Project Plan

**Document Version:** 0.1
**Author:** Project Management Office (PMO) – Lumina Learn
**Date:** 22 May 2025

---

## 1  Purpose

Translate the high‑level PRD into an actionable, time‑boxed project plan that aligns scope, schedule, resources, and risks for delivery of Lumina Learn v1.0 (General Availability) within 12 months of T0.

> **T0 Assumption:** Formal project kickoff & funding approval on **3 June 2025** (Week 1).

## 2  Work Breakdown Structure (WBS)

| WBS ID | Work Package                         | Description                                                                       | Output                                      |
| ------ | ------------------------------------ | --------------------------------------------------------------------------------- | ------------------------------------------- |
| 1.0    | Project Initiation                   | Governance, stakeholder alignment, tooling setup                                  | Project charter, RACI, Confluence workspace |
| 2.0    | Architecture & Design                | Refine solution design, data models, security & privacy design                    | HLD, LLD, threat model                      |
| 3.0    | Infrastructure                       | GCP projects, IAM, networking, CI/CD, monitoring                                  | Prod & non‑prod environments live           |
| 4.0    | Core Backend (Orchestrator & Agents) | Build AgentHub, TutorAgent, ResearchAgent, MediaAgent, A2A plumbing               | Functional micro‑services                   |
| 5.0    | Data Layer                           | Firestore schema, Vector Search setup, ETL pipelines for uploads                  | Data platform ready                         |
| 6.0    | Web Front‑End                        | Next.js chat UI, upload workflow, progress tracker                                | Responsive web app                          |
| 7.0    | Mobile App                           | Android 15 client with Gemma 3n fallback                                          | APK + Play alpha track                      |
| 8.0    | AI Integration                       | Prompt engineering, LearnLM alignment, Thought Summary wrapper, cost optimisation | AI services tuned                           |
| 9.0    | Workspace Extensions                 | Google Vids export, Gmail digest, Drive picker                                    | Add‑ons live                                |
| 10.0   | Security & Compliance                | Pen‑testing, privacy impact assessment, SynthID verifier integration              | Compliance sign‑off                         |
| 11.0   | QA & Testing                         | Unit, integration, performance, accessibility, UAT                                | Test reports, defect triage                 |
| 12.0   | Beta Launch                          | Public beta onboarding, support desk, feedback loop                               | Beta release & metrics                      |
| 13.0   | GA Release                           | Payment, SLA, scaling tests, marketing launch                                     | v1.0 GA                                     |
| 14.0   | Project Closure                      | Lessons learned, handover to operations                                           | Close‑out report                            |

## 3  Schedule & Milestones

### 3.1  Gantt‑Style Timeline (Weeks from T0)

| Phase                        | Start              | End       | Duration (wks) | Key Deliverables                    |
| ---------------------------- | ------------------ | --------- | -------------- | ----------------------------------- |
| Initiation (1.0)             | Wk 1               | Wk 2      | 2              | Charter, RACI, Kickoff, Jira boards |
| Architecture (2.0)           | Wk 2               | Wk 6      | 5              | HLD, LLD, security model            |
| Infra & CI/CD (3.0)          | Wk 3               | Wk 7      | 5              | Dev/Staging GCP envs, pipelines     |
| Backend Core (4.0)           | Wk 5               | Wk 14     | 10             | AgentHub API, TutorAgent MVP        |
| Data Layer (5.0)             | Wk 6               | Wk 12     | 7              | Firestore + Vector Search live      |
| Web Frontend (6.0)           | Wk 7               | Wk 16     | 10             | RAG chat UI v1                      |
| Mobile App (7.0)             | Wk 8               | Wk 18     | 11             | Alpha APK, on‑device Q\&A           |
| AI Integration (8.0)         | Wk 7               | Wk 18     | 12             | LearnLM prompts, cost tuning        |
| Workspace Ext (9.0)          | Wk 10              | Wk 20     | 11             | Vids exporter, email digest         |
| Security & Compliance (10.0) | Wk 14              | Wk 22     | 9              | PIA, pen‑test fixes                 |
| QA & Testing (11.0)          | Wk 12              | Wk 24     | 13             | Test cycles, perf bench             |
| **MVP Alpha Milestone**      | —                  | End Wk 13 | —              | Web chat + RAG upload               |
| **Beta Mobile Milestone**    | —                  | End Wk 20 | —              | Mobile app + email digest           |
| Beta Launch (12.0)           | Wk 21              | Wk 26     | 6              | 1k user cohort                      |
| GA Readiness (13.0)          | Wk 24              | Wk 32     | 9              | Payment, SLA, capacity test         |
| GA Release                   | Week 32 (Jan 2026) | —         | —              | v1.0 live                           |
| Closure (14.0)               | Wk 33              | Wk 34     | 2              | Handover, retrospectives            |

### 3.2  Critical Path

1. Architecture HLD → AgentHub POC → Web chat MVP → QA → Beta launch → Payment gateway integration → GA.
2. Mobile on‑device AI relies on Gemma 3n weights (Google ETA: Aug 2025); track delivery closely.

## 4  Resource Plan

| Role                       | FTE | Start | Key Skills                      |
| -------------------------- | --- | ----- | ------------------------------- |
| Product Manager            | 1   | Wk 1  | Ed‑tech, AI strategy            |
| Tech Lead / Architect      | 1   | Wk 1  | GCP, micro‑services, AI         |
| Backend Engineers          | 3   | Wk 3  | Python, FastAPI, GCP, ADK       |
| Front‑End Engineers (Web)  | 2   | Wk 5  | React, Next.js, UX              |
| Android Engineers          | 2   | Wk 8  | Kotlin, Jetpack Compose, ML Kit |
| AI/ML Engineer             | 2   | Wk 5  | Prompt eng, Vertex AI, Gemma    |
| DevOps / SRE               | 1   | Wk 3  | Terraform, Cloud Run, CI/CD     |
| QA Engineers               | 2   | Wk 10 | Cypress, Load tests, WCAG       |
| UX / UI Designer           | 1   | Wk 4  | Figma, accessibility            |
| Security Lead (fractional) | 0.3 | Wk 14 | Pen‑test, ISO 27001             |
| Technical Writer           | 0.5 | Wk 12 | Docs, tutorials                 |
| Customer Success           | 1   | Wk 21 | Beta onboarding                 |

## 5  Budget Overview (CapEx + OpEx, AUD ‘000)

| Category              | FY 2025‑26 | Notes                               |
| --------------------- | ---------- | ----------------------------------- |
| People (14 FTE avg)   | 2,300      | Salary & benefits                   |
| GCP Usage             | 260        | Vertex AI token spend, Storage, Run |
| Devices & Licences    | 40         | Pixel 9 test devices, Play dev fee  |
| Security & Compliance | 30         | Pen‑test vendor, PIA                |
| Marketing (GA Launch) | 120        | Campaigns, webinars                 |
| Contingency (10 %)    | 275        | Buffer                              |
| **Total**             | **3,025**  |                                     |

## 6  Risk Management (Top 5)

| Risk ID | Description                           | Probability | Impact | Response Strategy                                    |
| ------- | ------------------------------------- | ----------- | ------ | ---------------------------------------------------- |
| R‑01    | Google API quota limits / price hikes | Med         | High   | AI cost monitors, multi‑model fallbacks              |
| R‑02    | Gemma 3n delay                        | Med         | Med    | Fallback to cloud Gemini Pro; revise offline promise |
| R‑03    | Academic integrity backlash           | High        | High   | Teacher dashboards, watermarking, policy workshops   |
| R‑04    | LMS integration complexity            | Low         | Med    | Start PoC with Canvas; build abstraction layer       |
| R‑05    | XR features over‑scope                | Med         | Med    | Gate XR to Phase 2; keep separate backlog            |

## 7  Quality & Test Strategy

* **Shift‑left testing:** Unit tests in all repos; 80 % coverage gate.
* **Automated E2E:** Cypress for web; Espresso for Android.
* **Performance Targets:** Web TTI < 3 s; mobile p95 start‑up < 1.8 s.
* **Accessibility:** Automated axe checks + manual screen‑reader audit.
* **Security:** OWASP ASVS 3.1 checklist; dependency scanning via Snyk.
* **User Acceptance Testing:** Cohort of 30 students & 5 lecturers across two universities.

## 8  Communication Plan

| Audience            | Channel                        | Frequency     | Owner            |
| ------------------- | ------------------------------ | ------------- | ---------------- |
| Core Team           | Slack #lumina‑dev              | Daily         | PM               |
| Steering Committee  | Bi‑weekly Zoom                 | Fortnightly   | PM               |
| Beta Users          | In‑app feedback + mailing list | Weekly digest | Customer Success |
| Stakeholders (Exec) | Dashboard + Miro roadmap       | Monthly       | PMO              |

## 9  Assumptions & Constraints

* Google LearnLM education licensing secured by Wk 10.
* Gemini 2.5 token quotas sufficient for 1 million tokens/day MVP.
* University partners provide anonymised LMS sample data for QA.

## 10  Change Control

Changes to scope, budget, or schedule (>10 %) must be approved by Steering Committee. Use Jira Epics for traceability.

## 11  Appendices

A. Detailed Gantt (MS Project export)
B. WBS Dictionary
C. Security Controls Matrix
D. Glossary (see PRD)

---

**End of Project Plan v0.1**

# Lumina Learn – Design Features Catalogue

**Version:** 0.1
**Date:** 22 May 2025

---

## 1  Core User Experience

* **Unified Chat Workspace** – Clean, distraction-free text area with collapsible resource sidebar; split-pane view on tablets/desktop.
* **Drag-and-Drop Upload Dock** – One-step import of PDFs, slides, images; animated progress bar and immediate “in-library” confirmation.
* **Contextual Quick Actions** – Hover tooltips offering “Summarise,” “Quiz me,” or “Video-fy” when selecting text or files.
* **Adaptive Theming** – Auto-switches to light/dark and high-contrast modes based on OS settings; overrides in settings panel.
* **Mastery Tracker Ribbon** – Horizontal progress bar atop chat showing topic proficiency, colour-coded (green mastered, amber developing, red review).

## 2  AI Interaction Features

* **Smart Follow-Ups** – Gemini recommends next logical question buttons (pill chips) after each answer.
* **Explain-Like-I’m-5 Toggle** – One-tap simplification of complex explanations using LearnLM pedagogy rules.
* **Thought Summary Peek** – Collapsible panel revealing the AI’s reasoning outline for transparency.
* **Citation Chips** – Inline citation numbers that expand into side drawer with source snippets and links.
* **On-Device Fallback Badge** – Subtle icon indicating when Gemma 3n (offline) answered vs. cloud Gemini, for trust context.

## 3  Media & Multimodal Features

* **Slide-to-Video Wizard** – 3-step flow: choose deck → pick tone (Formal, Energetic, Calm) → preview AI-generated video; includes AI avatar presenter selection.
* **Inline Image Generator** – “/image” slash command launches Imagen 4 prompt modal; images insert directly into chat with SynthID watermark badge.
* **Snippet-to-Song** – Highlight text → “Compose audio” to generate short Lyria 2 background loop for presentations.
* **Dynamic Flashcards** – Auto-create, flip-style cards from selected notes; includes spaced-repetition scheduler.

## 4  Mobile & XR Enhancements

* **Point-and-Ask Lens** – Camera overlay with bounding box; tap to question any on-screen formula/diagram; haptic pulse when answer ready.
* **Offline Blitz Mode** – Lightweight Gemma 3n quiz drill that works in airplane mode; streak counter and confetti animation on perfect round.
* **XR Heads-Up Helper** – For Android XR glasses: top-of-view word translation subtitles; side swipe to bring up step-by-step lab instructions.

## 5  Accessibility & Inclusion

* **Real-Time Translation** – Powered by Gemini; toggles language overlay in chat and on generated videos.
* **Screen-Reader Optimised NAV** – ARIA landmarks, logical heading order, and alt-text auto-generated for media.
* **Colour-Blind Safe Palette** – Ensures charts and progress bars are discernible in deuteranopia and protanopia modes.
* **Font Scale Slider** – In-app dynamic type scaling up to 200%.

## 6  Teacher & Admin Tools

* **Cohort Heatmap Dashboard** – Visual map of class misunderstandings; click cell to view anonymised exemplar answers.
* **Rubric Generator** – Paste assignment brief → AI drafts rubric criteria matrix with Bloom’s verbs.
* **Bulk Comment Bot** – Upload CSV of student IDs & files; returns ZIP of annotated PDFs with inline AI comments.
* **Plagiarism Insight Panel** – Cross-checks AI usage logs vs. submission; flags potential overreliance.

## 7  Gamification & Motivation

* **Streak Flames & Study XP** – Daily streak counter with “flame” animation; XP awarded per mastered concept.
* **Mini-Boss Challenges** – Weekly timed quiz events; leaderboard by course.
* **Achievement Badges** – e.g., “Night-Owl Scholar” for studying after 11 pm, “Teach Me” badge for explaining topic to peer via AI.

## 8  Security & Trust Features

* **SynthID Detector Button** – One-click verify authenticity of any generated media.
* **Privacy Ledger View** – User-readable log of data sent to cloud vs. processed on-device.

---

# Lumina Learn – UI Design Specification (v0.1)

**Author:** UX Team
**Date:** 22 May 2025

---

## 1  Design Principles

1. **Clarity First** – Prioritise legibility and focus on tasks (chat, upload, learn).
2. **Zero‑Friction Interactions** – One‑tap or drag‑and‑drop for primary actions.
3. **Context = Confidence** – Always show citations, AI source badges, and thought‑peek affordances.
4. **Delight with Restraint** – Animations reinforce actions (e.g., streak confetti) but never block workflow.
5. **Accessible by Default** – AA colour contrast, keyboard nav, screen‑reader labels, reduced‑motion option.

---

## 2  Core Screens & Layouts

### 2.1  **Landing / Course Dashboard**

| Area                            | Spec                                                                                                         |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| **Top App Bar**                 | • App logo left  • “Courses” drop‑down  • Notification bell  • Profile avatar                                |
| **Hero Tile (Course Overview)** | Card showing last‑opened course → tap to resume chat. Background gradient in course brand colour.            |
| **Course Grid**                 | Responsive CSS Grid (auto‑fill, min 260 px). Card includes progress ring, course title, instructor initials. |
| **Global FAB**                  | Bottom‑right “+ New Course” (Lottie plus‑animation) → opens modal to enter code.                             |

### 2.2  **Tutor Chat Workspace**

| Zone                           | Description                                                                               |
| ------------------------------ | ----------------------------------------------------------------------------------------- |
| **Left Sidebar (collapsible)** | Tabs: **Library**, **Flashcards**, **Progress**. Slide‑in/out at 240 px width.            |
| **Main Chat Pane**             | 1 column max‑width 720 px; message bubbles 80 % width; assistant messages colour #F1F6FF. |
| **Citation Chips**             | Superscript numbers link to side drawer (opens right). Hover reveals tooltip.             |
| **Message Composer**           | Components: • multiline input • attachment clip • slash‑command helper • Send arrow.      |
| **Quick Follow‑Up Row**        | Horizontal scroll chips under each AI answer (max 3 suggestions).                         |

### 2.3  **Upload Modal**

| State         | UI Elements                                                                                           |
| ------------- | ----------------------------------------------------------------------------------------------------- |
| **Idle**      | Drag‑area with dotted border + icon; “Drop files or click to browse”. Accepts PDF, docx, ppt, images. |
| **Uploading** | File tile list with progress bars ≈ Tailwind `animate-pulse`; cancel x icon.                          |
| **Success**   | Green tick animation, “Indexed – ask away!” link to start question.                                   |
| **Error**     | Red icon if parsing fails; tooltip shows error details; retry button.                                 |

### 2.4  **Slide‑to‑Video Wizard**

1. **Select Deck** page – uses Drive picker component.
2. **Tone & Avatar** – Radio cards (Formal, Energetic, Calm) + AI avatar carousel (photo‑real).
3. **Preview & Edit** – Video player; timeline thumbnails; side panel for script edits.
4. **Export** – Big CTA buttons: *Download MP4* | *Add to Library*.

### 2.5  **Progress Tracker Page**

| Element                 | Details                                                                          |
| ----------------------- | -------------------------------------------------------------------------------- |
| **Mastery Ring**        | Donut chart showing overall % mastered; centre displays XP.                      |
| **Topic Accordion**     | Expandable list; each item has status chip (Mastered/Review) and “Quiz me” icon. |
| **Streak Flame Banner** | Top banner; flame icon + streak days; subtle shimmering glow.                    |

### 2.6  **Teacher Dashboard (Web only)**

| Section              | Component                                                             |
| -------------------- | --------------------------------------------------------------------- |
| **Heatmap**          | 20×N grid; cell tooltip shows misconception & link to sample answer.  |
| **Rubric Generator** | Textarea + “Generate” button; outputs criteria table editable inline. |
| **Bulk Comment Bot** | Upload CSV + template picker; progress bar + ZIP download.            |

---

## 3  Navigation & Information Architecture

* **Global Header** persists across web; contains App logo ↱ Dashboard, Current course badge, Notifications, Profile.
* **Mobile Bottom Nav** – 3 tabs: *Dashboard*, *Tutor*, *Library*. FAB appears conditionally.
* **Breadcrumbs** for Teacher views (Institution › Course › Dashboard).

---

## 4  Visual Style Guide

| Token              | Value                                                    |
| ------------------ | -------------------------------------------------------- |
| **Primary Colour** | `#2563EB` (Tailwind blue‑600)                            |
| **Secondary**      | `#22C55E` (green‑500)                                    |
| **Error**          | `#EF4444` (red‑500)                                      |
| **Grey‑BG**        | `#F7F9FB`                                                |
| **Font Family**    | `Inter`, sans‑serif                                      |
| **Heading Sizes**  | h1 text‑4xl, h2 text‑2xl, h3 text‑xl                     |
| **Border Radius**  | `rounded‑2xl` (16 px) cards; buttons `rounded‑lg` (8 px) |
| **Shadow**         | `shadow‑md` (#000 / 5 %)                                 |

### Component Library

* **Buttons** – Primary (solid), Secondary (outline), Tertiary (ghost) using shadcn/ui classes.
* **Cards** – Soft shadow, padding 5, gap‑4.
* **Chips** – Pill‑shape `rounded‑full` with text‑sm.
* **Modals** – Centre, width 600 px (desktop) / 90 % (mobile).
* **Animations** – Use Framer Motion with 150 ms ease‑out for slide/fade.

---

## 5  States & Feedback

| State              | Pattern                                                                    |
| ------------------ | -------------------------------------------------------------------------- |
| **Loading**        | Skeleton placeholders for cards / chat bubbles (Tailwind `animate-pulse`). |
| **Empty**          | Illustrations from unDraw + concise guidance text.                         |
| **Error Toast**    | Bottom‑left snack; auto‑dismiss 5 s; colour red‑500.                       |
| **Success Toast**  | Green tick; auto‑dismiss 3 s.                                              |
| **Offline Banner** | Yellow bar top of screen; indicates offline and switch to Gemma 3n.        |

---

## 6  Accessibility Details

* **Focus Ring** – 2 px primary blue outline on keyboard focus.
* **Skip‑to‑Content** link appears on tab‑start.
* **ARIA Live Regions** – Announce chat message arrivals & file‑upload completion.
* **Contrast** – Verify text vs. background ≥ 4.5:1 small text, 3:1 large.
* **Motion Toggle** – `prefers-reduced-motion` → disable confetti & flame animations.

---

## 7  Iconography & Illustrations

* **Icon Set** – `lucide-react` for crisp stroke icons.
* **Course Illustrations** – AI‑generated via Imagen 4 (flat colour style) but vetted & down‑scaled.

---

## 8  Prototype Links

* **Figma Prototype v0.1** – *to‑be‑created* (placeholder).
* **Storybook** – Components to be documented in Storybook with accessibility notes.

---

## 9  Open Items

1. Finalise palette variants for dark mode.
2. Decide on avatar visual language (photo‑real vs. stylised).
3. Need sample datasets for progress tracker demo.

## 10  Next Steps

* Wireframes for Tutor Chat & Upload Modal by **7 Jun 2025**.
* Create component tokens in Tailwind config.
* Accessibility audit scheduled for **20 Jun 2025**.

---

*End of UI Design Specification v0.1*


