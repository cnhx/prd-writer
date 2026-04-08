# Codex Sample Invocation

Use the PRD agent in this Codex workspace to create a product requirements document from `examples/sample-input-brief.md`.

Execution requirements:
- read the brief and any local project files that affect product scope
- ask one key question at a time when context is missing
- write the PRD draft to a markdown file instead of returning the full draft in chat
- do not force output language; follow the user's preference
- keep all variables, states, events, and config fields in readable English identifiers
- keep art and design requirements in a dedicated section
- mark unknown math, compliance, and market facts explicitly
- run the optional polish pass only if enabled in config
- save the final PRD and return the output contract with publish status
