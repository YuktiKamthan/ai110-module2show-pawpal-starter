from pawpal_system import Task, Pet


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
