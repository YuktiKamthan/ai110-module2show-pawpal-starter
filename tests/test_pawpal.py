import datetime
from pawpal_system import Task, Pet, Owner, Scheduler


def test_mark_complete_changes_status():
    """Calling mark_complete() should set task.completed to True."""
    task = Task(name="Walk", duration=30, priority="high", preferred_time="morning")
    assert task.completed == False
    task.mark_complete()
    assert task.completed == True


def test_add_task_increases_pet_task_count():
    """Adding a task to a Pet should increase its task list by 1."""
    pet = Pet(name="Buddy", species="Dog", age=3)
    assert len(pet.tasks) == 0
    pet.add_task(Task(name="Feeding", duration=10, priority="high", preferred_time="morning"))
    assert len(pet.tasks) == 1


def test_recurring_daily_task_schedules_next_day():
    """Completing a daily task should return a new task due tomorrow."""
    today = datetime.date.today()
    task = Task(name="Walk", duration=30, priority="high", preferred_time="morning", frequency="daily", due_date=today)
    next_task = task.mark_complete()
    assert next_task.due_date == today + datetime.timedelta(days=1)
    assert next_task.completed == False


def test_recurring_weekly_task_schedules_next_week():
    """Completing a weekly task should return a new task due in 7 days."""
    today = datetime.date.today()
    task = Task(name="Grooming", duration=15, priority="medium", preferred_time="afternoon", frequency="weekly", due_date=today)
    next_task = task.mark_complete()
    assert next_task.due_date == today + datetime.timedelta(days=7)


def test_complete_task_auto_adds_next_occurrence():
    """Pet.complete_task() should mark task done and add a new pending copy."""
    pet = Pet(name="Buddy", species="Dog", age=3)
    pet.add_task(Task(name="Walk", duration=30, priority="high", preferred_time="morning"))
    assert len(pet.tasks) == 1
    pet.complete_task("Walk")
    assert len(pet.tasks) == 2
    assert pet.tasks[0].completed == True
    assert pet.tasks[1].completed == False


def test_sort_by_time_orders_morning_first():
    """sort_by_time should order tasks morning → afternoon → evening."""
    owner = Owner("Alex", 120)
    pet = Pet("Buddy", "Dog", 3)
    pet.add_task(Task(name="Evening Play", duration=20, priority="low",    preferred_time="evening"))
    pet.add_task(Task(name="Afternoon Med", duration=5,  priority="medium", preferred_time="afternoon"))
    pet.add_task(Task(name="Morning Walk", duration=30, priority="high",   preferred_time="morning"))
    scheduler = Scheduler(pet=pet, owner=owner)
    sorted_tasks = scheduler.sort_by_time(pet.tasks)
    assert sorted_tasks[0].preferred_time == "morning"
    assert sorted_tasks[1].preferred_time == "afternoon"
    assert sorted_tasks[2].preferred_time == "evening"


def test_filter_pending_tasks_only():
    """get_filtered_tasks(completed=False) should return only pending tasks."""
    owner = Owner("Alex", 120)
    pet = Pet("Buddy", "Dog", 3)
    task1 = Task(name="Walk", duration=30, priority="high", preferred_time="morning")
    task2 = Task(name="Feeding", duration=10, priority="high", preferred_time="morning")
    task1.mark_complete()
    pet.add_task(task1)
    pet.add_task(task2)
    owner.add_pet(pet)
    pending = owner.get_filtered_tasks(completed=False)
    assert len(pending) == 1
    assert pending[0].name == "Feeding"


def test_conflict_detection_returns_warning_for_overloaded_slot():
    """detect_conflicts should return a warning when a time slot exceeds 60 min."""
    owner = Owner("Alex", 180)
    pet = Pet("Max", "Dog", 2)
    pet.add_task(Task(name="Long Walk", duration=40, priority="high",   preferred_time="morning"))
    pet.add_task(Task(name="Feeding",   duration=20, priority="high",   preferred_time="morning"))
    pet.add_task(Task(name="Training",  duration=20, priority="medium", preferred_time="morning"))
    scheduler = Scheduler(pet=pet, owner=owner)
    warnings = scheduler.detect_conflicts(pet.tasks)
    assert len(warnings) > 0
    assert any("morning" in w for w in warnings)


def test_weekly_tasks_excluded_on_non_weekly_day():
    """Weekly tasks should not appear in the schedule on a normal day."""
    owner = Owner("Alex", 120)
    pet = Pet("Whiskers", "Cat", 5)
    pet.add_task(Task(name="Feeding",  duration=10, priority="high",   preferred_time="morning", frequency="daily"))
    pet.add_task(Task(name="Grooming", duration=15, priority="medium", preferred_time="afternoon", frequency="weekly"))
    scheduler = Scheduler(pet=pet, owner=owner)
    schedule = scheduler.generate_schedule(is_weekly_day=False)
    names = [t.name for t in schedule]
    assert "Feeding" in names
    assert "Grooming" not in names
