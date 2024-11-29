from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('contact_list')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now login.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def google_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Agar foydalanuvchi mavjud bo'lmasa, yangi yaratamiz
        if not User.objects.filter(email=email).exists():
            username = email.split('@')[0]  # email dan username yasaymiz
            # Agar bunday username mavjud bo'lsa, raqam qo'shamiz
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
        else:
            user = User.objects.get(email=email)
            # Parolni yangilaymiz
            user.set_password(password)
            user.save()
        
        # Login qilamiz
        user = authenticate(username=user.username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Muvaffaqiyatli kirdingiz!")
            return redirect('contact_list')
        
    return redirect('login')
