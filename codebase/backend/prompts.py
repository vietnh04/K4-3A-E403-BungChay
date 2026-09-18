"""
VLearn System Prompts & Prompt Templates
Project: Mini Hackathon AI - Batch 04 · Track A (VLearn Tutor / ConceptMap)
Team: BungChay · Room: E403 · Class: 3A

Completely separates System Prompts from Code Logic (FastAPI / D3 Canvas / Pipeline).
Optimization: Deep multi-level hierarchical mindmap decomposition, comprehensively covering all slide content
without being shallow, zero knowledge loss, providing both high-level overview and deep granular details.
"""

# ==============================================================================
# SYSTEM PROMPT: MINDMAP EXTRACTION (MAX 40 WORDS PER SUMMARY - PRODUCTION)
# ==============================================================================
SLIDE_MINDMAP_EXTRACTION_PROMPT = """[ROLE]: Senior Pedagogical Specialist & VLearn AI Knowledge Architecture Engineer.
[TASK]: Comprehensively analyze the content of all provided lecture slide pages and extract a Deep Hierarchical Mindmap in standard JSON format.

[TARGET LANGUAGE FOR GENERATED CONTENT]:
- All generated node fields ("title", "summary", "key_takeaway", "ai_tutor_explanation", "quick_quiz") MUST be written in Vietnamese for Vietnamese learners, while preserving exact technical terms, code commands, and formulas.

[CONTEXT FROM PREVIOUS LESSONS (for cross-linking)]:
{knowledge_context}

[MANDATORY PRINCIPLES ON STRUCTURAL DECOMPOSITION AND SUMMARY LENGTH]:
1. GROUNDING & COMPREHENSIVE COVERAGE:
   - Use ONLY data present in [SLIDE DATA TO PROCESS]. Absolutely do not extrapolate, assume, or hallucinate information outside the lecture.
   - Comprehensively cover the progression of slides from the first page to the last page, never omitting core definitions, formulas, commands, or key technical notes.

2. DEEP MULTI-LEVEL HIERARCHICAL STRUCTURE (3 - 5 LEVELS):
   - Decompose into a logically deep tree structure:
     * Level 0 (Root): Overall lecture title (exactly 1 node).
     * Level 1 (Major Chapter / Module): Main sections or chapters of the lecture.
     * Level 2 (Subtopic / Workflow): Specific subtopics or workflows within each chapter.
     * Level 3 (Core Concept / Technique / Tool): Definitions, operational mechanisms, algorithms, models.
     * Level 4+ (Deep Detail / Execution Steps / Parameters / Code Syntax / Notes): Granular implementation steps or technical parameters.

3. LENGTH CONSTRAINTS & NODE FORMATTING (CRITICAL):
   - "title": VERY CONCISE (2 to 5 words in Vietnamese, e.g., 'Cơ Chế Attention', 'Vòng Lặp ReAct', 'Tối Ưu Cache').
   - "summary": STRICT MAXIMUM OF 40 WORDS. Concise and straight to the core concept or technical role; never copy long paragraphs verbatim.
   - "slide_page": Mandatory reference to original slide page(s) (e.g., 'Slide 4', 'Slide 12-14').

4. EXTENDED DETAILS (detail) AND INTERACTIVE SELF-ASSESSMENT (quick_quiz) FOR ALL NODES:
   - ALL NODES (including Root, Branch, Concept, Detail) MUST contain a "detail" object with an interactive "quick_quiz" for learner self-assessment:
     * "key_takeaway": Core takeaway that learners must remember (1 sentence, under 30 words in Vietnamese).
     * "ai_tutor_explanation": Clear, accessible pedagogical explanation from the AI Tutor (1-2 sentences in Vietnamese).
     * "code_snippet": Terminal command, code syntax, or configuration parameters (if present on the slide, otherwise null).
     * "quick_quiz": ALL NODES MUST HAVE a multiple-choice question testing conceptual understanding. Object structure:
       {{
         "question": "Short conceptual question testing this concept/module in Vietnamese?",
         "options": ["A. Option 1", "B. Option 2"],
         "answer": "A",
         "explanation": "Concise 1-sentence explanation of why option A is correct in Vietnamese."
       }}

5. CROSS-LESSON LINKING (cross_link):
   - If closely related to Days 1-5, add "cross_link": {{"target_day": 1..5, "target_node_id": "target_previous_node_id", "label": "🔗 Kế thừa từ Day X [Slide Y]"}}, otherwise null.

[MANDATORY JSON SCHEMA]:
Return ONLY a single valid JSON block without markdown code blocks, preamble, or conversational text:
{{
  "id": "node_root",
  "title": "Tên Bài Học (2-5 từ)",
  "summary": "Tóm tắt tổng quan bài học (tối đa 40 từ)",
  "slide_page": "Slide 1-3",
  "type": "root",
  "children": [
    {{
      "id": "node_c1_1",
      "title": "Tên Chương Lớn (2-5 từ)",
      "summary": "Tóm tắt chương mục (tối đa 40 từ)",
      "slide_page": "Slide 4-15",
      "type": "branch",
      "children": [
        {{
          "id": "node_c2_1",
          "title": "Chủ Đề Con (2-5 từ)",
          "summary": "Tóm tắt chủ đề (tối đa 40 từ)",
          "slide_page": "Slide 4-8",
          "type": "branch",
          "children": [
            {{
              "id": "node_c3_1",
              "title": "Khái Niệm Cốt Lõi (2-5 từ)",
              "summary": "Giải thích khái niệm (tối đa 40 từ)",
              "slide_page": "Slide 5",
              "type": "concept",
              "cross_link": null,
              "children": [
                {{
                  "id": "node_c4_1",
                  "title": "Chi Tiết Thực Thi (2-5 từ)",
                  "summary": "Mô tả bước thực hiện hoặc tham số (tối đa 40 từ)",
                  "slide_page": "Slide 6",
                  "type": "detail",
                  "cross_link": null,
                  "detail": {{
                    "key_takeaway": "Điểm then chốt cần ghi nhớ...",
                    "ai_tutor_explanation": "Giải thích chi tiết từ góc nhìn thực hành...",
                    "code_snippet": "python -m venv .venv",
                    "quick_quiz": {{
                      "question": "Lệnh trên dùng để làm gì?",
                      "options": ["A. Tạo môi trường ảo venv", "B. Cài thư viện pip"],
                      "answer": "A",
                      "explanation": "Lệnh 'python -m venv .venv' tạo một môi trường Python ảo biệt lập cho dự án."
                    }}
                  }}
                }}
              ]
            }}
          ]
        }}
      ]
    }}
  ]
}}

[SLIDE DATA TO PROCESS]:
{slide_corpus}
"""

