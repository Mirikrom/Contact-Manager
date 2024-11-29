from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.contact_list, name='home'),
    path('contacts/', views.contact_list, name='contact_list'),
    path('contacts/search/', views.search_contacts, name='search_contacts'),
    path('contacts/add/', views.contact_add, name='contact_add'),
    path('contacts/<int:pk>/edit/', views.contact_edit, name='contact_edit'),
    path('contacts/<int:pk>/delete/', views.contact_delete, name='contact_delete'),
    path('contacts/bulk-delete/', views.bulk_delete_contacts, name='bulk_delete_contacts'),
    path('contacts/get-all-ids/', views.get_all_contact_ids, name='get_all_contact_ids'),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    
    # Profile URLs
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    
    # Groups URLs
    path('groups/', views.group_list, name='group_list'),
    path('groups/add/', views.group_create, name='group_add'),
    path('groups/<int:pk>/', views.group_detail, name='group_detail'),
    path('groups/<int:pk>/edit/', views.group_edit, name='group_edit'),
    path('groups/<int:pk>/delete/', views.group_delete, name='group_delete'),
    path('groups/<int:pk>/add-contacts/', views.add_contacts_to_group, name='add_contacts_to_group'),
    path('groups/<int:group_pk>/contacts/<int:contact_pk>/add/', views.add_contact_to_group, name='add_contact_to_group'),
    path('groups/<int:group_pk>/contacts/<int:contact_pk>/remove/', views.remove_contact_from_group, name='remove_contact_from_group'),
    path('groups/<int:pk>/search/', views.search_group_contacts, name='search_group_contacts'),
    path('groups/<int:pk>/delete-contacts/', views.delete_group_contacts, name='delete_group_contacts'),
    path('groups/<int:pk>/contact-ids/', views.get_group_contact_ids, name='get_group_contact_ids'),
]
