import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import time
from collections import Counter
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import openai

# Streamlit App Title
st.title("Custom Email Sender with OpenAI and SendGrid")

# Step 1: Upload CSV
st.header("Step 1: Upload Data")
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Data Preview:")
    st.dataframe(df)

if 'df' in locals():
    if 'Email' not in df.columns:
        st.error("The uploaded dataset must include an 'Email' column.")
        st.stop()

# Step 2: Customize Email Template
st.header("Step 2: Customize Your Email Template")
if uploaded_file:
    placeholders = df.columns.tolist()
    st.write(f"Available placeholders: {', '.join(placeholders)}")

prompt_template = st.text_area(
    "Enter your email prompt with placeholders (e.g., Dear {Name}, your order {OrderID} is ready)."
)

# Step 3: Generate and Preview Emails
st.header("Step 3: Generate Email Content Using OpenAI")
openai.api_key = st.text_input("Enter OpenAI API Key", type="password")

generated_emails = []
if 'df' in locals() and prompt_template:
    st.write("Preview customized emails:")
    for i, row in df.iterrows():
        try:
            # Generate email content using the new OpenAI API
            prompt = prompt_template.format(**row.to_dict())
            response = openai.ChatCompletion.create(
                model="gpt-4",  # Use gpt-4 or gpt-3.5-turbo
                messages=[
                    {"role": "system", "content": "You are an email assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                timeout=10  # Set a timeout of 10 seconds
            )
            email_content = response['choices'][0]['message']['content'].strip()
            generated_emails.append(email_content)
            st.write(f"Email to {row['Email']}:")
            st.write(email_content)
        except Exception as e:
            st.error(f"Error generating email for {row['Email']}: {e}")
            generated_emails.append("")  # Add placeholder for empty content

# Step 4: Send Emails with SendGrid
st.header("Step 4: Send Emails")
sendgrid_api_key = st.text_input("Enter SendGrid API Key", type="password")

schedule_option = st.radio(
    "Do you want to schedule the emails?",
    ["Send Now", "Schedule Later"]
)

if schedule_option == "Schedule Later":
    scheduled_time = st.time_input("Select time to send emails", datetime.now().time())

throttling_limit = st.number_input("Set the throttling limit (emails per minute):", min_value=1, value=10)

if st.button("Start Email Sending"):
    if not sendgrid_api_key:
        st.error("Please enter your SendGrid API Key.")
        st.stop()

    sent_emails = []
    failed_emails = []

    # Schedule emails
    if schedule_option == "Schedule Later":
        delay = (datetime.combine(datetime.today(), scheduled_time) - datetime.now()).total_seconds()
        st.write(f"Waiting for {delay} seconds to start...")
        time.sleep(max(0, delay))

    st.write("Sending emails...")
    for i, row in df.iterrows():
        try:
            email_content = generated_emails[i]
            if not email_content.strip():
                raise ValueError("Generated email content is empty.")

            # Send email via SendGrid
            message = Mail(
                from_email="your_verified_sender@example.com",  # Replace with your verified sender email
                to_emails=row['Email'],
                subject="Custom Email",
                html_content=email_content
            )
            sg = SendGridAPIClient(sendgrid_api_key)
            response = sg.send(message)

            if response.status_code == 202:
                sent_emails.append(row['Email'])
                st.success(f"Email sent to {row['Email']}")
            else:
                failed_emails.append(row['Email'])
                st.error(f"Failed to send to {row['Email']}: Status Code {response.status_code}")
        except Exception as e:
            failed_emails.append(row['Email'])
            st.error(f"Error sending email to {row['Email']}: {e}")

        # Throttling: Wait to maintain the limit
        if (i + 1) % throttling_limit == 0:
            time.sleep(60)

# Step 5: Real-Time Analytics
st.header("Step 5: Real-Time Analytics")
if 'sent_emails' in locals() or 'failed_emails' in locals():
    total_emails = len(sent_emails) + len(failed_emails)
    st.metric("Total Emails", total_emails)
    st.metric("Total Sent", len(sent_emails))
    st.metric("Total Failed", len(failed_emails))
    st.write("Analytics Breakdown:")
    st.write(Counter(sent_emails))
