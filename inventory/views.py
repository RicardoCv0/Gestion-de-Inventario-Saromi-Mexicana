from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hi!!, This is the inventory dashboard")

# Gemstones Crud
def add_gemstone(request):
    return HttpResponse("Hellope!!, You are adding a new gemstone type")

def edit_gemstone(request, gemstone_id):
    return HttpResponse("Howdy!!, You are editing the data for the %s gemstone" % gemstone_id)

def delete_gemstone(request, gemstone_id):
    return HttpResponse("Oi!!, You are you are deleting the %s gemstone" % gemstone_id)

# Gemstones Movement
def entry_movement(request, gemstone_id):
    return HttpResponse("Hellope!!, You are you are adding to the %s gemstone" % gemstone_id)

def adjustment_movement(request, gemstone_id):
    return HttpResponse("Howdy!!, You are you are adjusting the %s gemstone" % gemstone_id)

def exit_movement(request, gemstone_id):
    return HttpResponse("Oi!!, You are you are removing from the %s gemstone" % gemstone_id)
