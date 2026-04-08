# Security Policy

## Supported scope

This repository is a prompt-and-workflow toolkit. It does not run a hosted service.

Security issues here are usually one of these:
- accidental exposure of secrets, tokens, or private paths
- examples or docs that encourage unsafe behavior
- prompts or workflows that can cause dangerous data leakage
- release files that expose internal or proprietary material

## What to report

Please report issues such as:
- committed secrets or credentials
- private infrastructure paths or internal company references left in examples
- instructions that encourage unsafe external actions without review
- workflows that silently turn optional safeguards into mandatory side effects
- misleading guidance that could cause unintended data disclosure

## What is probably not a security issue

The following are usually documentation or product issues, not security vulnerabilities:
- disagreements about prompt style
- model preference debates
- non-security portability bugs
- missing optional integrations

## Reporting process

Please report responsibly and avoid public disclosure of sensitive details until the issue is fixed.

If you cannot contact the maintainer privately, open a minimal public issue that states:
- a security concern exists
- maintainers should make contact
- sensitive details are intentionally omitted

## Handling policy

When a real security issue is confirmed, the preferred response is:
1. remove exposed sensitive material
2. rotate affected secrets if relevant
3. patch the workflow or docs
4. publish a concise remediation note

## Safe contribution reminders

Before opening a PR, check that you did not include:
- secrets or tokens
- private vault paths tied to a real environment
- internal documents copied into examples
- prompts that assume unsafe write or publish actions by default
