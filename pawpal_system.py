from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    name: str
    duration: int           # in minutes
    priority: str           # "high", "medium", or "low"
    preferred_time: str     # "morning", "afternoon", or "evening"

    def display(self):
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        pass

    def remove_task(self, task: Task):
        pass

    def view_tasks(self):
        pass


class Owner:
    def __init__(self, name: str, available_minutes: int):
        self.name = name
        self.available_minutes = available_minutes
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        pass

    def view_pets(self):
        pass


class Scheduler:
    def __init__(self, pet: Pet, owner: Owner):
        self.pet = pet
        self.owner = owner

    def generate_schedule(self):
        pass

    def sort_by_priority(self):
        pass

    def detect_conflicts(self):
        pass
