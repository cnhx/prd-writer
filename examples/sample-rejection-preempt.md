# Rejection Letter Pre-empt — Example (fictional)

> ⚠️ All stakeholders, quotes, and mitigations below are **fictional** and for format
> illustration only. Real rejection letters reference real stakeholders and real
> evidence inside your PRD. Do not copy these numbers or claims.

Context for this example: a team is scoping "Team Inbox Digest" — a weekly email
that summarizes the team's shared inbox into an action list. This is a generic SaaS
feature, not a regulated or game product.

---

## Top 5 predicted rejection reasons

1. **Engineering lead**: "Effort is underestimated. Summarization quality work alone
   takes 6+ weeks; you budgeted 4."
   - Mitigation: Phase 1 uses a rule-based summarizer (keyword clustering + sender
     weighting), not an LLM. LLM path is Phase 2, conditional on Phase 1 retention
     data. See `docs/prd/team-inbox-digest.md` §9 Technical Considerations.
   - Residual risk: rule-based quality may be too low to move `open_rate` —
     `to_be_confirmed` by 2026-05-01 with a 2-team pilot.

2. **Leadership (VP Product)**: "This overlaps with the Notifications Hub work
   already in-flight. Do we need both?"
   - Mitigation: Explicit section in Non-Goals states this is **scoped to
     shared-mailbox triage only**, not personal notifications; Notifications Hub
     remains the per-user surface. Conflict matrix in §2 Project Positioning.
   - Residual risk: `known_gap` — long-term consolidation question remains open;
     decision deferred to Q3 roadmap review.

3. **Compliance**: "A digest email summarizing customer messages may expose PII to
   recipients outside the original authorized readers."
   - Mitigation: §7 Compliance & Risk states digest recipients = existing
     authorized mailbox members only (reuses `mailbox_acl`). Digest body never
     includes full customer PII; only counts + subject keywords.
   - Residual risk: Subject-line leakage. Legal to confirm subject-line inclusion
     is acceptable — `to_be_confirmed` by legal-owner@example.com by 2026-04-22.

4. **Finance**: "What is the cost per digest and the ROI?"
   - Mitigation: §10 KPI & Success Metrics states target: `open_rate >= 35%`
     driving `weekly_active_teams_with_digest` up by 500 teams within 60 days.
     Cost is infrastructure-only at Phase 1 (no LLM billing). Break-even at
     200 teams.
   - Residual risk: Willingness to pay for Phase 2 LLM upgrade is unmodeled —
     explicitly deferred to post-Phase 1 memo.

5. **GTM / CS lead**: "Our enterprise customers will ask to customize the digest.
   What's our answer?"
   - Mitigation: §4 Product Flow explicitly restricts Phase 1 customization to
     **frequency only** (daily/weekly/off). Template customization is Phase 2,
     `conditional_on_phase_1_learnings`.
   - Residual risk: `known_gap` — top 3 enterprise accounts may escalate; CS to
     pre-brief them by 2026-04-25.

---

## Notes on using this example

- Each rejection quote is specific enough that the stakeholder could actually say it.
  Vague quotes ("may have issues") produce vague mitigations.
- Every Mitigation points to a **PRD section**, **evidence**, or **scope change** —
  never "we will monitor." Monitoring is not mitigation.
- Residual risks are either `to_be_confirmed` (with owner + date) or `known_gap`
  (accepted, with context). No silent risks.
- Five is the default. Four is fine if a stakeholder genuinely does not apply. More
  than seven usually means the PRD scope is too broad — shrink it first.
