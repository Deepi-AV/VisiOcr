from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from .utils.extract import extract_text
from django.shortcuts import render,redirect
from .models import images
from .forms import ImageForm
from datetime import datetime, timedelta

def home(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save()  # Save the image instance
            extracted_text = extract_text(image_instance.image.path)

            if isinstance(extracted_text, dict):
                # If all necessary fields were found, store and redirect
                request.session['extracted_text'] = extracted_text
                return redirect('visitor_pass')
            else:
                # Show the error message from `final_text`
                return render(request, 'home.html', {
                    'form': form,
                    'error_message': extracted_text  # This will be the error message
                })
    else:
        form = ImageForm()

    return render(request, "home.html", {'form': form})

def generate_pass(request):
    visitor_pass = None
    if request.method == 'POST':
    
        phone_number = request.POST.get('phone_number')

        extracted_text = request.session.get('extracted_text', {})
        
        # Prepare the visitor pass details
        visitor_pass = {
            "name": extracted_text.get("Name", "Unknown"),
            "dob": extracted_text.get("DOB", "Unknown"),
            "phone_number": phone_number,
            "gen_date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),  # Include time in generation date
            "exp_date": (datetime.now() + timedelta(hours=6)).strftime("%d/%m/%Y %H:%M:%S"),  # 6-hour validity
}

    
    return render(request, "visitor_pass.html", {"visitor_pass": visitor_pass})

