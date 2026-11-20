from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.http import require_POST
from .models import Complaint
from .utils import validate_complaint, clean_name, capitalize_first, build_stats, first_urgent_pending
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
    errors = validate_complaint(p, [c["name"] for c in CATEGORIES])
    if errors:
        for e in errors:
            messages.error(request, e)
        return redirect("home")
    c = Complaint.objects.create(
        name=clean_name(p["name"]),
        enroll=p["enroll"].strip().upper(),
        category=p["category"],
        urgency=p["urgency"],
        block=p.get("block", "").strip().upper(),
        room=p.get("room", "").strip(),
        title=capitalize_first(p["title"]),
        desc=p["desc"].strip(),
        photo=request.FILES.get("photo", ""))
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

@login_required
def stats_view(request):
    complaints = Complaint.objects.order_by("created")
    data = build_stats(complaints)
    data["urgent"] = first_urgent_pending(complaints)
    return render(request, "stats.html", data)