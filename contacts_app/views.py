from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from .models import Contact, Group, User, UserProfile
from .forms import ContactForm, GroupForm, GroupEditForm, UserRegistrationForm, UserProfileForm
import os

@login_required
def contact_list(request):
    contacts = Contact.objects.filter(user=request.user).order_by('first_name', 'last_name')
    paginator = Paginator(contacts, 5)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    return render(request, 'contacts_app/contact_list.html', {'contacts': contacts})

@login_required
def search_contacts(request):
    query = request.GET.get('q', '')
    if query:
        contacts = Contact.objects.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query),
            user=request.user
        ).order_by('first_name', 'last_name')
    else:
        contacts = Contact.objects.filter(user=request.user).order_by('first_name', 'last_name')
    
    paginator = Paginator(contacts, 5)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    
    if request.headers.get('HX-Request'):
        return render(request, 'contacts_app/partials/contact_list.html', {'contacts': contacts})
    return render(request, 'contacts_app/contact_list.html', {'contacts': contacts})

@login_required
def contact_add(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            messages.success(request, 'Kontakt muvaffaqiyatli qo\'shildi.')
            return redirect('contact_list')
    else:
        form = ContactForm()
    return render(request, 'contacts_app/contact_add.html', {'form': form})

@login_required
def contact_edit(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kontakt muvaffaqiyatli yangilandi.')
            return redirect('contact_list')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'contacts_app/contact_edit.html', {'form': form, 'contact': contact})

@login_required
def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    
    # Agar kontaktda rasm bo'lsa, uni o'chirish
    if contact.image:
        try:
            image_path = contact.image.path
            contact.delete()
            
            # Kontakt o'chirilgandan keyin rasmni o'chirish
            if os.path.exists(image_path):
                os.remove(image_path)
        except Exception as e:
            # Agar rasm o'chirishda muammo bo'lsa, logga yozish
            print(f"Rasm o'chirishda xatolik: {e}")
            contact.delete()
    else:
        contact.delete()
    
    messages.success(request, 'Kontakt muvaffaqiyatli o\'chirildi.')
    return redirect('contact_list')

@login_required
def bulk_delete_contacts(request):
    if request.method == 'POST':
        print("POST request received")
        print("POST data:", request.POST)
        contact_ids = request.POST.getlist('contact_ids')
        print("Contact IDs to delete:", contact_ids)
        
        if contact_ids:
            contacts = Contact.objects.filter(user=request.user, id__in=contact_ids)
            deleted_count = contacts.count()
            print(f"Found {deleted_count} contacts to delete")
            
            # Rasmlarni o'chirish
            for contact in contacts:
                if contact.image:
                    try:
                        if os.path.exists(contact.image.path):
                            os.remove(contact.image.path)
                            print(f"Deleted image for contact {contact.id}")
                    except Exception as e:
                        print(f"Rasm o'chirishda xatolik: {e}")
            
            # Kontaktlarni o'chirish
            contacts.delete()
            print(f"Deleted {deleted_count} contacts")
            messages.success(request, f'{deleted_count} ta kontakt muvaffaqiyatli o\'chirildi.')
        else:
            print("No contact IDs received")
            messages.error(request, 'O\'chirish uchun kontaktlar tanlanmagan.')
    else:
        print("Non-POST request received")
    return redirect('contact_list')

@login_required
def group_list(request):
    groups = Group.objects.filter(user=request.user).order_by('name')
    paginator = Paginator(groups, 10)
    page = request.GET.get('page')
    groups = paginator.get_page(page)
    return render(request, 'contacts_app/group_list.html', {'groups': groups})

@login_required
def group_create(request):
    if request.method == 'POST':
        form = GroupForm(request.POST, user=request.user)
        if form.is_valid():
            group = form.save(commit=False)
            group.user = request.user
            group.save()
            # Kontaktlarni saqlash
            form.save_m2m()
            messages.success(request, 'Guruh muvaffaqiyatli yaratildi.')
            return redirect('group_list')
    else:
        form = GroupForm(user=request.user)
    return render(request, 'contacts_app/group_form.html', {'form': form})

@login_required
def group_detail(request, pk):
    group = get_object_or_404(Group, pk=pk, user=request.user)
    contacts = group.contacts.all().order_by('first_name', 'last_name')
    paginator = Paginator(contacts, 5)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    
    if request.headers.get('HX-Request'):
        return render(request, 'contacts_app/partials/group_contacts.html', 
                     {'group': group, 'contacts': contacts})
    return render(request, 'contacts_app/group_detail.html', 
                 {'group': group, 'contacts': contacts})

@login_required
def group_edit(request, pk):
    group = get_object_or_404(Group, pk=pk, user=request.user)
    if request.method == 'POST':
        form = GroupEditForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, 'Guruh muvaffaqiyatli yangilandi.')
            return redirect('group_list')
    else:
        form = GroupEditForm(instance=group)
    return render(request, 'contacts_app/group_form.html', {'form': form, 'edit_mode': True})

