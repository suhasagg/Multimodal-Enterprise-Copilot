# Multimodal design

Supported reference flows:
- text -> RAG -> answer
- image + text -> vision understanding -> RAG -> answer
- PDF/text document -> parsing -> chunks -> embeddings -> RAG
- audio -> transcription -> copilot context
- Java image endpoint -> Spring AI multimodal ChatClient

For production:
- preserve page/region/timecode provenance
- extract tables separately
- use OCR only when native text is unavailable
- thumbnail/resize very large images
- virus-scan uploads
- classify sensitive media
- keep raw media outside prompts when unnecessary
- attach signed object-store references rather than huge inline payloads where supported
