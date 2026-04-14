# Feature Trinity — Format Reference

> ⚠️ Fictional example. Use for format only; do not copy the numbers.

Every user-facing functional requirement in a PRD's §5 must have three elements:
**User job**, **Mechanism**, **Success signal**. This is the PRD analogue of
EvoSkills paper-writing's "every method module needs design + motivation + advantage."

Missing any element → `trinity_incomplete`. Pure infrastructure requirements →
`trinity_na` with a one-line reason.

---

## ✅ Good — all three elements present

### Feature: `daily_summary_email`

- **User job** — When a shared-mailbox team member starts their Monday, they want
  to know what customer conversations landed over the weekend so they can plan
  their morning triage.
- **Mechanism** — At `0800` Monday local time, aggregate the past 48 hours of
  unread threads in `mailbox_id`, cluster by `sender_domain` and `thread_topic`,
  render into an HTML email scoped to that user's `mailbox_acl` membership.
- **Success signal** — `open_rate` on the Monday digest `>= 30%` within 30 days
  of rollout, measured weekly.

Notes:
- Project-level KPI might be `weekly_active_teams_with_digest`. `open_rate` is the
  **feature-level** signal — it tests whether the digest itself is useful, not
  whether adoption grew.
- Mechanism names `mailbox_acl` (reused identifier) — English per language policy.

---

## ❌ Bad — `trinity_incomplete`

### Feature: `smart_notifications`

- **User job** — Users want better notifications.  *(too vague — who, what
  situation, what outcome?)*
- **Mechanism** — The system intelligently prioritizes notifications.  *(no input,
  no observable behavior, "intelligently" hides the design)*
- **Success signal** — *(missing)*

→ Mark `trinity_incomplete`. Do not proceed to §9 Technical Considerations or §10
KPI until all three cells are filled. Rewriting the User job alone ("when a user
has >50 unread notifications, they want to surface the 3 that require action")
usually forces the Mechanism and Success signal to emerge.

---

## ✅ Valid — `trinity_na` with reason

### Requirement: `migrate_auth_service_from_v1_to_v2`

- **trinity_na** — Internal service migration. No user-visible behavior change
  intended; validated by traffic mirror showing `error_rate_delta == 0` and
  `p95_latency_delta < 5ms` for 7 days.

Notes:
- `trinity_na` is OK here because no end user (human or external API consumer)
  sees a difference. The migration owner's test criteria replace the Trinity.
- If downstream API clients *would* see a breaking change, this is user-facing
  and Trinity is required, not `trinity_na`.

---

## Anti-patterns

- **Writing Mechanism as feature name**: "The system provides a smart inbox" is a
  name, not a mechanism. Mechanism describes input → processing → output.
- **Using project KPI as Success signal**: project KPI aggregates many features.
  The feature-level signal must be narrow enough to attribute to *this* feature.
- **`trinity_na` for time-pressure**: if you are tempted to mark it `trinity_na`
  because "we don't have time to write the User job," the feature is
  `trinity_incomplete`, not `trinity_na`. Push back on scope, not on the spec.

---

## Why this exists

Without Trinity, PRD features commonly fail review for one of:
- "Why does this exist?" (no User job)
- "What exactly is being built?" (no Mechanism)
- "How do we know it worked?" (no Success signal)

All three are answerable in one sentence each. If any takes a paragraph, the
feature itself is probably too big — split it.
