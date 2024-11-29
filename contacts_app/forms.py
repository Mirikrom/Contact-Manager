from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Contact, Group, UserProfile

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        label='Foydalanuvchi nomi',
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'placeholder': 'Foydalanuvchi nomi'
        }),
        error_messages={
            'required': 'Foydalanuvchi nomini kiriting',
            'invalid': 'Iltimos, to\'g\'ri foydalanuvchi nomi kiriting'
        }
    )
    email = forms.EmailField(
        label='Elektron pochta',
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'placeholder': 'Elektron pochta'
        }),
        error_messages={
            'required': 'Elektron pochtani kiriting',
            'invalid': 'Iltimos, to\'g\'ri elektron pochta kiriting'
        }
    )
    first_name = forms.CharField(
        label='Ismingiz',
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'placeholder': 'Ismingiz'
        }),
        required=False,
        error_messages={
            'required': 'Ismingizni kiriting',
            'invalid': 'Iltimos, to\'g\'ri ism kiriting'
        }
    )
    last_name = forms.CharField(
        label='Familiyangiz',
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'placeholder': 'Familiyangiz'
        }),
        required=False,
        error_messages={
            'required': 'Familiyangizni kiriting',
            'invalid': 'Iltimos, to\'g\'ri familiya kiriting'
        }
    )
    password1 = forms.CharField(
        label='Parol',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'placeholder': 'Parol'
        }),
        error_messages={
            'required': 'Parolni kiriting',
            'invalid': 'Iltimos, kuchli parol kiriting'
        }
    )
    password2 = forms.CharField(
        label='Parolni tasdiqlash',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'placeholder': 'Parolni tasdiqlash'
        }),
        error_messages={
            'required': 'Parolni tasdiqlang',
            'invalid': 'Parollar bir-biriga mos emas'
        }
    )
    image = forms.ImageField(
        label='Profil rasmi',
        widget=forms.FileInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'accept': 'image/*'
        }),
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'image']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Parollar bir-biriga mos emas")
        return password2

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Rasm hajmini tekshirish (10 MB)
            if image.size > 10 * 1024 * 1024:
                raise forms.ValidationError("Rasm hajmi 10 MB dan oshmasligi kerak.")
        return image

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class ContactForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500'
        })
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500'
        })
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500'
        })
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 h-24'
        })
    )
    image = forms.ImageField(
        widget=forms.FileInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'accept': 'image/*'
        }),
        required=False
    )
    
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'image']
        
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Rasm hajmini tekshirish (10 MB)
            if image.size > 10 * 1024 * 1024:
                raise forms.ValidationError("Rasm hajmi 10 MB dan oshmasligi kerak.")
        return image

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = self.instance.user if self.instance.pk else None
        if email and Contact.objects.filter(user=user, email=email).exclude(pk=self.instance.pk if self.instance.pk else None).exists():
            raise forms.ValidationError('Bu email manzili sizning kontaktlaringiz orasida allaqachon mavjud.')
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        user = self.instance.user if self.instance.pk else None
        if phone and Contact.objects.filter(user=user, phone=phone).exclude(pk=self.instance.pk if self.instance.pk else None).exists():
            raise forms.ValidationError('Bu telefon raqami sizning kontaktlaringiz orasida allaqachon mavjud.')
        return phone

class GroupForm(forms.ModelForm):
    contacts = forms.ModelMultipleChoiceField(
        queryset=Contact.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-checkbox h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500'
        }),
    )
    
    class Meta:
        model = Group
        fields = ['name', 'description', 'contacts']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input px-4 py-3 rounded-full'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea px-4 py-3 rounded-lg', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['contacts'].queryset = Contact.objects.filter(user=user)

    def save(self, commit=True):
        group = super().save(commit=False)
        if commit:
            group.save()
            self.save_m2m()  # Kontaktlarni saqlash
        return group

class GroupEditForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input px-4 py-3 rounded-full'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea px-4 py-3 rounded-lg', 'rows': 3}),
        }

class UserProfileForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500'
        })
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500'
        }),
        required=False
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500'
        }),
        required=False
    )
    image = forms.ImageField(
        widget=forms.FileInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'accept': 'image/*'
        }),
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            try:
                user_profile = self.instance.userprofile
            except UserProfile.DoesNotExist:
                user_profile = UserProfile.objects.create(user=self.instance)

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Profil rasmini saqlash
            if self.cleaned_data.get('image'):
                user.userprofile.image = self.cleaned_data['image']
                user.userprofile.save()
        return user
