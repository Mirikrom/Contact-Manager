from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

# Ma'lumotlar bazasi modellari

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_verified = models.BooleanField(default=True)  # Default True qilamiz
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, email_verified=True)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()

class Group(models.Model):
    """
    Kontakt guruhi modeli.
    Guruh nomi, tavsifi va yaratuvchi ma'lumotlarini saqlaydi.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # Guruh nomi
    description = models.TextField(blank=True)  # Guruh tavsifi (ixtiyoriy)
    created_at = models.DateTimeField(auto_now_add=True)  # Yaratilgan vaqti
    updated_at = models.DateTimeField(auto_now=True)  # O'zgartirilgan vaqti
    contacts = models.ManyToManyField('Contact', related_name='groups', blank=True)  # Kontakt guruhlari

    def __str__(self):
        return self.name

class Contact(models.Model):
    """
    Kontakt modeli.
    Kontakt haqidagi barcha ma'lumotlarni saqlaydi.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)  # Ism
    last_name = models.CharField(max_length=50)  # Familiya
    email = models.EmailField()  # Elektron pochta
    phone = models.CharField(max_length=20)  # Telefon raqami
    address = models.TextField(blank=True)  # Manzil (ixtiyoriy)
    created_at = models.DateTimeField(auto_now_add=True)  # Yaratilgan vaqti
    updated_at = models.DateTimeField(auto_now=True)  # O'zgartirilgan vaqti
    image = models.ImageField(upload_to='contact_images/', null=True, blank=True)  # Rasm (ixtiyoriy)

    class Meta:
        ordering = ['first_name', 'last_name']  # Ism va familiya bo'yicha tartiblash

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
