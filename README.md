# Automation-university
Automates college email outreach by sending personalized emails in batches, tracking status in a CSV, handling errors, and running persistently with progress-saving and SMTP reconnection.


### **Project Description: Automated College Email Outreach System**

#### **Objective:**
The goal of this project is to automate the process of sending personalized admission inquiry emails to universities worldwide. The system is designed to send batches of emails with personalized content, track which colleges have already received emails, and ensure that the process is both scalable and persistent even during interruptions like SSH disconnections.

This project aims to streamline the application process for students, especially those seeking admission opportunities in highly competitive fields like cybersecurity, web development, and innovation.

---

### **Core Functionalities:**

1. **CSV File Handling:**
   - The system reads a CSV file containing college names and their email addresses. The CSV file is located at:
     ```
     /srv/dev-disk-by-uuid-f4827f3c-9537-4d3a-8090-55cd8559677e/500gb WD Green/colleges/colleges.csv
     ```
   - The CSV file includes a `Sent_Status` column, which is used to track whether an email has already been sent to a particular college. If this column is missing, it is automatically added.

2. **Email Configuration:**
   - The email is sent using the Simple Mail Transfer Protocol (SMTP) through Gmail’s SMTP server:
     ```
     smtp.gmail.com (Port: 587)
     ```
   - The sender's email address and password are securely stored within the script.

3. **Email Composition:**
   - **Subject:**  
     `Inquiry About B.Tech Admissions and Opportunities`
   - **Body Content:**  
     An HTML-based template with professional formatting, including the applicant's background, achievements, academic scores, and a request for information on scholarships and application strategies.
   - The HTML template is designed to render properly in email clients, ensuring that important details (like bolded accomplishments) are visually emphasized.

4. **BCC Handling:**
   - Additional email addresses (like personal backup accounts) are added as BCC recipients for tracking purposes.

5. **Batch Processing and Rate Limiting:**
   - The system sends emails in batches of 400 per day to avoid Gmail’s spam filters.
   - A 10-second delay is added between sending individual emails to further reduce the risk of flagging.

6. **Error Handling and Retry Mechanism:**
   - If an email fails to send due to SMTP disconnection, the system automatically attempts to reconnect and retry.
   - All errors are printed to the console for troubleshooting.

7. **Status Tracking and Resume Functionality:**
   - After each email is sent, the `Sent_Status` column in the CSV is updated to "Sent" for that college.
   - The CSV file is saved after each email to prevent data loss in case of unexpected interruptions.
   - If the script is restarted, it will resume from the next unsent email.

---

### **Technical Highlights:**

- **Persistent Execution with `tmux` or `nohup`:**  
  The script can be executed persistently using either `tmux` or `nohup`, ensuring that it continues to run even after SSH disconnections.

- **Email Attachments and Future Scalability:**  
  The current system is modular and can be extended to include additional functionalities like email attachments, multiple templates, or dynamic content based on college data.

---

### **Step-by-Step Workflow:**

1. **CSV Handling:**
   - Load the CSV file using `pandas` and check for the presence of the `Sent_Status` column.
   - If the column is missing, initialize it.

2. **Email Setup:**
   - Configure the SMTP server with the sender's email credentials.
   - Define the BCC email addresses for tracking.

3. **Email Template:**
   - Construct an HTML-based email template with personalized content.

4. **Batch Email Sending:**
   - Iterate through the rows of the CSV file.
   - Skip rows that are already marked as "Sent."
   - Send emails to colleges one by one, with a 10-second delay between each email.

5. **Status Update and CSV Saving:**
   - Mark each sent email in the CSV file by updating the `Sent_Status` column.
   - Save the CSV file after each email to avoid progress loss.

6. **Error Handling and SMTP Reconnection:**
   - Catch and print any errors that occur during the email-sending process.
   - Attempt to reconnect to the SMTP server if disconnected.

7. **End Process:**
   - Save the CSV file one final time and close the SMTP connection once the batch is complete.

---

### **How to Run the Script Persistently:**

#### **Option 1: Using `nohup`:**
```bash
nohup python3 /srv/dev-disk-by-uuid-f4827f3c-9537-4d3a-8090-55cd8559677e/500gb\ WD\ Green/colleges/automation.py > nohup.out 2>&1 &
```
- This will run the script in the background and redirect the output to `nohup.out`.

#### **Option 2: Using `tmux`:**
1. Start a new `tmux` session:
   ```bash
   tmux new -s email_script
   ```
2. Run the script inside the session:
   ```bash
   python3 /srv/dev-disk-by-uuid-f4827f3c-9537-4d3a-8090-55cd8559677e/500gb\ WD\ Green/colleges/automation.py
   ```
3. Detach from the session by pressing `Ctrl + B`, then `D`.
4. Reattach later with:
   ```bash
   tmux attach -t email_script
   ```

---

### **Expected Output:**
- Console output displaying the status of each email sent.
- Live logs in `nohup.out` or visible inside the `tmux` session.
- Updated CSV file with the `Sent_Status` column reflecting which colleges have already been emailed.

---

This project is a powerful solution for automating large-scale email outreach, saving time, and improving efficiency in the college application process.
