"""
VLearn Prompts Module Entrypoint
Convenience entrypoint directly importing system prompts and builder functions.
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

