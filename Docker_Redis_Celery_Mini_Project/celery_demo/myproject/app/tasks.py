from celery import shared_task
import time

@shared_task
def test_task():
    print("Task executed successfully!")

@shared_task
def send_welcome_email(username):
    print(f"Sending email to {username}...")
    time.sleep(5) # simulate delay
    print(f"Welcome email sent to {username}!")
    return f"Email sent to {username}"
