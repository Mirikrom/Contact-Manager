from faker import Faker
from django.contrib.auth.models import User
from contacts_app.models import Contact
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'contacts.settings')
django.setup()

fake = Faker()
user = User.objects.get(id=2)

for i in range(20):
    Contact.objects.create(
        user=user,
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.unique.email(),
        phone=f'+99890{fake.unique.random_number(digits=7)}',
        address=fake.address()
    )
