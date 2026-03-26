from dataclasses import dataclass, field
from typing import List


PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    name: str
    duration: int           # in minutes
    priority: str           # "high", "medium", or "low"
    preferred_time: str     # "morning", "afternoon", or "evening"
    frequency: str = "daily"    # "daily" or "weekly"
    completed: bool = False

    def mark_complete(self):
        self.completed = True

    def display(self):
        status = "Done" if self.completed else "Pending"
        print(f"[{self.priority.upper()}] {self.name} | {self.duration} min | {self.preferred_time} | {self.frequency} | {status}")


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


class Scheduler:
    def __init__(self, pet: Pet, owner: Owner):
        self.pet = pet
        self.owner = owner

    def sort_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks high → medium → low."""
        return sorted(tasks, key=lambda t: PRIORITY_ORDER.get(t.priority, 99))

    def detect_conflicts(self, tasks: List[Task]) -> bool:
        """Return True if total task duration exceeds owner's available time."""
        total = sum(t.duration for t in tasks)
        if total > self.owner.available_minutes:
            print(f"Warning: Total task time ({total} min) exceeds available time ({self.owner.available_minutes} min).")
            return True
        return False

    def generate_schedule(self) -> List[Task]:
        """
        Retrieve tasks for this pet, sort by priority, and fit as many
        as possible within the owner's available time.
        """
        tasks = self.sort_by_priority(self.pet.tasks)
        self.detect_conflicts(tasks)

        schedule = []
        time_remaining = self.owner.available_minutes

        for task in tasks:
            if task.duration <= time_remaining:
                schedule.append(task)
                time_remaining -= task.duration

        print(f"\nDaily Schedule for {self.pet.name} (owner: {self.owner.name}):")
        print(f"Available time: {self.owner.available_minutes} min")
        print("-" * 40)
        if not schedule:
            print("No tasks fit within the available time.")
        for task in schedule:
            task.display()
        print(f"\nTime used: {self.owner.available_minutes - time_remaining} min | Remaining: {time_remaining} min")

        return schedule
