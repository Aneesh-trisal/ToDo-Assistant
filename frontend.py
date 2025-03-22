import streamlit as st
import requests
from datetime import datetime
import time
import streamlit_autorefresh  # ✅ To refresh countdown dynamically


BASE_URL = "https://todo-assistant-on2d.onrender.com"

st.set_page_config(layout="wide")

st.title("📝 AI-Powered To-Do List Assistant with Task Progress 📂")

# Function to download tasks as PDF
def download_pdf():
    response = requests.get(f"{BASE_URL}/download-tasks")
    if response.status_code == 200:
        data = response.json()
        pdf_url = data.get("pdf_url")
        if pdf_url:
            st.markdown(f"[📄 Download Tasks PDF]({pdf_url})", unsafe_allow_html=True)  # ✅ Direct Download Link
    else:
        st.warning("⚠️ Failed to generate PDF.", icon="⚠️")


# Function to safely trigger rerun
def rerun_app():
    if "rerun" not in st.session_state:
        st.session_state["rerun"] = True
    else:
        st.session_state["rerun"] = not st.session_state["rerun"]

# Function to get tasks from the backend
def get_tasks():
    response = requests.get(f"{BASE_URL}/get-tasks")
    if response.status_code == 200:
        data = response.json()
        return data.get("tasks", []) if data else []
    return []
# Function to update task status
def update_task_status(task, status):
    response = requests.post(f"{BASE_URL}/update-task-status", json={"task": task, "status": status})
    try:
        if response.status_code == 200:
            st.rerun()  # ✅ Forces UI refresh instantly
        return response.json()
    except requests.exceptions.JSONDecodeError:
        return {"error": "Invalid response from the server"}

# Function to delete a task
def delete_task(task):
    response = requests.post(f"{BASE_URL}/delete-task", json={"task": task})
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        return {"error": "Invalid response from the server"}

# Function to activate voice assistant
def voice_add_task():
    response = requests.get(f"{BASE_URL}/voice-add-task")

    try:
        data = response.json()
        if "message" in data:
            st.toast(data["message"], icon="✅")  # ✅ Safer UI update
        elif "error" in data:
            st.toast(data["error"], icon="⚠️")  # ✅ Prevents background thread issues
    except requests.exceptions.JSONDecodeError:
        st.toast("Invalid response from the server", icon="⚠️")


# Create layout with two columns
col1, col2 = st.columns([2, 1])

# **LEFT SIDE: Display Tasks**
with col1:
    st.subheader("📋 Your Tasks (Grouped by Status)")
    if st.button("📄 Save as PDF", key="save_pdf_button"):
        download_pdf()
    tasks = get_tasks()
    if tasks:
        statuses = ["Remaining", "In Process", "Done"]
        for status in statuses:
            status_tasks = [task for task in tasks if task["status"] == status]
            if status_tasks:
                st.markdown(f"### {status} Tasks")
                for task in status_tasks:
                    col1_1, col1_2, col1_3 = st.columns([4, 1, 1])

                    with col1_1:
                        task_display = st.empty()  # ✅ Placeholder for real-time updates

                        if status == "Done":
                            time_display = f"✅ Completed on {task['completed_time']}"
                        else:
                            submission_datetime = datetime.strptime(task["submission_time"], "%d/%m/%Y %H:%M")
                            remaining_time = submission_datetime - datetime.now()

                            days, seconds = divmod(remaining_time.total_seconds(), 86400)
                            hours, seconds = divmod(seconds, 3600)
                            minutes, seconds = divmod(seconds, 60)

                            time_display = f"⏳ {int(days)}d {int(hours)}h {int(minutes)}m {int(seconds)}s left"

                        task_display.markdown(f"""
                        <div class='task-box'>
                        ✅ <b>{task['task']}</b> <span style='color: gray;'>({task['category']})</span> 
                        <br><small>📅 Submission: {task['submission_time']} | {time_display}</small>
                        </div>
                        """, unsafe_allow_html=True)

                        # ✅ Auto-refresh every 1 second without blocking the UI
                        streamlit_autorefresh.st_autorefresh(interval=1000, limit=None, key=f"refresh_{task['task']}")

                    with col1_2:
                        status_options = ["Remaining", "In Process", "Done"]
                        new_status = st.selectbox("Change Status", status_options, index=status_options.index(task["status"]), key=f"status_{task['task']}")
                        if new_status != task["status"]:
                            update_task_status(task["task"], new_status)
                            st.rerun()  # ✅ Only update UI, keeping form & dropdown active

                    with col1_3:
                        if st.button("❌", key=f"del_{task['task']}"):
                            delete_task(task["task"])
                            st.rerun()  # ✅ Prevents UI from freezing
    else:
        st.write("No tasks yet! Add one on the right side. 😊")

# **RIGHT SIDE: Task Entry Form**
# **RIGHT SIDE: Task Entry Form**
with col2:
    st.subheader("➕ Add a New Task")

    new_task = st.text_input("Enter a task:")
    submission_date = st.date_input("Select submission date:")  # ✅ Updated label
    submission_time = st.time_input("Select submission time:")  # ✅ Updated label

    category = st.selectbox("Select a category:", ["Work", "Personal", "Urgent", "Other"])

    # Button to add a task manually
    if st.button("➕ Add Task", key="add_task_button"):
        if new_task:
            # ✅ Ensure proper datetime format (DD/MM/YYYY HH:MM)
            submission_datetime = f"{submission_date.strftime('%d/%m/%Y')} {submission_time.strftime('%H:%M')}"
            try:
                datetime.strptime(submission_datetime, "%d/%m/%Y %H:%M")  # Validate format
                response = requests.post(f"{BASE_URL}/add-task", json={"task": new_task, "submission_time": submission_datetime, "category": category})
        
                if response.status_code == 400:
                    st.warning(response.json().get("error"), icon="⚠️")
                else:
                    st.success(f"Task '{new_task}' added successfully! 🎉")
                    st.rerun()
            except ValueError:
                st.warning("Invalid date or time format! Please try again.", icon="⚠️")



    # 🎤 Button to add task via voice
    if st.button("🎤 Add Task via Voice", key="voice_add_task_button"):
        voice_add_task()
