from dataclasses import dataclass, field
from typing import List
import datetime

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}
TIME_ORDER = {"morning": 0, "afternoon": 1, "evening": 2}
FREQUENCY_DAYS = {"daily": 1, "weekly": 7}


@dataclass
class Task:
    name: str
    duration: int           # in minutes
    priority: str           # "high", "medium", or "low"
    preferred_time: str     # "morning", "afternoon", or "evening"
    frequency: str = "daily"    # "daily" or "weekly"
    completed: bool = False
    due_date: datetime.date = field(default_factory=datetime.date.today)

    def mark_complete(self) -> "Task":
        """
        Mark this task complete and return a new Task due on the next occurrence.
        Uses timedelta to calculate: daily → +1 day, weekly → +7 days.
        """
        self.completed = True
        days_ahead = FREQUENCY_DAYS.get(self.frequency, 1)
        next_due = self.due_date + datetime.timedelta(days=days_ahead)
        return Task(
            name=self.name,
            duration=self.duration,
            priority=self.priority,
            preferred_time=self.preferred_time,
            frequency=self.frequency,
            completed=False,
            due_date=next_due,
        )

    def display(self):
        status = "Done" if self.completed else "Pending"
        print(f"[{self.priority.upper()}] {self.name} | {self.duration} min | {self.preferred_time} | {self.frequency} | due {self.due_date} | {status}")


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        self.tasks.append(task)
        print(f"Task '{task.name}' added for {self.name}.")

    def remove_task(self, task_name: str):
        self.tasks = [t for t in self.tasks if t.name != task_name]
        print(f"Task '{task_name}' removed from {self.name}.")

    def complete_task(self, task_name: str):
        """
        Mark a task complete by name and automatically add the next
        occurrence back into the task list with the updated due date.
        """
        for task in self.tasks:
            if task.name == task_name and not task.completed:
                next_task = task.mark_complete()
                self.tasks.append(next_task)
                print(f"'{task.name}' marked complete. Next occurrence scheduled for {next_task.due_date}.")
                return
        print(f"No pending task named '{task_name}' found for {self.name}.")

    def view_tasks(self):
        if not self.tasks:
            print(f"{self.name} has no tasks.")
        else:
            print(f"\nTasks for {self.name}:")
            for task in self.tasks:
                task.display()


class Owner:
    def __init__(self, name: str, available_minutes: int):
        self.name = name
        self.available_minutes = available_minutes
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        self.pets.append(pet)
        print(f"Pet '{pet.name}' added for owner {self.name}.")

    def view_pets(self):
        if not self.pets:
            print(f"{self.name} has no pets.")
        else:
            print(f"\n{self.name}'s pets:")
            for pet in self.pets:
                print(f"  - {pet.name} ({pet.species}, age {pet.age})")

    def get_all_tasks(self) -> List[Task]:
        """Collect all tasks across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def get_filtered_tasks(self, completed: bool = None, pet_name: str = None) -> List[Task]:
        """
        Algorithm 2 — Filtering.
        Returns tasks filtered by completion status and/or pet name.
        - completed=True  → only done tasks
        - completed=False → only pending tasks
        - completed=None  → all tasks
        - pet_name        → only tasks belonging to that pet
        """
        results = []
        for pet in self.pets:
            if pet_name and pet.name != pet_name:
                continue
            for task in pet.tasks:
                if completed is None or task.completed == completed:
                    results.append(task)
        return results


class Scheduler:
    def __init__(self, pet: Pet, owner: Owner):
        self.pet = pet
        self.owner = owner

    def sort_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks high → medium → low."""
        return sorted(tasks, key=lambda t: PRIORITY_ORDER.get(t.priority, 99))

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """
        Algorithm 1 — Sort by time of day.
        Orders tasks morning → afternoon → evening so the schedule
        flows naturally through the day.
        """
        return sorted(tasks, key=lambda t: TIME_ORDER.get(t.preferred_time, 99))

    def filter_by_frequency(self, tasks: List[Task], is_weekly_day: bool = False) -> List[Task]:
        """
        Algorithm 3 — Recurring task handling.
        Daily tasks always appear. Weekly tasks only appear when is_weekly_day=True.
        This prevents grooming or vet tasks from cluttering every day's schedule.
        """
        return [t for t in tasks if t.frequency == "daily" or (t.frequency == "weekly" and is_weekly_day)]

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """
        Algorithm 4 — Lightweight conflict detection.
        Returns a list of warning messages (never crashes).
        Checks:
        1. Total duration exceeds owner's available time.
        2. Any time slot (morning/afternoon/evening) is overloaded beyond 60 min,
           and names which tasks are causing the clash.
        """
        warnings = []
        total = sum(t.duration for t in tasks)

        if total > self.owner.available_minutes:
            warnings.append(
                f"Total task time ({total} min) exceeds available time ({self.owner.available_minutes} min)."
            )

        # Group tasks by time slot and check each slot
        for slot in ["morning", "afternoon", "evening"]:
            slot_tasks = [t for t in tasks if t.preferred_time == slot]
            slot_total = sum(t.duration for t in slot_tasks)
            if slot_total > 60:
                names = ", ".join(t.name for t in slot_tasks)
                warnings.append(
                    f"'{slot}' slot overloaded: {slot_total} min across [{names}] — exceeds 60 min window."
                )

        for w in warnings:
            print(f"⚠️  Warning: {w}")

        return warnings

    def generate_schedule(self, is_weekly_day: bool = False) -> List[Task]:
        """
        Full scheduling pipeline:
        1. Filter out weekly tasks if today isn't the weekly day.
        2. Sort by priority so high-priority tasks get time first.
        3. Fit tasks within available time (greedy).
        4. Sort the final schedule by time of day for a natural flow.
        5. Detect and report any conflicts.
        """
        # Step 1: filter recurring tasks
        tasks = self.filter_by_frequency(self.pet.tasks, is_weekly_day)

        # Step 2: sort by priority to decide what gets scheduled first
        tasks = self.sort_by_priority(tasks)

        # Step 3: detect conflicts before trimming
        self.detect_conflicts(tasks)

        # Step 4: greedily fill schedule within available time
        schedule = []
        time_remaining = self.owner.available_minutes
        for task in tasks:
            if task.duration <= time_remaining:
                schedule.append(task)
                time_remaining -= task.duration

        # Step 5: sort the final schedule by time of day
        schedule = self.sort_by_time(schedule)

        print(f"\nDaily Schedule for {self.pet.name} (owner: {self.owner.name}):")
        print(f"Available time: {self.owner.available_minutes} min")
        print("-" * 40)
        if not schedule:
            print("No tasks fit within the available time.")
        for task in schedule:
            task.display()
        print(f"\nTime used: {self.owner.available_minutes - time_remaining} min | Remaining: {time_remaining} min")

        return schedule
