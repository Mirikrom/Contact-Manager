from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from contacts_app.models import Contact
from faker import Faker
import random
from django.core.files import File
import requests
from io import BytesIO
import os

class Command(BaseCommand):
    help = 'Generate fake contacts with Uzbek names and phone numbers'

    def handle(self, *args, **kwargs):
        fake = Faker('uz_UZ')  # O'zbek tili uchun
        
        # Admin foydalanuvchisini olish
        try:
            user = User.objects.get(username='admin')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Admin foydalanuvchisi topilmadi'))
            return

        # 20 ta kontakt yaratish
        for i in range(20):
            # Random avatar olish
            avatar_url = f'https://i.pravatar.cc/150?img={random.randint(1, 70)}'
            response = requests.get(avatar_url)
            if response.status_code == 200:
                img_temp = BytesIO(response.content)
                img_temp.name = f'avatar_{i}.jpg'

                # Kontakt ma'lumotlarini generatsiya qilish
                gender = random.choice(['male', 'female'])
                if gender == 'male':
                    first_name = fake.first_name_male()
                    last_name = fake.last_name_male()
                else:
                    first_name = fake.first_name_female()
                    last_name = fake.last_name_female()

                contact = Contact(
                    user=user,
                    first_name=first_name,
                    last_name=last_name,
                    email=f"{first_name.lower()}.{last_name.lower()}@{fake.free_email_domain()}",
                    phone=f"+998{random.randint(90, 99)}{random.randint(1000000, 9999999)}",
                    address=fake.address(),
                    notes=fake.text(max_nb_chars=200)
                )
                
                # Rasmni saqlash
                contact.image.save(img_temp.name, File(img_temp), save=True)
                
                self.stdout.write(self.style.SUCCESS(f'Kontakt yaratildi: {contact.first_name} {contact.last_name}'))
