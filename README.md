# PawPal+ (Module 2 Project)

**PawPal+** is a smart pet care management system built with Python and Streamlit. It helps busy pet owners stay consistent with daily routines by tracking tasks, generating prioritized schedules, and automatically handling recurring care.

---

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

---

## Features

- **Owner and pet profiles** — Set up an owner with available time per day, then register one or more pets.
- **Task management** — Add care tasks with name, duration, priority (high/medium/low), time of day (morning/afternoon/evening), and frequency (daily/weekly).
- **Priority-based scheduling** — High-priority tasks are always scheduled first. If time runs out, lower-priority tasks are gracefully skipped with a warning.
- **Time-of-day sorting** — The generated schedule is ordered morning → afternoon → evening so it reads like a natural day, regardless of the order tasks were added.
- **Recurring task automation** — Completing a daily task auto-schedules the next occurrence for tomorrow. Weekly tasks (grooming, vet visits) reschedule 7 days out and are hidden on non-weekly days to avoid clutter.
- **Conflict detection** — The scheduler warns if total task time exceeds the owner's available time, or if any single time slot is overloaded beyond 60 minutes — and names the specific tasks causing the clash.
- **Task filtering** — View only pending or completed tasks across all pets.
- **Mark complete from UI** — Mark any task done directly in the browser; the next occurrence is auto-added instantly.

---

## System Architecture

The app is built around four OOP classes in `pawpal_system.py`:

| Class | Responsibility |
|-------|---------------|
| `Task` | Stores a single care activity with duration, priority, frequency, and due date |
| `Pet` | Holds a pet's details and its list of tasks |
| `Owner` | Manages multiple pets and provides filtered views of all tasks |
| `Scheduler` | Generates a prioritized, time-sorted daily plan with conflict detection |

See `uml_final.png` for the complete class diagram.

---

## Smarter Scheduling

PawPal+ goes beyond a simple task list with four algorithmic features:

- **Priority-based scheduling** — Tasks are ranked high → medium → low. High-priority tasks always get time in the schedule first.
- **Time-of-day sorting** — The final schedule is ordered morning → afternoon → evening so it reads like a natural day.
- **Recurring task automation** — Daily tasks reschedule for the next day when marked complete. Weekly tasks reschedule 7 days out and are hidden on non-weekly days to avoid clutter.
- **Conflict detection** — Warns if total task time exceeds available time, or if any time slot is overloaded — and names the specific tasks causing the clash.

---

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

---

## 📸 Demo

<a href="screenshots/pawpal Ui scrrenshot .png" target="_blank"><img src='screenshots/pawpal Ui scrrenshot .png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

<a href="screenshots/pawpal Ui screenshot 2 .png" target="_blank"><img src='screenshots/pawpal Ui screenshot 2 .png' title='PawPal App Schedule View' width='' alt='PawPal App Schedule View' class='center-block' /></a>

---

## Author

**Yukti Kamthan**
[LinkedIn](https://www.linkedin.com/in/yuktikamthan)

---

## Getting Started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the app

```bash
streamlit run app.py
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
