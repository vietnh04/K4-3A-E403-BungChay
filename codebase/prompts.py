"""
VLearn Prompts Module Entrypoint
Tiện ích import trực tiếp các system prompts và builder functions.
"""

from backend.prompts import (
    SLIDE_MINDMAP_EXTRACTION_PROMPT,
    PIPELINE_MINDMAP_EXTRACTION_PROMPT,
    build_upload_slide_prompt,
    build_pipeline_mindmap_prompt,
)

__all__ = [
    "SLIDE_MINDMAP_EXTRACTION_PROMPT",
    "PIPELINE_MINDMAP_EXTRACTION_PROMPT",
    "build_upload_slide_prompt",
    "build_pipeline_mindmap_prompt",
]
