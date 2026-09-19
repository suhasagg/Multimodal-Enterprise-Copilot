# Security

Production requirements:
- OIDC / Entra ID / workload identity
- tenant authorization independent of prompts
- row-level security for knowledge
- signed/short-lived object URLs
- malware scanning
- DLP / PII classification
- MIME sniffing, not filename trust
- decompression-bomb limits
- prompt-injection defenses for documents/images
- least-privilege MCP credentials
- human approval for high-impact tools
- immutable action audit
- egress allowlists
- secrets manager
- retention/deletion policy for uploaded media

Retrieved content is untrusted data. It must never be allowed to redefine system policy.
