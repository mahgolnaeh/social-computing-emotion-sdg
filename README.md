# Social Computing Project – Emotion-Aware SDG Response System

This project analyzes short social media posts to detect SDG relevance and emotional tone, then generates supportive responses aligned with both.  
It is modular, LLM-powered, and designed for human-centered, empathetic automation.

## 🔧 Pipeline Overview
1. Load trends (real or synthetic)
2. Classify with UN SDGs
3. Detect emotion (from 9 classes)
4. Generate supportive response (template or LLM-based)
5. Output structured JSON ready for dashboard display

> Example:  
> **Trend:** "privacy concerns with AI"  
> → **SDG:** Reduced Inequality  
> → **Emotion:** Frustration  
> → **Response:** Supportive message + SDG link

All modules are fully validated with Pydantic and support either local or API-based LLMs.
