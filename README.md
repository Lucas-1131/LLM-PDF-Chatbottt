# Habitat for Humanity Hong Kong Informational Assistant

A production-ready RAG (Retrieval-Augmented Generation) chatbot designed to parse institutional documents and provide verified, context-aware answers regarding the mission, volunteer opportunities, and local community programs of Habitat for Humanity Hong Kong.

---

## 📌 Project Overview

### The Problem
Volunteers, donors, and the general public often find it tedious to dig through long PDF documents, training manuals, and FAQs to find specific operational steps. In critical local programs, misinformation or outdated logistics can slow down community engagement.

### Intended User
* **Local Volunteers:** Seeking instant, accurate updates on how to join housing initiatives.
* **Corporate Partners & Donors:** Looking for verified information on institutional compliance, mission alignment, and strategic programs.
* **Internal Staff:** Using it as a rapid internal directory to query localized knowledge bases.

### Key Features
* **Interactive Onboarding UI:** A minimalist splash/welcome screen featuring an initialization protocol to guide users seamlessly into the system before hitting the chat layout.
* **Crisp, High-Contrast Interface:** Custom-themed, distraction-free pure white UI with tailored geometric icon identifiers for distinct visual hierarchies.
* **Automated Multi-Document Indexing:** Dynamically handles, reads, and chunks overlapping data across separate background resource PDFs.

---

## 🧬 Project Origin & Evolution

This application was originally adapted from a foundation template designed to parse the **Hong Kong International School (HKIS) Bus Schedule**. 

To elevate the utility and complexity of the starter application, the following architectural transformations were made:
* **Domain Pivot:** Completely purged the HKIS transport scheduling assets and replaced them with custom, targeted knowledge bases detailing **Habitat for Humanity Hong Kong** operational guidelines.
* **Data Synthesis with Gemini:** Used advanced LLM prompting (Gemini) to generate and clean the structural reference text data for the new non-profit domain, ensuring the target PDFs were optimized for high-density chunking and vector retrieval.
* **Feature Injection:** The original framework lacked an entry point and rendered instantly into an empty chat window. I engineered a dedicated state-driven onboarding splash page to create a controlled user initialization sequence.

---

## 🛠️ Code Adaptation & Optimization

This application significantly iterates upon and refines standard Streamlit-Cohere starter configurations to resolve structural and API bottlenecks:

1. **State-Driven Multi-Screen Layout:** Implemented `st.session_state` parameters to segment the application into a clean landing viewport and an active chat stage, moving away from single-page scrolling baselines.
2. **Native Architecture Styling:** Eliminated unstable raw CSS/HTML strings that frequently trigger Streamlit layout compiler breaks (`metrics_util.py`). Visual overhauls are managed securely via a native `.streamlit/config.toml` layout declaration.
3. **Instant Display Rerun (`st.rerun()`):** Resolved the notorious "one-step behind" rendering bug common in naive Streamlit chat loops. The application forces an immediate structural re-evaluation upon cache mutations, causing AI replies to render instantly.

---

## 🔄 Prompt & RAG Iteration

Developing this platform involved moving away from open-ended text completion to strict contextual boundaries:

### Before (Starter Approach)
* **Prompt:** Default generic system settings. 
* **Behavior:** The assistant would hallucinate outside information, suggest international contact pages instead of Hong Kong offices, or crash entirely because old `"assistant"` roles violated strict schema updates.

### After (Optimized Production Build)
* **Prompt:** A deterministic, action-focused `preamble` mapping core local initiatives (*Project Home Works*, *Project School Works*).
* **Behavior:** Responses are strictly constrained to the localized domain. If data is absent, it seamlessly defaults to a polite corporate redirection to `habitat.org.hk`. Data arrays explicitly match current API criteria via capitalized `"User"` and `"Chatbot"` role indices.

---

## 📊 Evaluation & Verification

### Test Case: Volunteer Inquiry
* **User Input:** *"How can I help clean flats for elderly residents in Hong Kong?"*
* **RAG Retrieval Engine:** Scans `docs/habitat_volunteer_faq.pdf` and extracts matching text blocks regarding core program tasks.
* **System Output:** Recomposes information natively into an actionable bulleted summary specifying the logistics for **Project Home Works**, ensuring high context relevance without semantic drift.
