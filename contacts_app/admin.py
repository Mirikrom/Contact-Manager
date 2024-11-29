from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from .models import Contact, Group as ContactGroup, UserProfile
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django import forms


# Django Groups ni admin panelidan o'chirish
admin.site.unregister(Group)

# User admin ni qayta e'lon qilish
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    email_verified = forms.BooleanField(
        required=False,
        initial=True,
        label="Email tasdiqlangan",
        help_text="Email manzili tasdiqlangan deb belgilash"
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Yangi foydalanuvchi yaratilayotganda
            obj.is_active = True
        obj.save()

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            actions['delete_selected'] = (
                self.delete_selected,
                'delete_selected',
                "Tanlangan foydalanuvchilarni o'chirish"
            )
        return actions

    def delete_selected(self, request, queryset):
        if request.POST.get('post'):  # Tasdiqlash so'rovi
            queryset.delete()
            return None
        
        context = {
            'title': "Foydalanuvchilarni o'chirish",
            'queryset': queryset,
            'action': 'delete_selected',
            'deletable_objects': [obj for obj in queryset],
        }
        return self.delete_view(request, context)
    delete_selected.short_description = "Tanlangan foydalanuvchilarni o'chirish"
    
    actions = ['delete_selected']

# Standart UserAdmin ni o'chirib, yangisini ro'yxatdan o'tkazish
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'user', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'phone', 'email')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('first_name', 'last_name', 'phone', 'email', 'user')
        }),
        ('Qo\'shimcha ma\'lumotlar', {
            'fields': ('image', 'created_at', 'updated_at')
        })
    )

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'To\'liq ismi'


@admin.register(ContactGroup)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'contact_count', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('contacts',)

    def contact_count(self, obj):
        return obj.contacts.count()
    contact_count.short_description = 'Kontaktlar soni'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_email', 'get_email_verified')
    list_filter = ('email_verified',)
    search_fields = ('user__username', 'user__email')
    fields = ('user', 'email_verified', 'verification_token')
    readonly_fields = ('verification_token',)

    def get_email(self, obj):
        return obj.user.email if obj.user else ''
    get_email.short_description = 'Email'

    def get_email_verified(self, obj):
        return obj.email_verified
    get_email_verified.short_description = 'Email tasdiqlangan'
    get_email_verified.boolean = True  # True/False ni chiroyli ko'rsatish uchun

    def has_delete_permission(self, request, obj=None):
        return True

    def delete_queryset(self, request, queryset):
        deleted_count = 0
        for profile in queryset:
            try:
                user = profile.user
                user.delete()  # Bu UserProfile ni ham o'chiradi (CASCADE bo'lgani uchun)
                deleted_count += 1
            except Exception as e:
                messages.error(request, f"Xatolik: {str(e)}")
        
        if deleted_count > 0:
            messages.success(request, f"{deleted_count} ta foydalanuvchi muvaffaqiyatli o'chirildi.")

    def delete_model(self, request, obj):
        try:
            user = obj.user
            user.delete()
            messages.success(request, "Foydalanuvchi muvaffaqiyatli o'chirildi.")
        except Exception as e:
            messages.error(request, f"Xatolik: {str(e)}")

    def has_module_permission(self, request):
        return True
