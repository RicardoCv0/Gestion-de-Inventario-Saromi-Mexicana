from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import GemstoneForm, EntryForm, ExitForm, AdjustmentForm

from .models import Gemstone

def index(request):
    gemstones_list = Gemstone.objects.order_by("name")    

    if len(gemstones_list) == 0: return render(request, "inventory/index.html")

    context = {
        "gemstones_list": gemstones_list,
    }

    return render(request, "inventory/index.html", context)

def gemstone_details(request, gemstone_id):
    gemstone = get_object_or_404(Gemstone, pk=gemstone_id)

    context = {
        "gemstone": gemstone,
    }

    return render(request, "inventory/gemstone_details.html", context)

# Gemstones Crud
def create_gemstone(request):
    if request.method == "POST":
        form = GemstoneForm(request.POST)
        
        if form.is_valid():
            if len(form.cleaned_data["id"]) == 5: form.save()
        
        return redirect("index")

    return render(request, "inventory/gemstone_create.html")

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


def delete_gemstone(request, gemstone_id):
    gemstone = get_object_or_404(Gemstone, pk=gemstone_id)
    gemstone.delete()

    return redirect("index")

# Gemstones Movement
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