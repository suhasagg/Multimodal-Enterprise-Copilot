# Architecture

## Multimodal intake
Media processing is separated from orchestration. Images are interpreted by a multimodal model; documents are parsed/chunked/embedded; audio is transcribed through an isolated adapter.

## Grounded enterprise answers
Enterprise facts come from tenant-filtered retrieval. The answer agent receives explicit evidence and citation identifiers.

## Agent/action boundary
Read-only questions should not trigger actions. Actions go through MCP tools with deterministic server-side policy. High-impact operations must not rely on model self-approval.

## Polyglot design
Python owns agent orchestration, RAG and media pipelines. Java/Spring AI demonstrates enterprise integration, multimodal model access and governed MCP actions.

## Scale
Production ingestion should be asynchronous through a queue, store originals in object storage, run malware/DLP scanning, and independently scale parsing, embedding and serving workers.
