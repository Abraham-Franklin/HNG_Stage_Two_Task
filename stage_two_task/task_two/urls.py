from django.urls import path
from .views import RegisterView, LoginView, UserDetailView, UserOrganisationsView, OrganisationDetailView, CreateOrganisationView, AddUserToOrganisationView

urlpatterns = [
    path('auth/register', RegisterView.as_view(), name='register'),
    path('auth/login', LoginView.as_view(), name='login'),
    path('api/users/<str:id>', UserDetailView.as_view(), name='user-detail'),
    path('api/organisations', UserOrganisationsView.as_view(), name='organisations'),
    path('api/organisations/<str:orgId>', OrganisationDetailView.as_view(), name='organisation-detail'),
    path('api/organisations', CreateOrganisationView.as_view(), name='create-organisation'),
    path('api/organisations/<str:orgId>/users', AddUserToOrganisationView.as_view(), name='add-user-to-organisation'),
]