@login_required
def group_delete(request, pk):
    group = get_object_or_404(Group, pk=pk, user=request.user)
    if request.method == 'POST':
        group_name = group.name
        group.delete()
        messages.success(request, f'"{group_name}" guruhi muvaffaqiyatli o\'chirildi.')
        return redirect('group_list')
    return render(request, 'contacts_app/group_confirm_delete.html', {'group': group})

@login_required
def add_contact_to_group(request, group_pk, contact_pk):
    group = get_object_or_404(Group, pk=group_pk, user=request.user)
    contact = get_object_or_404(Contact, pk=contact_pk, user=request.user)
    group.contacts.add(contact)
    return redirect('group_detail', pk=group_pk)

@login_required
def remove_contact_from_group(request, group_pk, contact_pk):
    group = get_object_or_404(Group, pk=group_pk, user=request.user)
    contact = get_object_or_404(Contact, pk=contact_pk, user=request.user)
    group.contacts.remove(contact)
    
    if request.headers.get('HX-Request'):
        contacts = group.contacts.all().order_by('first_name', 'last_name')
        paginator = Paginator(contacts, 5)
        page = request.GET.get('page', 1)
        contacts = paginator.get_page(page)
        return render(request, 'contacts_app/partials/group_contacts.html',
                     {'group': group, 'contacts': contacts})
    return redirect('group_detail', pk=group_pk)

@login_required
def add_contacts_to_group(request, pk):
    group = get_object_or_404(Group, pk=pk, user=request.user)
    
    if request.method == 'POST':
        contact_ids = request.POST.getlist('contacts')
        contacts = Contact.objects.filter(id__in=contact_ids, user=request.user)
        group.contacts.add(*contacts)
        messages.success(request, 'Kontaktlar guruhga qo\'shildi.')
        return redirect('group_detail', pk=pk)
    
    # Get contacts that are not in the group
    existing_contacts = group.contacts.all()
    available_contacts = Contact.objects.filter(user=request.user).exclude(id__in=existing_contacts)
    
    return render(request, 'contacts_app/add_contacts_to_group.html', {
        'group': group,
        'contacts': available_contacts
    })

@login_required
def delete_group_contacts(request, pk):
    group = get_object_or_404(Group, pk=pk, user=request.user)
    if request.method == 'POST':
        contact_ids = request.POST.getlist('contact_ids[]')
        if contact_ids:
            contacts = Contact.objects.filter(id__in=contact_ids, user=request.user)
            for contact in contacts:
                group.contacts.remove(contact)
            messages.success(request, f"{len(contact_ids)} ta kontakt guruhdan o'chirildi")
        return redirect('group_detail', pk=pk)
    return redirect('group_detail', pk=pk)

@login_required
def search_group_contacts(request, pk):
    group = get_object_or_404(Group, id=pk, user=request.user)
    query = request.GET.get('q', '')
    
    if query:
        contacts = group.contacts.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query)
        ).order_by('first_name', 'last_name')
    else:
        contacts = group.contacts.all().order_by('first_name', 'last_name')
    
    paginator = Paginator(contacts, 5)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    
    if request.headers.get('HX-Request'):
        return render(request, 'contacts_app/partials/group_contacts.html', {'contacts': contacts, 'group': group})
    return render(request, 'contacts_app/group_detail.html', {'contacts': contacts, 'group': group})

@login_required
def get_all_contact_ids(request):
    contact_ids = list(Contact.objects.filter(user=request.user).values_list('id', flat=True))
    return JsonResponse({'contact_ids': contact_ids})

@login_required
def get_group_contact_ids(request, pk):
    group = get_object_or_404(Group, pk=pk, user=request.user)
    contact_ids = list(group.contacts.values_list('id', flat=True))
    return JsonResponse({
        'contact_ids': contact_ids,
        'total_count': len(contact_ids)
    })

@login_required
def profile(request):
    user = request.user
    return render(request, 'contacts_app/profile.html', {'user': user})

