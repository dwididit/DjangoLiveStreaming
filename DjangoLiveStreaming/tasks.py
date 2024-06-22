from celery import shared_task
from django.core.mail import send_mail
from .models import Donation

@shared_task
def process_donation(donation_id):
    donation = Donation.objects.get(id=donation_id)
    # Here you can add code to process the donation through the payment gateway (e.g., Midtrans)
    donation.status = 'completed'
    donation.save()
    send_donation_notification_email(donation.id)

@shared_task
def send_donation_notification_email(donation_id):
    donation = Donation.objects.get(id=donation_id)
    send_mail(
        'Donation Received',
        f'Thank you for your donation of {donation.amount} to {donation.stream.title}.',
        'from@example.com',
        [donation.donor.email],
        fail_silently=False,
    )
