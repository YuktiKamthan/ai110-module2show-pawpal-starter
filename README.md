# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Smarter Scheduling

PawPal+ goes beyond a simple task list with four algorithmic features:

- **Priority-based scheduling** — Tasks are ranked high → medium → low. High-priority tasks always get time in the schedule first.
- **Time-of-day sorting** — The final schedule is ordered morning → afternoon → evening so it reads like a natural day.
- **Recurring task automation** — Daily tasks reschedule for the next day when marked complete. Weekly tasks (grooming, vet visits) reschedule 7 days out and are hidden on non-weekly days to avoid clutter.
- **Conflict detection** — The scheduler warns if total task time exceeds the owner's available time, or if any single time slot (morning/afternoon/evening) is overloaded beyond 60 minutes — and names the specific tasks causing the clash.

## Testing PawPal+

Run the full test suite with:

```bash
python -m pytest
```

The 14 tests cover:

- **Happy paths** — task completion, adding pets/tasks, sorting, filtering, recurring scheduling, conflict detection
- **Edge cases** — empty pet (no tasks), task too long to fit, all tasks already completed, completing a non-existent task, owner with no pets

**Confidence level: ⭐⭐⭐⭐ (4/5)**
The core scheduling logic is well-covered. The missing star reflects that time slots are broad (morning/afternoon/evening) rather than exact timestamps, so minute-level overlaps are not tested. That's a known tradeoff, not a bug.

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