@login_required
def profile_edit(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil muvaffaqiyatli yangilandi.')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'contacts_app/profile_edit.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Email validatsiyasi
            if not (email.endswith('@gmail.com') or email.endswith('@mail.ru') or 
                   email.endswith('@yahoo.com') or email.endswith('@yandex.ru')):
                messages.error(request, "Iltimos, to'g'ri email manzilini kiriting (gmail.com, mail.ru, yahoo.com yoki yandex.ru)")
                return render(request, 'registration/register.html', {'form': form})
            
            try:
                user = form.save(commit=False)
                # user.is_active = False  # Email tasdiqlangunicha login qila olmaydi email bilan tasdiqlash uchun yoqish kerak bo'ladi.
                user.is_active = True  # Email tasdiqlash shart emas.
                user.save()
                
                # Verification token yaratish
                # token = default_token_generator.make_token(user) #email bilan tasdiqlash uchun yoqish kerak bo'ladi.
                
                # Tasdiqlash emailini yuborish
                # verification_url = request.build_absolute_uri(f'/verify-email/{token}/')
                # send_mail(
                #     'Elektron pochtani tasdiqlash',
                #     f'Elektron pochtangizni tasdiqlash uchun ushbu havolani bosing: {verification_url}',    #email bilan tasdiqlash uchun yoqish kerak bo'ladi.
                #     settings.DEFAULT_FROM_EMAIL,
                #     [user.email],
                #     fail_silently=False,
                # )
                
                # messages.success(request, 'Hisobni yaratish uchun elektron pochtangizga kelgan xabarni tasdiqlang.') #email bilan tasdiqlash uchun yoqish kerak bo'ladi.
                messages.success(request, 'Hisobingiz muvaffaqiyatli yaratildi. Endi tizimga kirishingiz mumkin.')
                return redirect('login')
            except Exception as e:
                user.delete()  # Xatolik bo'lsa foydalanuvchini o'chirish 
                # messages.error(request, "Email yuborishda xatolik yuz berdi. Iltimos, boshqa email manzil bilan urinib ko'ring.")
                messages.error(request, "Xatolik yuz berdi. Iltimos, qayta urinib ko'ring.")
                return render(request, 'registration/register.html', {'form': form})
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def verify_email(request, token):
    try:
        # Token orqali foydalanuvchini topish
        user = User.objects.filter(is_active=False).first()
        if user and default_token_generator.check_token(user, token):
            # Foydalanuvchini aktivlashtirish
            user.is_active = True
            user.save()
            
            # UserProfile ni yangilash
            user_profile = UserProfile.objects.get(user=user)
            user_profile.email_verified = True
            user_profile.save()
            
            messages.success(request, 'Email manzil tasdiqlandi! Endi tizimga kirishingiz mumkin.')
            return redirect('login')
        else:
            messages.error(request, 'Noto\'g\'ri tasdiqlash havolasi!')
            return redirect('login')
    except Exception as e:
        messages.error(request, 'Tasdiqlashda xatolik yuz berdi. Iltimos, qaytadan urinib ko\'ring.')
        return redirect('login')

def password_reset_request(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            # Avval username bo'yicha qidirish
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Username topilmasa, email bo'yicha qidirish
                user = User.objects.get(email=username)
                
            # Token va uid yaratish
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Reset URL yaratish
            reset_url = request.build_absolute_uri(
                reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            )
            
            # Email yuborish
            try:
                send_mail(
                    'Parolni tiklash so\'rovi',
                    f'Parolni tiklash uchun ushbu havolani bosing: {reset_url}',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                messages.success(request, 'Parolni tiklash havolasi elektron pochtangizga yuborildi.')
                return redirect('password_reset_done')
            except Exception as mail_error:
                print(f"Email yuborishda xatolik: {str(mail_error)}")
                messages.error(request, 'Email yuborishda xatolik yuz berdi. Iltimos, keyinroq qayta urinib ko\'ring.')
                
        except User.DoesNotExist:
            messages.error(request, 'Bunday foydalanuvchi topilmadi.')
        except Exception as e:
            print(f"Umumiy xatolik: {str(e)}")
            messages.error(request, 'So\'rovni bajarishda xatolik yuz berdi.')
    
    return render(request, 'registration/password_reset_form.html')

def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')
            
            if new_password1 and new_password2:
                if new_password1 == new_password2:
                    user.set_password(new_password1)
                    user.save()
                    messages.success(request, 'Parolingiz muvaffaqiyatli o\'zgartirildi.')
                    return redirect('login')
                else:
                    messages.error(request, 'Parollar bir xil emas.')
            else:
                messages.error(request, 'Iltimos, barcha maydonlarni to\'ldiring.')
        
        return render(request, 'registration/password_reset_confirm.html')
    else:
        messages.error(request, 'Parolni tiklash havolasi yaroqsiz yoki muddati o\'tgan.')
        return redirect('password_reset')

def password_reset_complete(request):
    return render(request, 'registration/password_reset_complete.html')
