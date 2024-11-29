import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'contacts.settings')
django.setup()

from django.contrib.auth.models import User
from contacts_app.models import UserProfile

print("\nFoydalanuvchilar ro'yxati:")
print("-" * 50)
for user in User.objects.all():
    try:
        profile = UserProfile.objects.get(user=user)
        verified = "Tasdiqlangan" if profile.email_verified else "Tasdiqlanmagan"
    except UserProfile.DoesNotExist:
        verified = "Profil topilmadi"
    
    print(f"ID: {user.id}")
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    print(f"Email holati: {verified}")
    print(f"Faol: {'Ha' if user.is_active else 'Yo\'q'}")
    print("-" * 50)
    print({user})
