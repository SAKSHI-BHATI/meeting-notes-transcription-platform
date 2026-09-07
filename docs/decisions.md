# Key decisions

- **Modular monolith:** avoids distributed-systems overhead while keeping clean seams.
- **Mock/seeded summaries:** the product works without an API key; a provider interface can later call an LLM asynchronously.
- **Binary search synchronization:** player updates find the current segment in O(log n), not a linear scan.
- **Transcript parser strategy:** TXT, VTT, and JSON normalize to one segment contract.
