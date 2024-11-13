# Custom Email Sender with OpenAI and SendGrid

## Description

This project is a **Custom Email Sender** that integrates:
- **OpenAI's GPT-4/3.5 API** for generating personalized email content.
- **SendGrid API** for securely sending emails.
- Real-time analytics for tracking sent, failed, and scheduled emails.
- A user-friendly dashboard built with **Streamlit**.

## Features
- Upload data from a CSV file.
- Use placeholders for customizing email templates (e.g., `{Name}`, `{Email}`).
- Generate email content using **OpenAI's GPT-4/3.5**.
- Send emails securely using **SendGrid**.
- Schedule emails for a specific time.
- Real-time analytics for sent, failed, and total emails.

## Requirements
- Python 3.7+
- Libraries: `streamlit`, `pandas`, `sendgrid`, `openai`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/custom-email-sender.git
   cd custom-email-sender
