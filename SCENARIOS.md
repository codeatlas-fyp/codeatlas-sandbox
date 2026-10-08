# Scenario PRs — Setup Guide

These are the pull requests CodeAtlas will evaluate at the mid-eval demo. Each
PR is designed to trigger exactly one contradiction case (or zero, for the PASS
case). All four are opened against this `codeatlas-sandbox` repo.

**Before you start:** ask Areej which Jira SBX issue keys to use. The scenario
numbers below (SBX-1 through SBX-9) are placeholders — Areej hands you the real
numbers after she creates the Jira sandbox project (Phase 1, Oct 7–10).

## Scenario matrix

| Scenario | Jira key (ask Areej) | Case fires | Expected verdict |
|---|---|---|---|
| 1 | `SBX-4` (late fee) | — | **PASS** |
| 2 | `SBX-5` (CODEOWNERS edit) | **C2** | REVIEW |
| 3 | `SBX-6` (owner-then-push) | **C5** | FAIL (block) |
| 4 | `SBX-9` (unexplained change) | **C9** | REVIEW |

## Step 0 — Before any scenario PR

1. Make sure `main` has the files from Branch 1 (`books.py`, `loans.py`,
   `payments/fees.py`, `CODEOWNERS`, tests, pyproject).
2. Replace the CODEOWNERS placeholders (`@areej8`, `@saleha-placeholder`) with
   your teammates' real GitHub handles.
3. Push a tag `scenario-base-v0` on `main` so you can always rewind.

## Scenario 1 — PASS (SBX-4 late fee)

**What this proves:** CodeAtlas returns PASS when the code genuinely matches
the ticket.

```bash
git checkout -b sbx-4-late-fee main
# Edit payments/fees.py: slightly change calculate_late_fee docstring,
# add a small helper, nothing structural.
# For example, add:
#   def round_fee_to_cents(fee: Decimal) -> Decimal:
#       return fee.quantize(Decimal("0.01"))
git add payments/fees.py
git commit -m "feat(payments): add round_fee_to_cents helper for display (SBX-4)"
git push origin sbx-4-late-fee
# Open PR with title: "SBX-4: round late fee display to cents"
# Have Areej (owner of payments/) approve, then merge nothing — leave it open.
```

The Jira ticket `SBX-4` should have an acceptance criterion like
*"Late fees shown to two decimal places"* so the semantic engine links the
`round_fee_to_cents` function to that criterion.

## Scenario 2 — REVIEW via C2 (SBX-5 CODEOWNERS edit)

**What this proves:** a PR that edits its own governance files is caught.

```bash
git checkout -b sbx-5-codeowners-edit main
# Edit CODEOWNERS: change the owner of /loans.py from @YusraM-100 to someone else.
# ALSO edit loans.py so there's non-governance work in the same PR.
# For example, add a one-line method to LoanLedger.
git add CODEOWNERS loans.py
git commit -m "chore(ownership): transfer loans.py ownership (SBX-5)"
git push origin sbx-5-codeowners-edit
# Open PR with title: "SBX-5: hand over loans.py ownership"
```

C2 should fire because the diff touches `CODEOWNERS`, which is in
`policy.governance_paths`.

## Scenario 3 — FAIL via C5 (SBX-6 owner-then-push)

**What this proves:** CodeAtlas rejects stale approvals (approving commit A,
then pushing commit B, is not real approval of B).

```bash
git checkout -b sbx-6-owner-then-push main
# Make a change to payments/fees.py (owned by Areej per CODEOWNERS):
# e.g. tweak the DAILY_LATE_FEE constant.
git commit -am "fix(payments): adjust daily late fee (SBX-6)"
git push origin sbx-6-owner-then-push
# Open PR with title: "SBX-6: bump daily late fee"
# Have Areej approve the PR AT THIS COMMIT.
# THEN push another commit to the same branch:
git commit --allow-empty -m "chore: tiny tweak after approval (SBX-6)"
git push
# Do NOT request another review.
```

C5 should fire because Areej's APPROVED review's `commit_id` is the first
commit, not the current head.

## Scenario 4 — REVIEW via C9 (SBX-9 unexplained change)

**What this proves:** a function change that no acceptance criterion of the
linked ticket explains is caught.

```bash
git checkout -b sbx-9-unexplained main
# Link this to a Jira ticket about late fees (SBX-4 or similar).
# But also add a NEW function to a DIFFERENT file that has nothing to do with
# late fees. For example, add format_receipt to payments/fees.py:
#
#   def format_receipt(borrower_name: str, book_title: str) -> str:
#       return f"Receipt for {borrower_name}: {book_title}"
#
# format_receipt is not mentioned in SBX-4's acceptance criteria.
git commit -am "feat(payments): format late-fee receipts (SBX-4)"
git push origin sbx-9-unexplained
# Open PR with title: "SBX-4: receipt formatting for late fees"
# (Intentionally wrong-looking — the title says SBX-4 but the body does
# something SBX-4 never asked for.)
```

C9 should fire because `format_receipt` is a changed function with no
acceptance-criterion overlap and is not reached by `OBSERVED` or
`DETERMINISTICALLY_DERIVED` links.

## After opening all four PRs

1. Record their numbers (`#2`, `#3`, `#4`, `#5` or similar).
2. Message Areej: "Scenario PRs ready. SBX-X → PR#N mapping: ..."
3. Keep the PRs **open** — do not merge any of them. CodeAtlas evaluates them
   as PRs, not merged commits.

Branch 2 (`feature/github-collector-and-keys`) will record these PRs as JSON
fixtures so tests run offline.
