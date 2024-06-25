import os
from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .models import Donation


@shared_task
def process_donation(donation_id):
    donation = Donation.objects.get(id=donation_id)
    donation.status = 'completed'
    donation.save()
    send_donation_notification_email.delay(donation.id)


@shared_task
def send_donation_notification_email(donation_id):
    donation = Donation.objects.get(id=donation_id)

    # Email to the streamer
    subject_streamer = f'New Donation - Rp {donation.amount}'
    from_email = f"{os.getenv('MAIL_FROM_NAME')} <{os.getenv('MAIL_FROM_EMAIL')}>"
    recipient_list_streamer = [donation.stream.streamer.email]

    # Render the HTML message for the streamer
    html_message_streamer = render_to_string('emails/donation_received_streamer.html', {'donation': donation})

    email_streamer = EmailMessage(subject_streamer, html_message_streamer, from_email, recipient_list_streamer)
    email_streamer.content_subtype = 'html'
    email_streamer.send(fail_silently=False)

    # Email to the donor
    subject_donor = f'Thank You for Your Donation - Rp {donation.amount}'
    recipient_list_donor = [donation.donor.email]

    # Render the HTML message for the donor
    html_message_donor = render_to_string('emails/donation_received_donor.html', {'donation': donation})

    email_donor = EmailMessage(subject_donor, html_message_donor, from_email, recipient_list_donor)
    email_donor.content_subtype = 'html'
    email_donor.send(fail_silently=False)
