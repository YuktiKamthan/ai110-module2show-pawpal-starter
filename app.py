import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# --- Session state initialization ---
# These run only once when the app first loads.
# On every rerun, Streamlit finds them already in the "vault" and skips creation.
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
    # Create a real Owner object and store it in session state
    st.session_state.owner = Owner(name=owner_name, available_minutes=int(available_minutes))
    st.session_state.pet = None  # reset pet when owner changes

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
        # Create a real Pet object, call owner.add_pet() to register it
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
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            task_name = st.text_input("Task", value="Morning walk")
        with col2:
            duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
        with col3:
            priority = st.selectbox("Priority", ["high", "medium", "low"])
        with col4:
            preferred_time = st.selectbox("Time of day", ["morning", "afternoon", "evening"])
        submitted_task = st.form_submit_button("Add Task")

    if submitted_task:
        # Create a real Task object and call pet.add_task()
        new_task = Task(
            name=task_name,
            duration=int(duration),
            priority=priority,
            preferred_time=preferred_time
        )
        st.session_state.pet.add_task(new_task)

    # Display current tasks as a table
    if st.session_state.pet.tasks:
        st.write(f"Tasks for **{st.session_state.pet.name}**:")
        task_data = [
            {
                "Task": t.name,
                "Duration (min)": t.duration,
                "Priority": t.priority,
                "Time of Day": t.preferred_time,
                "Done": t.completed
            }
            for t in st.session_state.pet.tasks
        ]
        st.table(task_data)
    else:
        st.info("No tasks yet. Add one above.")

st.divider()

# ── Section 4: Generate Schedule ──────────────────────────────────────────────
st.subheader("4. Generate Today's Schedule")

if not st.session_state.pet or not st.session_state.pet.tasks:
    st.info("Add at least one task before generating a schedule.")
else:
    if st.button("Generate Schedule"):
        scheduler = Scheduler(pet=st.session_state.pet, owner=st.session_state.owner)
        schedule = scheduler.generate_schedule()

        st.success(f"Schedule generated for **{st.session_state.pet.name}**!")
        st.write(f"Available time: **{st.session_state.owner.available_minutes} min**")

        total_used = sum(t.duration for t in schedule)
        remaining = st.session_state.owner.available_minutes - total_used

        for task in schedule:
            st.markdown(
                f"- **[{task.priority.upper()}]** {task.name} — {task.duration} min | {task.preferred_time}"
            )

        st.info(f"Time used: {total_used} min | Remaining: {remaining} min")

        if len(schedule) < len(st.session_state.pet.tasks):
            skipped = len(st.session_state.pet.tasks) - len(schedule)
            st.warning(f"{skipped} task(s) were skipped because they didn't fit in the available time.")
