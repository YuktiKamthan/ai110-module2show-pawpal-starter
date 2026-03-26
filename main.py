from pawpal_system import Task, Pet, Owner, Scheduler

# --- Setup ---
owner = Owner(name="Alex", available_minutes=90)

# --- Pets ---
dog = Pet(name="Buddy", species="Dog", age=3)
cat = Pet(name="Whiskers", species="Cat", age=5)

# --- Tasks for Buddy (added OUT OF ORDER intentionally) ---
dog.add_task(Task(name="Playtime",      duration=20, priority="low",    preferred_time="evening"))
dog.add_task(Task(name="Medication",    duration=5,  priority="medium", preferred_time="afternoon"))
dog.add_task(Task(name="Feeding",       duration=10, priority="high",   preferred_time="morning"))
dog.add_task(Task(name="Morning Walk",  duration=30, priority="high",   preferred_time="morning"))

# --- Tasks for Whiskers ---
cat.add_task(Task(name="Enrichment",    duration=20, priority="low",    preferred_time="evening",   frequency="weekly"))
cat.add_task(Task(name="Grooming",      duration=15, priority="medium", preferred_time="afternoon", frequency="weekly"))
cat.add_task(Task(name="Feeding",       duration=10, priority="high",   preferred_time="morning"))

# Mark one task as done to test filtering
dog.tasks[0].mark_complete()  # Playtime is done

# --- Add pets to owner ---
owner.add_pet(dog)
owner.add_pet(cat)

print("=" * 40)
print("DEMO 1: Schedule sorted by TIME OF DAY (not insertion order)")
print("=" * 40)
scheduler_dog = Scheduler(pet=dog, owner=owner)
scheduler_dog.generate_schedule()

print("\n" + "=" * 40)
print("DEMO 2: Recurring task filtering (not a weekly day)")
print("Weekly tasks like Grooming and Enrichment should be excluded.")
print("=" * 40)
scheduler_cat = Scheduler(pet=cat, owner=owner)
scheduler_cat.generate_schedule(is_weekly_day=False)

print("\n" + "=" * 40)
print("DEMO 3: Recurring task filtering (IS a weekly day)")
print("Weekly tasks should now appear.")
print("=" * 40)
scheduler_cat.generate_schedule(is_weekly_day=True)

print("\n" + "=" * 40)
print("DEMO 4: Filter — only PENDING tasks across all pets")
print("=" * 40)
pending = owner.get_filtered_tasks(completed=False)
for t in pending:
    t.display()

print("\n" + "=" * 40)
print("DEMO 5: Filter — only COMPLETED tasks across all pets")
print("=" * 40)
done = owner.get_filtered_tasks(completed=True)
if done:
    for t in done:
        t.display()
else:
    print("No completed tasks.")

print("\n" + "=" * 40)
print("DEMO 6: Filter — only Buddy's tasks")
print("=" * 40)
buddy_tasks = owner.get_filtered_tasks(pet_name="Buddy")
for t in buddy_tasks:
    t.display()
