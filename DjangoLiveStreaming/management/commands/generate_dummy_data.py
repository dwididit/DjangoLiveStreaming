import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from DjangoLiveStreaming.models import Stream, Donation, Comment
from faker import Faker

User = get_user_model()

class Command(BaseCommand):
    help = 'Generate dummy data for the application and create a superuser'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin'
            )
            print('Superuser "admin" created with password "adminpassword"')

        # Create dummy users
        users = []
        for _ in range(10):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='password',
                is_streamer=fake.boolean()
            )
            users.append(user)
            print(f"Created user: {user.username}")

        # Create dummy streams
        streams = []
        for user in User.objects.filter(is_streamer=True):
            for _ in range(3):
                stream = Stream.objects.create(
                    title=fake.sentence(),
                    description=fake.paragraph(),
                    streamer=user,
                    is_active=fake.boolean()
                )
                streams.append(stream)
                print(f"Created stream: {stream.title} by {user.username}")

        # Create dummy donations
        donors = User.objects.exclude(is_streamer=True)
        for stream in streams:
            for _ in range(5):
                donation = Donation.objects.create(
                    amount=round(random.uniform(10.0, 100.0), 2),
                    message=fake.sentence(),
                    stream=stream,
                    donor=random.choice(donors),
                    payment_method=random.choice(['credit_card', 'virtual_account', 'bank_transfer']),
                    status=random.choice(['pending', 'completed', 'failed']),
                )
                print(f"Created donation: {donation.amount} to {stream.title}")

        # Create dummy comments
        for stream in streams:
            for _ in range(10):
                comment = Comment.objects.create(
                    content=fake.sentence(),
                    user=random.choice(users),
                    stream=stream
                )
                print(f"Created comment: {comment.content} on {stream.title}")

        self.stdout.write(self.style.SUCCESS('Dummy data generated successfully'))
