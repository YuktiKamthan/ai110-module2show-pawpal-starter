from pawpal_system import Task, Pet, Owner, Scheduler

# --- Setup ---
owner = Owner(name="Alex", available_minutes=90)

# --- Pets ---
dog = Pet(name="Buddy", species="Dog", age=3)
cat = Pet(name="Whiskers", species="Cat", age=5)

# --- Tasks for Buddy ---
dog.add_task(Task(name="Morning Walk",  duration=30, priority="high",   preferred_time="morning"))
dog.add_task(Task(name="Feeding",       duration=10, priority="high",   preferred_time="morning"))
dog.add_task(Task(name="Medication",    duration=5,  priority="medium", preferred_time="afternoon"))
dog.add_task(Task(name="Playtime",      duration=20, priority="low",    preferred_time="evening"))

# --- Tasks for Whiskers ---
cat.add_task(Task(name="Feeding",       duration=10, priority="high",   preferred_time="morning"))
cat.add_task(Task(name="Grooming",      duration=15, priority="medium", preferred_time="afternoon"))
cat.add_task(Task(name="Enrichment",    duration=20, priority="low",    preferred_time="evening"))

# --- Add pets to owner ---
owner.add_pet(dog)
owner.add_pet(cat)

# --- View pets ---
owner.view_pets()

# --- Generate schedules ---
print("\n" + "=" * 40)
scheduler_dog = Scheduler(pet=dog, owner=owner)
scheduler_dog.generate_schedule()

print("\n" + "=" * 40)
scheduler_cat = Scheduler(pet=cat, owner=owner)
scheduler_cat.generate_schedule()
