from django.urls import path
from press_agency import views

urlpatterns = [
    path("", views.index, name="index"),
    path("author-profile/", views.AuthorProfile.as_view(), name="author-profile"),
    path(
        "newspaper-details/", views.NewspaperDetails.as_view(), name="newspaper-details"
    ),
    path("newspaper-topic/", views.NewspaperAddTopic.as_view(), name="newspaper-topic"),
    path("newspaper-list/", views.NewspaperList.as_view(), name="newspaper-list"),
    path("topic-list/", views.TopicList.as_view(), name="topic-list"),
    path("contact-us/", views.contact_us, name="contact-us"),
    path("about-us/", views.about_us, name="about-us"),
    # Authentication
    path("accounts/login/", views.UserLoginView.as_view(), name="login"),
    path("accounts/logout/", views.user_logout_view, name="logout"),
    path("accounts/register/", views.registration, name="register"),
]
