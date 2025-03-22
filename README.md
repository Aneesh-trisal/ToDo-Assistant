# 📝 AI-Powered To-Do List Assistant  

A web-based task management assistant that helps users organize tasks, track deadlines, categorize progress, and download task lists as PDFs.  

🔹 **Frontend:** Streamlit  
🔹 **Backend:** Flask (Deployed on Render)  
🔹 **Features:** Task management, real-time countdown, PDF export, auto-refresh  

---

## 🔧 Methods & Libraries Used  

- **Backend:** Flask (`flask`) – Handles task management and API requests  
- **Frontend:** Streamlit (`streamlit`, `streamlit-autorefresh`) – Displays UI and updates dynamically  
- **Speech Recognition (Future):** `speechrecognition`, `gtts` – For voice-based task input  
- **Task Storage:** JSON-based storage (can be replaced with a database)  
- **PDF Generation:** `fpdf` – Allows exporting task lists  
- **Authentication (Future):** Google OAuth (Planned) – Enable cross-platform access  

---

## 📜 Requirements & Installation  
**Required Libraries:**  
fpdf==1.7.2  
requests==2.32.3  
streamlit==1.43.2  
streamlit-autorefresh==1.0.1  
flask  
speechrecognition  
gtts  

🛠 Features
✔ Task Management – Add, delete, update tasks
✔ Task Categorization – Remaining, In Progress, Completed
✔ Deadline Tracking – Real-time countdown for upcoming tasks
✔ Save as PDF – Export task list for offline use
✔ Auto Refresh – Updates dynamically without manual refresh
✔ Smooth UI – User-friendly interface

🔮 Future Enhancements
🔹 🎤 Voice Assistance (Planned) – Add tasks using speech commands
🔹 🔑 Google OAuth Authentication (Planned) – Cross-platform user authentication
🔹 📅 Calendar Integration (Planned) – Sync tasks with Google Calendar
🔹 💾 Database Storage (Planned) – Replace JSON with SQL for better scalability
🔹 📧 Email Reminders (Planned) – Get alerts for upcoming deadlines

!!!Thank You!!!