import os
import sys
import django

# Django sozlamalarini qo'lda o'rnatish
sys.path.append('c:/Users/Bouncer/CascadeProjects/contacts')
os.environ['DJANGO_SETTINGS_MODULE'] = 'contacts.settings'
django.setup()

import random
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from faker import Faker
from PIL import Image
import io
from contacts_app.models import Contact

# Lokal Faker obyektini yaratish
fake = Faker('ru_RU')  # Rus lokalizatsiyasi

def generate_random_image(width=300, height=300):
    """Tasodifiy rang bilan rasm yaratish"""
    color = (
        random.randint(100, 255), 
        random.randint(100, 255), 
        random.randint(100, 255)
    )
    image = Image.new('RGB', (width, height), color)
    
    # Rasm uchun byte buffer
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    return SimpleUploadedFile(
        name=f'{fake.uuid4()}.png', 
        content=img_byte_arr, 
        content_type='image/png'
    )

def generate_contacts(user, num_contacts=30):
    """Tasodifiy kontaktlar yaratish"""
    for _ in range(num_contacts):
        first_name = fake.first_name()
        last_name = fake.last_name()
        
        contact = Contact(
            user=user,
            first_name=first_name,
            last_name=last_name,
            email=fake.email(),
            phone=fake.phone_number(),
            address=fake.address(),
            image=generate_random_image()
        )
        contact.save()
        print(f"Kontakt yaratildi: {first_name} {last_name}")

def main():
    user = User.objects.get(id=33)
    generate_contacts(user, num_contacts=200)
    print(f"200 ta kontakt muvaffaqiyatli yaratildi!")

if __name__ == '__main__':
    main()
