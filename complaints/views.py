from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.http import require_POST
from .models import Complaint

from functools import wraps

def staff_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, "Only staff can do this.")
            return redirect("home")
        return view(request, *args, **kwargs)
    return wrapper

CATEGORIES = [
    {"name": "Mess / Food", "emoji": "🍽️", "desc": "Food, Hygiene, Menu"},
    {"name": "Electricity", "emoji": "💡", "desc": "Light, Fan, Power Cut"},
    {"name": "Hostel / Room", "emoji": "🛏️", "desc": "Bed, Washroom, Cleaning"},
    {"name": "Wi-Fi / IT", "emoji": "📶", "desc": "Internet, Login Issue"},
    {"name": "Water", "emoji": "💧", "desc": "RO, Geyser, Leakage"},
    {"name": "Academics", "emoji": "📚", "desc": "Faculty, Timetable, Exam"},
    {"name": "Transport / Bus", "emoji": "🚌", "desc": "Bus Timing, Route"},
    {"name": "Others", "emoji": "📝", "desc": "Anything ..."},
]

def login_view(request):
    if request.method == "POST":
        email = request.POST["email"].strip()
        pw = request.POST["password"].strip()
        if not email.endswith("@bennett.edu.in"):
            messages.error(request, "Only login with Bennett id @bennett.edu.in")
        elif len(pw) < 3:
            messages.error(request, "Password daalo.")
        else:
            user = authenticate(request, username=email, password=pw)
            if user:
                login(request, user)
                return redirect("home")
            messages.error(request, "Invalid credentials")
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def home(request):
    cat = request.GET.get("category", "All")
    q = request.GET.get("q", "").strip()
    qs = Complaint.objects.all().order_by("-created")
    if cat != "All":
        qs = qs.filter(category=cat)
    if q:
        cond = Q(title__icontains=q)
        digits = "".join(ch for ch in q if ch.isdigit())
        if digits:
            cond |= Q(pk=int(digits) - 1020)   # QUICO-1023 -> pk 3
        qs = qs.filter(cond)
    return render(request, "index.html", {
        "categories": CATEGORIES, "complaints": qs, "current": cat,
        "total": Complaint.objects.count(),
        "pending": Complaint.objects.exclude(status="Resolved").count(),
        "resolved": Complaint.objects.filter(status="Resolved").count(),
        "username": request.user.email.split("@")[0],
    })

@login_required
@require_POST
def submit_complaint(request):
    p = request.POST
    if not all([p["name"].strip(), p["enroll"].strip(), p["title"].strip(), p["desc"].strip()]):
        messages.error(request, "Please fill Name, Enrollment, Title and details.")
        return redirect("home")
    c = Complaint.objects.create(
        name=p["name"], enroll=p["enroll"], category=p["category"],
        urgency=p["urgency"], block=p["block"], room=p["room"],
        title=p["title"], desc=p["desc"], photo=request.FILES.get("photo", ""))
    messages.success(request, f"Complaint Submitted! Your Id is: {c.code}")
    return redirect("home")

@login_required
@require_POST
@staff_required
def change_status(request, pk, status):
    if status not in ("Pending", "InProgress", "Resolved"):
        return redirect("home")
    c = get_object_or_404(Complaint, pk=pk)
    c.status = status
    c.save()
    return redirect("home")

@login_required
@require_POST
@staff_required
def delete_complaint(request, pk):
    get_object_or_404(Complaint, pk=pk).delete()
    return redirect("home")