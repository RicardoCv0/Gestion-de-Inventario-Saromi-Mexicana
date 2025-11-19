from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import GemstoneForm, EntryForm, ExitForm, AdjustmentForm
from django.contrib.auth.decorators import login_required
from users.decorators import roles_required
from .models import Gemstone
from django.core.paginator import Paginator
from django.db.models import Q

@login_required
@roles_required(["supervisor", "gerente", "asistente"])
def index(request):
    gemstones_list = Gemstone.objects.order_by("name")    

    if len(gemstones_list) == 0: return render(request, "inventory/index.html")

    context = {
        "gemstones_list": gemstones_list,
    }

    return render(request, "inventory/index.html", context)

@login_required
@roles_required(["supervisor", "gerente", "asistente"])
def gemstone_details(request, gemstone_id):
    gemstone = get_object_or_404(Gemstone, pk=gemstone_id)

    context = {
        "gemstone": gemstone,
    }

    return render(request, "inventory/gemstone_details.html", context)

# Gemstones Crud

@login_required
@roles_required(["gerente"])
def create_gemstone(request):
    if request.method == "POST":
        form = GemstoneForm(request.POST)
        
        if form.is_valid():
            if len(form.cleaned_data["id"]) == 5: form.save()
        
        return redirect("index")

    return render(request, "inventory/gemstone_create.html")

@login_required
@roles_required(["gerente"])
def edit_gemstone(request, gemstone_id):
    gemstone = get_object_or_404(Gemstone, pk=gemstone_id)
    
    if request.method == "POST":
        form = GemstoneForm(request.POST, instance=gemstone)

        if form.is_valid():
            form.save()
        
        return redirect("index")

    context = {
        "gemstone": gemstone,
    }

    return render(request, "inventory/gemstone_edit.html", context)

@login_required
@roles_required(["gerente"])
def delete_gemstone(request, gemstone_id):
    gemstone = get_object_or_404(Gemstone, pk=gemstone_id)
    gemstone.delete()

    return redirect("index")

# Gemstones Movement

@login_required
@roles_required(["surtidor", "gerente"])
def entry_movement(request, gemstone_id):
    gemstone = get_object_or_404(Gemstone, pk=gemstone_id)

    context = {
        "gemstone": gemstone,
    }

    if request.method == "POST":
        form = EntryForm(request.POST)
        
        if not form.is_valid(): return redirect("index")

        ammount = form.cleaned_data["ammount"]
        if ammount < 0: return redirect("index")

        gemstone.ammount_available += ammount
        gemstone.save()

        return render(request, "inventory/gemstone_details.html", context)


    return render(request, "inventory/entry_movement.html", context)

@login_required
@roles_required(["surtidor", "gerente", "asistente"])
def adjustment_movement(request, gemstone_id):
    gemstone = get_object_or_404(Gemstone, pk=gemstone_id)

    context = {
        "gemstone": gemstone,
    }
    
    if request.method == "POST":
        form = EntryForm(request.POST)
        
        if not form.is_valid(): return redirect("index")

        ammount = form.cleaned_data["ammount"]

        if ammount < 0: return redirect("index")

        gemstone.ammount_available = ammount
        gemstone.save()

        return render(request, "inventory/gemstone_details.html", context)

    return render(request, "inventory/adjustment_movement.html", context)

@login_required
@roles_required(["surtidor", "gerente"])
def exit_movement(request, gemstone_id):
    gemstone = get_object_or_404(Gemstone, pk=gemstone_id)

    context = {
        "gemstone": gemstone,
    }

    if request.method == "POST":
        form = EntryForm(request.POST)
        
        if not form.is_valid(): return redirect("index")

        ammount = form.cleaned_data["ammount"]

        if ammount < 0 or ammount > gemstone.ammount_available: return redirect("index")

        gemstone.ammount_available -= ammount
        gemstone.save()

        return render(request, "inventory/gemstone_details.html", context)

    return render(request, "inventory/exit_movement.html", context)

@login_required
def dashboard(request):
    profile = request.user.userprofile
    role = profile.role

    # --- FILTROS Y BÚSQUEDA ---
    search_query = request.GET.get("search", "")
    filter_type = request.GET.get("type", "")

    gemstones = Gemstone.objects.all()

    # Búsqueda por nombre
    if search_query:
        gemstones = gemstones.filter(name__icontains=search_query)

    # Filtro por tipo
    if filter_type:
        gemstones = gemstones.filter(type__icontains=filter_type)

    # --- PAGINACIÓN ---
    paginator = Paginator(gemstones, 10)  # 10 por página
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Estadísticas
    context = {
        "role": role,
        "is_gerente": role == "gerente",
        "is_supervisor": role == "supervisor",
        "is_surtidor": role == "surtidor",
        "is_asistente": role == "asistente",
        "is_contador": role == "contador",

        "page_obj": page_obj,
        "gemstones": gemstones,
        "total_materiales": gemstones.count(),
        "total_existencias": sum(g.ammount_available for g in gemstones),
        "bajo_stock": gemstones.filter(ammount_available__lt=10).count(),

        # para búsqueda
        "search_query": search_query,
        "filter_type": filter_type,
    }

    return render(request, "inventory/dashboard.html", context)