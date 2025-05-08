from django.contrib.auth import views as auth_views, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from press_agency.forms import (
    NewspaperForm,
    LoginForm,
    RegistrationForm,
    AuthorProfileForm,
    NewspaperDetailsForm,
)
from press_agency.models import Topic, Redactor, Newspaper


def index(request: HttpRequest) -> HttpResponse:
    number_of_topic = Topic.objects.all().count()
    number_of_redactors = Redactor.objects.all().count()
    number_of_newspapers = Newspaper.objects.all().count()
    context = {
        "number_of_topic": number_of_topic,
        "number_of_redactors": number_of_redactors,
        "number_of_newspapers": number_of_newspapers,
    }
    return render(request, "pages/index.html", context=context)


def contact_us(request):
    return render(request, "pages/contact-us.html")


def about_us(request):
    redactors = Redactor.objects.all()
    return render(request, "pages/about-us.html", {"redactors": redactors})


def registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            print("Account created successfully!")
            return redirect("/accounts/login/")
        else:
            print("Registration failed!")
    else:
        form = RegistrationForm()

    context = {"form": form}
    return render(request, "accounts/sign-up.html", context)


class UserLoginView(auth_views.LoginView):
    template_name = "accounts/sign-in.html"
    form_class = LoginForm

    def get_success_url(self):
        return reverse_lazy("index")


def user_logout_view(request):
    logout(request)
    return redirect("/accounts/login/")


class AuthorProfile(generic.CreateView):
    model = Redactor
    form_class = AuthorProfileForm
    template_name = "pages/author-profile.html"
    success_url = reverse_lazy("index")


class RedactorDetailsView(generic.DetailView):
    model = Redactor
    queryset = Redactor.objects.all()


class NewspaperDetails(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    template_name = "pages/newspaper-details.html"
    form_class = NewspaperDetailsForm
    success_url = reverse_lazy("index")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        last = Topic.objects.filter(owner=self.request.user).order_by("-pk").first()
        if last:
            initial["topic"] = last.pk
        return initial

    def form_valid(self, form):
        form.instance.publisher = self.request.user
        return super().form_valid(form)


class TopicList(generic.ListView):
    model = Topic
    template_name = "pages/topic-list.html"
    context_object_name = "topics"

    def get_queryset(self):
        qs = Topic.objects.annotate(publications=Count("newspaper"))
        return qs


class NewspaperList(generic.ListView):
    model = Newspaper
    template_name = "pages/newspaper-list.html"
    fields = ["title", "content", "published_date", "topic", "publisher"]
    context_object_name = "newspapers"
    success_url = reverse_lazy("newspaper-list")


class NewspaperAddTopic(LoginRequiredMixin, generic.CreateView):
    model = Topic
    form_class = NewspaperForm
    template_name = "pages/newspaper-topic.html"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