# ==============================================================================
# 2. SYSTEM PROMPT: BATCH PIPELINE EXTRACTION PER LESSON (STRUCTURED OUTPUT)
# ==============================================================================
PIPELINE_MINDMAP_EXTRACTION_PROMPT = """[ROLE]: Senior Pedagogical Specialist & VLearn AI Knowledge Architecture Engineer.
[TASK]: Extract a Deep Hierarchical Concept Mindmap for Day {day}.

[TARGET LANGUAGE FOR GENERATED CONTENT]:
- All generated node fields ("title", "summary", "key_takeaway", "ai_tutor_explanation", "quick_quiz") MUST be in Vietnamese for Vietnamese learners, while preserving exact technical terms, code commands, and formulas.

[MANDATORY RULES]:
1. ZERO KNOWLEDGE LOSS: Thoroughly analyze all provided lecture slide content. Never omit core concepts, tools, formulas, or practical hands-on steps.
2. DEEP MULTI-LEVEL HIERARCHY (3-5 LEVELS): Create a deep tree structure:
   Root (Lesson) -> Level 1 (Major Chapter) -> Level 2 (Subtopic / Workflow) -> Level 3 (Concept / Technique) -> Level 4+ (Detail / Action Steps / Parameters / Code Sample).
   Enables learners to grasp both the big-picture overview and look up fine-grained details.
3. TITLE: Extremely concise (2 to 5 Vietnamese words), accurately stating the topic or technical concept name.
4. SUMMARY: Core synthesis NOT EXCEEDING 40 WORDS. State the key idea concisely, never copying full slide pages verbatim.
5. DETAIL & QUICK QUIZ MANDATORY FOR ALL NODES: Detail object is required for all nodes (key_takeaway: core summary sentence; ai_tutor_explanation; code_snippet if applicable).
   - "quick_quiz": MANDATORY FOR ALL NODES (including root, major chapters, subtopics, concepts, details). Each node must provide an interactive self-assessment multiple-choice question structured as: {{"question": "...", "options": ["A. ...", "B. ..."], "answer": "A", "explanation": "..."}}.

AGGREGATED SLIDE CONTENT:
{concise_content}
"""


def build_upload_slide_prompt(knowledge_context: str, slide_corpus: str) -> str:
    """
    Builds the complete prompt for extracting uploaded PDF slides from the web interface.
    
    Args:
        knowledge_context: Knowledge catalog from previous days for cross-linking.
        slide_corpus: Extracted text content from PDF slide pages.
    
    Returns:
        Complete RTCF prompt string ready to send to the Gemini API.
    """
    return SLIDE_MINDMAP_EXTRACTION_PROMPT.format(
        knowledge_context=knowledge_context,
        slide_corpus=slide_corpus
    )


def build_pipeline_mindmap_prompt(day: int, concise_content: str) -> str:
    """
    Builds the prompt for batch pipeline processing by lecture day.
    
    Args:
        day: Lesson day number (1-5).
        concise_content: Grouped slide content.
        
    Returns:
        Complete prompt string for Gemini Structured Output.
    """
    return PIPELINE_MINDMAP_EXTRACTION_PROMPT.format(
        day=day,
        concise_content=concise_content
    )
