import smtplib
import pandas as pd
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load CSV and initialize Sent_Status if not present
df = pd.read_csv("/srv/dev-disk-by-uuid-f4827f3c-9537-4d3a-8090-55cd8559677e/500gb WD Green/colleges/colleges.csv", encoding='utf-8')
if "Sent_Status" not in df.columns:
    df["Sent_Status"] = ""  # Initialize empty column if missing

# Email account details
your_email = "Yashkulkarni20008@gmail.com"
your_password = "ttmd jkhe skog mtax"

# Set up SMTP server connection
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(your_email, your_password)

# BCC email addresses
bcc_emails = ["yashk.pvt@gmail.com"]

# Subject for the email
subject = "Inquiry About B.Tech Admissions and Opportunities"

# HTML Email Template
message_template = """
<html>
<body>
<p>Dear Admissions Team,</p>

<p>I hope this email finds you well. My name is <b>Yash Amol Kulkarni</b>, and I am currently pursuing my 12th-grade education, with core subjects in <b>Physics, Chemistry, Mathematics, and Computer Science</b>. I am reaching out to explore admission opportunities for your esteemed <b>B.Tech program</b>, particularly in fields related to <b>cybersecurity, web development, and technological innovation</b>.</p>

<p>Over the past few years, I’ve been fortunate to contribute meaningfully to the tech community while developing my skills in <b>cybersecurity</b>, <b>ethical hacking</b>, and <b>leadership</b>. Below are some key milestones from my journey:</p>

<ul>
    <li><b>Founder & CEO of PurpleRain TechSafe:</b> I lead a cybersecurity firm focused on delivering real-time threat alerts, network security reports, and digital safety solutions to small businesses and enterprises.</li>
    <li><b>Co-Founder of CodeQuestt Hackathon:</b> I co-organized CodeQuestt, a dynamic hackathon that generated over <b>₹4 lakh (over 4000USD) in revenue and sponsorships</b> in just two months, attracting creative minds from across the country.</li>
    <li><b>Ethical Hacker and OSINT Specialist:</b> I lead a cybersecurity team called <b>CypherSec</b>, and I actively collaborate with <b>Trace Labs</b> to locate missing persons through <b>OSINT (Open-Source Intelligence)</b> investigations.</li>
    <li><b>National Robotics Achievements:</b> Representing Punjab, I secured <b>4th place at the ATL All-India Robotics Championship</b> with a score of <b>93.75/100</b>.</li>
</ul>

<p>In addition to my extracurricular pursuits, I have maintained a strong academic foundation, ranking consistently at the top of my class. My <b>11th-grade scores</b> are as follows:</p>

<ul>
    <li><b>Physics:</b> 86/100</li>
    <li><b>Chemistry:</b> 87/100</li>
    <li><b>Mathematics:</b> 84/100</li>
    <li><b>Computer Science:</b> 93/100</li>
    <li><b>English:</b> 90/100</li>
</ul>

<p>I would also appreciate any guidance regarding:</p>

<ol>
    <li><b>Scholarship opportunities,</b> especially those offering full or partial tuition waivers for students with achievements in entrepreneurship, technology, or leadership.</li>
    <li><b>Application strategies</b> that could enhance my chances of standing out, particularly with my background in cybersecurity, ethical hacking, and innovation.</li>
</ol>

<p>Thank you for taking the time to review my email. I look forward to learning more about the opportunities your institution offers and how I can be part of your vibrant academic and extracurricular community.</p>

<p>Warm regards,<br>
<b>Yash Amol Kulkarni</b><br>
Founder & CEO, PurpleRain TechSafe<br>
📞 +91 9915181929 | 🌐 <a href="https://yashk.app">yashk.app</a><br>
<a href="https://www.linkedin.com/in/yashkulkarni08/">LinkedIn Profile</a></p>
</body>
</html>
"""

# Email sending configuration
batch_size = 400
delay_between_emails = 10  # 10-second delay between emails
sent_count = 0

# Send emails in batch
for index, row in df.iterrows():
    if row.get("Sent_Status") == "Sent":
        continue  # Skip if already sent

    college_name = row["College"]
    recipient_email = row["Email"]

    msg = MIMEMultipart()
    msg["From"] = your_email
    msg["To"] = recipient_email
    msg["Bcc"] = ", ".join(bcc_emails)  # Joining BCC emails as a string
    msg["Subject"] = subject
    msg.attach(MIMEText(message_template, "html"))  # Attach as HTML

    try:
        server.sendmail(your_email, [recipient_email] + bcc_emails, msg.as_string())
        print(f"Email sent to {college_name} at {recipient_email}!")

        # Mark the email as sent and save the DataFrame after each email
        df.at[index, "Sent_Status"] = "Sent"
        df.to_csv("/srv/dev-disk-by-uuid-f4827f3c-9537-4d3a-8090-55cd8559677e/500gb WD Green/colleges/colleges.csv", index=False)
        print(f"Marked {college_name} as 'Sent' in the CSV.")

        sent_count += 1

        # Stop after reaching the batch limit
        if sent_count >= batch_size:
            print("Reached daily limit of 400 emails.")
            break

        time.sleep(delay_between_emails)

    except Exception as e:
        print(f"Failed to send email to {recipient_email}: {e}")
        # Retry SMTP connection if the server disconnects
        try:
            print("Reconnecting to SMTP server...")
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(your_email, your_password)
        except Exception as smtp_error:
            print(f"Failed to reconnect to SMTP server: {smtp_error}")
            break  # Stop if reconnection fails

# Save the CSV file again after completing the batch
df.to_csv("/srv/dev-disk-by-uuid-f4827f3c-9537-4d3a-8090-55cd8559677e/500gb WD Green/colleges/colleges.csv", index=False)

# Close the SMTP server connection
server.quit()
