from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render

from users.models import User
from finance.models import MemberSaving, MeriGoRoundPayment, ChamaFine
from loans.models import Loan, LoanPayment

# Create your views here.
# Create your views here.
################ Authentication URLs ##############
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            return redirect("home")
    return render(request, "accounts/login.html")


def user_logout(request):
    logout(request)
    return redirect("login")


@login_required(login_url="/users/login/")
def members(request):
    members = User.objects.all().order_by("-created")

    if request.method == "POST":
        search_text = request.POST.get("search_text")
        members = User.objects.filter(
            Q(first_name__icontains=search_text)
            | Q(last_name__icontains=search_text)
            | Q(id_number__icontains=search_text)
            | Q(phone_number__icontains=search_text)
        ).order_by("-created")

    paginator = Paginator(members, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj}
    return render(request, "members/members.html", context)


@login_required(login_url="/users/login/")
def member_details(request, member_id=None):
    member = User.objects.get(id=member_id)

    context = {
        "member": member
        # "page_obj": page_obj
    }

    return render(request, "members/member_details.html", context)


@login_required(login_url="/users/login/")
def new_member(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        gender = request.POST.get("gender")
        id_number = request.POST.get("id_number")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("address")
        city = request.POST.get("city")
        country = request.POST.get("country")
        county = request.POST.get("county")

        date_joined = request.POST.get("date_joined")
        role = request.POST.get("role")

        member = User.objects.create(
            username=email,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            id_number=id_number,
            phone_number=phone_number,
            email=email,
            address=address,
            city=city,
            county=county,
            country=country,
            date_joined=date_joined,
            role=role,
        )

        return redirect("members")
    return render(request, "members/new_member.html")


@login_required(login_url="/users/login/")
def edit_member(request):
    if request.method == "POST":
        member_id = request.POST.get("member_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        gender = request.POST.get("gender")
        id_number = request.POST.get("id_number")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("address")
        city = request.POST.get("city")
        county = request.POST.get("county")
        country = request.POST.get("country")
        date_joined = request.POST.get("date_joined")
        role = request.POST.get("role")

        member = User.objects.get(id=member_id)
        member.gender = gender
        member.id_number = id_number
        member.email = email
        member.phone_number = phone_number
        member.address = address
        member.city = city
        member.county = county
        member.country = country
        member.first_name = first_name
        member.last_name = last_name
        member.role = role
        member.date_joined = date_joined
        member.username = email
        member.save()

        return redirect("members")

    return render(request, "members/edit_member.html")


@login_required(login_url="/users/login/")
def delete_member(request):
    if request.method == "POST":
        member_id = request.POST.get("member_id")
        member = User.objects.get(id=member_id)
        member.delete()

        return redirect("members")

    return render(request, "members/delete_member.html")
