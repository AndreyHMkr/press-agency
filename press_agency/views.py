from django.contrib.auth import views as auth_views, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from press_agency.forms import (
    NewspaperForm,
    LoginForm,
    RegistrationForm,
    AuthorProfileForm,
    NewspaperDetailsForm, NewspaperSearchForm,
)
from press_agency.models import Topic, Redactor, Newspaper


def index(request: HttpRequest) -> HttpResponse:
    search_form = NewspaperSearchForm(request.GET)
    if search_form.is_valid():
        title = search_form.cleaned_data["title"]
        if title:
            return redirect(f"{reverse('newspaper-list')}?title={title}")
    number_of_topic = Topic.objects.all().count()
    number_of_redactors = Redactor.objects.all().count()
    number_of_newspapers = Newspaper.objects.all().count()
    context = {
        "search_form": search_form,
        "number_of_topic": number_of_topic,
        "number_of_redactors": number_of_redactors,
        "number_of_newspapers": number_of_newspapers,
    }
    return render(request, "pages/index.html", context=context)


class NewspaperAddTopic(LoginRequiredMixin, generic.CreateView):
    model = Topic
    form_class = NewspaperForm
    template_name = "pages/newspaper-topic.html"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


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


class AuthorProfile(LoginRequiredMixin, generic.UpdateView):
    model = Redactor
    form_class = AuthorProfileForm
    template_name = "pages/author-profile.html"
    success_url = reverse_lazy("index")

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.instance.username = self.request.user.username
        form.instance.pk = self.request.user.pk
        return super().form_valid(form)

    def get_initial(self):
        return {
            "pen_name": self.request.user.username,
        }


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

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.GET.get("title")
        if title:
            queryset = queryset.filter(Q(title__icontains=title) | Q(content__icontains=title))
        return queryset

    def get_context_data(self, **kwargs):
        title = self.request.GET.get("title", "")
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("title", "")
        return context
