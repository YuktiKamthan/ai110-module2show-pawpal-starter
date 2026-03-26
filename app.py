import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# --- Session state initialization ---
if "owner" not in st.session_state:
    st.session_state.owner = None
if "pet" not in st.session_state:
    st.session_state.pet = None

st.title("🐾 PawPal+")
st.caption("A smart pet care management system.")
st.divider()

# ── Section 1: Owner Setup ─────────────────────────────────────────────────────
st.subheader("1. Owner Setup")

with st.form("owner_form"):
    owner_name = st.text_input("Your name", value="Jordan")
    available_minutes = st.number_input("Available time today (minutes)", min_value=10, max_value=480, value=90)
    submitted_owner = st.form_submit_button("Save Owner")

if submitted_owner:
    st.session_state.owner = Owner(name=owner_name, available_minutes=int(available_minutes))
    st.session_state.pet = None

if st.session_state.owner:
    st.success(f"Owner: {st.session_state.owner.name} | Available time: {st.session_state.owner.available_minutes} min")

st.divider()

# ── Section 2: Pet Setup ───────────────────────────────────────────────────────
st.subheader("2. Add a Pet")

if not st.session_state.owner:
    st.info("Please save an owner first.")
else:
    with st.form("pet_form"):
        pet_name = st.text_input("Pet name", value="Mochi")
        species = st.selectbox("Species", ["Dog", "Cat", "Other"])
        age = st.number_input("Age", min_value=0, max_value=30, value=2)
        submitted_pet = st.form_submit_button("Add Pet")

    if submitted_pet:
        new_pet = Pet(name=pet_name, species=species, age=age)
        st.session_state.owner.add_pet(new_pet)
        st.session_state.pet = new_pet

    if st.session_state.pet:
        st.success(f"Active pet: {st.session_state.pet.name} ({st.session_state.pet.species}, age {st.session_state.pet.age})")

st.divider()

# ── Section 3: Add Tasks ───────────────────────────────────────────────────────
st.subheader("3. Add Care Tasks")

if not st.session_state.pet:
    st.info("Please add a pet first.")
else:
    with st.form("task_form"):
        col1, col2 = st.columns(2)
        with col1:
            task_name = st.text_input("Task name", value="Morning walk")
            duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
        with col2:
            priority = st.selectbox("Priority", ["high", "medium", "low"])
            preferred_time = st.selectbox("Time of day", ["morning", "afternoon", "evening"])
            frequency = st.selectbox("Frequency", ["daily", "weekly"])
        submitted_task = st.form_submit_button("Add Task")

    if submitted_task:
        new_task = Task(
            name=task_name,
            duration=int(duration),
            priority=priority,
            preferred_time=preferred_time,
            frequency=frequency,
        )
        st.session_state.pet.add_task(new_task)
        st.success(f"Task '{task_name}' added.")

    # Display current tasks
    pending_tasks = [t for t in st.session_state.pet.tasks if not t.completed]
    done_tasks = [t for t in st.session_state.pet.tasks if t.completed]

    if pending_tasks:
        st.write(f"**Pending tasks for {st.session_state.pet.name}:**")
        st.table([
            {
                "Task": t.name,
                "Duration (min)": t.duration,
                "Priority": t.priority.upper(),
                "Time of Day": t.preferred_time,
                "Frequency": t.frequency,
                "Due": str(t.due_date),
            }
            for t in pending_tasks
        ])
    else:
        st.info("No pending tasks. Add one above.")

    if done_tasks:
        with st.expander(f"Completed tasks ({len(done_tasks)})"):
            st.table([
                {"Task": t.name, "Due": str(t.due_date)}
                for t in done_tasks
            ])

    # Mark task complete
    if pending_tasks:
        st.write("**Mark a task complete:**")
        task_to_complete = st.selectbox(
            "Select task",
            options=[t.name for t in pending_tasks],
            key="complete_select"
        )
        if st.button("Mark Complete"):
            st.session_state.pet.complete_task(task_to_complete)
            st.success(f"'{task_to_complete}' marked complete. Next occurrence auto-scheduled!")
            st.rerun()

st.divider()

# ── Section 4: Generate Schedule ──────────────────────────────────────────────
st.subheader("4. Generate Today's Schedule")

if not st.session_state.pet or not st.session_state.pet.tasks:
    st.info("Add at least one task before generating a schedule.")
else:
    is_weekly_day = st.toggle("Today is a weekly task day (e.g. grooming day)")

    if st.button("Generate Schedule"):
        scheduler = Scheduler(pet=st.session_state.pet, owner=st.session_state.owner)

        # Run conflict detection first and show warnings
        all_tasks = [t for t in st.session_state.pet.tasks if not t.completed]
        conflict_warnings = scheduler.detect_conflicts(all_tasks)
        for w in conflict_warnings:
            st.warning(f"Conflict detected: {w}")

        # Generate the sorted schedule
        schedule = scheduler.generate_schedule(is_weekly_day=is_weekly_day)

        if schedule:
            st.success(f"Schedule generated for **{st.session_state.pet.name}** — sorted by time of day")

            schedule_data = [
                {
                    "Time of Day": t.preferred_time.capitalize(),
                    "Task": t.name,
                    "Duration (min)": t.duration,
                    "Priority": t.priority.upper(),
                    "Frequency": t.frequency,
                }
                for t in schedule
            ]
            st.table(schedule_data)

            total_used = sum(t.duration for t in schedule)
            remaining = st.session_state.owner.available_minutes - total_used
            st.info(f"Time used: **{total_used} min** | Remaining: **{remaining} min**")

            skipped = len(all_tasks) - len(schedule)
            if skipped > 0:
                st.warning(f"{skipped} task(s) were skipped — they didn't fit within your available time.")
        else:
            st.warning("No tasks could be scheduled. Tasks may exceed available time or all are weekly tasks on a non-weekly day.")
