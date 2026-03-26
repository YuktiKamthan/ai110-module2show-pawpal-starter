# PawPal+ Project Reflection

---

## 1. System Design

**a. Initial design**

Three core actions the user can perform:

1. **Add a pet** — Enter pet info (name, species, age). Everything in the app is tied to a pet.
2. **Add care tasks** — Create tasks like feeding, walks, or medication, each with a duration and priority.
3. **Generate a daily schedule** — The system organizes tasks by priority and available time, and explains what fits and what doesn't.

The system is built around four classes:

- **Owner** — Stores the owner's name and available time per day. Manages a list of pets.
- **Pet** — Stores pet details and holds a list of care tasks.
- **Task** — Represents one care activity with name, duration, priority, time of day, frequency, and due date.
- **Scheduler** — The brain. Takes a pet and owner, sorts tasks by priority, fits them within available time, and warns about conflicts.

Relationships:
- Owner → owns → Pet(s)
- Pet → has → Tasks
- Scheduler → uses → Pet + Owner to build the daily plan

**b. Design changes**

One change was made after reviewing the skeleton:

- **Original:** `Scheduler(pet, available_minutes)` — passed time as a plain number
- **Changed to:** `Scheduler(pet, owner)` — passes the full Owner object
- **Why:** The Scheduler can now always read `owner.available_minutes` directly. Passing just a number disconnected the Scheduler from the Owner and could cause inconsistencies if the owner's time was updated later.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers three constraints:

- **Priority (high / medium / low)** — Most important. High-priority tasks always get scheduled first. A missed medication matters more than a missed playtime.
- **Available time** — Acts as a hard cap. Tasks are added greedily until time runs out.
- **Time of day (morning / afternoon / evening)** — A soft preference used to sort the final plan so it flows naturally through the day.
- **Frequency (daily / weekly)** — Weekly tasks are hidden on non-weekly days to avoid clutter.

**b. Tradeoffs**

The scheduler uses broad time slots (morning, afternoon, evening) instead of exact start and end times.

- **What this means:** It can warn that a slot is overloaded in total minutes, but it can't detect that two tasks literally overlap at 8:00 AM and 8:15 AM.
- **Why it's okay:** Pet owners think in routines, not timestamps. A morning walk and morning feeding just need to both happen in the morning — exact times don't matter.
- **Benefit:** Much simpler to build, easier to understand, and still catches the most common problem — too many tasks in one part of the day.

---

## 3. AI Collaboration

**a. How I used AI**

AI was involved at every phase:

- **Phase 1** — Brainstormed the four-class architecture and generated the UML diagram from a plain-English description.
- **Phase 2** — Scaffolded class skeletons and suggested using Python dataclasses for Task and Pet to reduce boilerplate.
- **Phase 4** — Helped design conflict detection and suggested using `timedelta` for recurring task scheduling.
- **Phase 5** — Drafted initial test functions, which were then reviewed and extended with edge cases.

The most helpful prompts were **specific and file-anchored** — for example:
> "Based on my skeletons in pawpal_system.py, how should the Scheduler retrieve all tasks from the Owner's pets?"

Vague prompts like "help me with scheduling" produced generic, unusable responses.

**b. One moment I didn't accept the AI suggestion**

For `filter_by_frequency`, the AI suggested:
```python
allowed = {"daily"} | ({"weekly"} if is_weekly_day else set())
return [t for t in tasks if t.frequency in allowed]
```

This is more Pythonic but harder to read if you don't know set operations. The original version was kept:
```python
return [t for t in tasks if t.frequency == "daily" or (t.frequency == "weekly" and is_weekly_day)]
```

Both versions passed all tests — so the decision came down to readability over cleverness. The readable version won.

---

## 4. Testing and Verification

**a. What I tested**

14 tests across two categories:

**Happy paths:**
- Task completion changes status to Done
- Adding a task increases the pet's task count
- Daily task reschedules for tomorrow after completion
- Weekly task reschedules 7 days out after completion
- Completing a task auto-adds the next occurrence
- Tasks sort correctly morning → afternoon → evening
- Pending task filter returns only incomplete tasks
- Conflict detection fires when a slot is overloaded
- Weekly tasks excluded on non-weekly days

**Edge cases:**
- Pet with no tasks returns an empty schedule (no crash)
- Task longer than available time is skipped gracefully
- Filter returns empty when all tasks are completed
- Completing a non-existent task name doesn't crash
- Owner with no pets returns an empty task list

**b. Confidence level: ⭐⭐⭐⭐ (4/5)**

The core pipeline is well covered. The missing star is for exact-timestamp conflict detection — two tasks in the same broad slot are warned about collectively, but minute-by-minute overlap isn't calculated. That's a known tradeoff, not a bug.

Next tests I'd add:
- One combined schedule across multiple pets
- Tasks with identical names on the same pet
- Scheduling when available time is exactly zero

---

## 5. Reflection

**a. What went well**

The **CLI-first workflow** was the best decision made early on. All logic was built and verified in `pawpal_system.py` and `main.py` before any UI work began. This meant connecting the Streamlit UI was just wiring — no debugging of core logic in the browser. The test suite also caught a real gap early: `mark_complete()` originally returned nothing, but recurring tasks required it to return the next Task object. The tests made that visible before it became a bug in the UI.

**b. What I would improve**

Supporting **multiple pets in one schedule view**. Right now the Scheduler works one pet at a time. A real owner with two dogs and a cat wants to see the full day across all pets in one plan. This would mean:
- Scheduler accepts an Owner instead of a single Pet
- Tasks are grouped by pet
- Time budget is shared across all animals

**c. Key takeaway**

AI is most useful when **you already have a clear design**. Vague prompts produce generic code. Specific prompts referencing actual files and constraints produce precise, usable output.

The role of the human isn't to write every line — it's to define the boundaries, make the architectural decisions, and verify the results. That's what "lead architect" actually means when working with AI.
