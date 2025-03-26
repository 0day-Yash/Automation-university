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
your_email = "jfasdosiohsdj@gmail.com"
your_password = "xxxx xxxx xxxx xxxx"

# Set up SMTP server connection
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(your_email, your_password)

# BCC email addresses
bcc_emails = ["yashk.pvt@gmail.com"]

# Subject for the email
subject = "Inquiry about...?"

# HTML Email Template
message_template = """
<html>
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
