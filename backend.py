from flask import Flask, request, jsonify

from fpdf import FPDF
import os
from datetime import datetime


app = Flask(__name__, static_folder="static")



# Global task list
todo_list = []

@app.route('/download-tasks', methods=['GET'])
def download_tasks():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Your To-Do List", ln=True, align="C")
    pdf.ln(10)

    if not todo_list:
        pdf.cell(200, 10, txt="No tasks available.", ln=True, align="L")
    else:
        for task in todo_list:
            pdf.cell(200, 10, txt=f"✅ {task['task']} - {task['category']} - {task['status']}", ln=True, align="L")

    # ✅ Ensure 'static' directory exists
    static_folder = os.path.join(os.getcwd(), "static")
    if not os.path.exists(static_folder):
        os.makedirs(static_folder)

    # ✅ Save PDF in the 'static' folder
    pdf_file_path = os.path.join(static_folder, "tasks.pdf")
    pdf.output(pdf_file_path)

    # ✅ Debugging: Check if the file was actually created
    if os.path.exists(pdf_file_path):
        print(f"✅ PDF successfully saved at {pdf_file_path}")  # Debugging
        return jsonify({"message": "PDF generated successfully!", "pdf_url": f"http://127.0.0.1:5000/static/tasks.pdf"})
    else:
        print("❌ PDF file not found!")  # Debugging
        return jsonify({"error": "Failed to generate PDF - File not found"}), 500



# Route to get the to-do list
@app.route('/get-tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': todo_list})


@app.route('/update-task-status', methods=['POST'])
def update_task_status():
    global todo_list
    data = request.get_json()
    task_name = data.get("task")
    new_status = data.get("status")

    for task in todo_list:
        if task["task"] == task_name:
            task["status"] = new_status

            # ✅ If task is marked "Done", store completion date & time
            if new_status == "Done":
                task["completed_time"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                task["remaining"] = f"✅ Completed on {task['completed_time']}"
            else:
                # ✅ If task is still pending, update remaining time
                submission_datetime = datetime.strptime(task["submission_time"], "%d/%m/%Y %H:%M")
                remaining_time = submission_datetime - datetime.now()

                days, seconds = divmod(remaining_time.total_seconds(), 86400)
                hours, seconds = divmod(seconds, 3600)
                minutes, seconds = divmod(seconds, 60)

                task["remaining"] = f"{int(days)}d {int(hours)}h {int(minutes)}m {int(seconds)}s left"

            return jsonify({"message": f"Task '{task_name}' status updated to {new_status}!", "tasks": todo_list}), 200

    return jsonify({"error": "Task not found"}), 404


# Route to add a task with category, reminder, and default status


@app.route('/add-task', methods=['POST'])
def add_task():
    global todo_list
    data = request.get_json()
    task = data.get("task")
    submission_time = data.get("submission_time")  # ✅ Expecting `DD/MM/YYYY HH:MM`
    category = data.get("category", "General")

    # Check if task name already exists
    for existing_task in todo_list:
        if existing_task["task"].lower() == task.lower():
            return jsonify({"error": "Task name already exists. Please choose a different name."}), 400

    if task and submission_time:
        try:
            # ✅ Ensure correct datetime format (`DD/MM/YYYY HH:MM`)
            submission_datetime = datetime.strptime(submission_time, "%d/%m/%Y %H:%M")
            remaining_time = submission_datetime - datetime.now()

            # Convert to days/hours/minutes
            days, seconds = divmod(remaining_time.total_seconds(), 86400)
            hours, seconds = divmod(seconds, 3600)
            minutes, _ = divmod(seconds, 60)

            remaining_text = f"{int(days)}d {int(hours)}h {int(minutes)}m left"

            # ✅ Append new task
            new_task = {
                "task": task,
                "submission_time": submission_time,  # ✅ Store in `DD/MM/YYYY HH:MM`
                "category": category,
                "status": "Remaining",
                "remaining": remaining_text
            }
            todo_list.append(new_task)

            return jsonify({"message": f"Task '{task}' added successfully!", "tasks": todo_list}), 201
        except ValueError:
            return jsonify({"error": "Invalid datetime format! Please use DD/MM/YYYY HH:MM"}), 400

    return jsonify({"error": "Task, category, and submission time cannot be empty"}), 400

# Route to delete a task
@app.route('/delete-task', methods=['POST'])
def delete_task():
    global todo_list
    data = request.get_json()
    task = data.get("task")

    todo_list = [t for t in todo_list if t["task"] != task]

    return jsonify({"message": f"Task '{task}' deleted successfully!", "tasks": todo_list}), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

