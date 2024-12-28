from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from httpcore import request
from register.models import Users
from .models import Report
import pandas as pd

def clear_history(request):
    if 'user_messages' in request.session:
        del request.session['response_history']
    if 'messages' in request.session:
        del request.session['messages']
    
    


# def loginAction(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")

#         # Connect to the MySQL database
#         m = sql.connect(host="localhost", user="root", password="", database='newsAuthenticator')
#         cursor = m.cursor()

#         # Execute SQL query to select user based on username and password
#         cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))

#         # Fetch results
#         user = cursor.fetchone()

#         if user is not None:
#             # Successful authentication
#             # Clear history before logging in
#             clear_history(request)

#         if user is not None:
#             # Successful authentication
#             # Store username in session
#             request.session['username'] = username
#             # Redirect to the welcome page
#             return HttpResponseRedirect(reverse('welcome'))
#         else:
#             # Authentication failed, render error template
#             return render(request, 'login.html')

#     return render(request, 'login.html')


def loginAction(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        raw_password = request.POST.get('password')

        try:
            user = Users.objects.get(email=email)
            print("1")
        except Users.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
            print("2")
            return redirect('/login')

        if user.check_password(raw_password):
            print("Password check passed")  # Debugging line
            auth_login(request, user)
            request.session['user_id'] = user.id

            request.session['user_messages'] = []
            request.session['response_history'] = []
            request.session['messages'] = []

            if user.is_superUser == "admin":
                return redirect('/admin_panel')  # Redirect to admin home if user is admin
            else:
                return redirect('/index')  # Redirect to home if user is not admin
        else:
            print("noo")
            messages.error(request, 'Invalid email or password.')
            return redirect('/login')

    return render(request, 'login.html')

from django.contrib.auth import get_user_model

def index(request):
    user = None
    user_id = request.session.get('user_id')
    print(user_id)

    # Check if user_id exists in the session, fetch the user if logged in
    if user_id:
        try:
            user = Users.objects.get(id=user_id)
            print(user)
        except get_user_model().DoesNotExist:
            user = None

    # Render different content depending on whether the user is logged in or not
    return render(request, 'index.html', {
        'username': user.username if user else None  # Pass username if the user is logged in, else None
    })


def logout(request):
    # Perform the logout operation
    auth_logout(request)
    
    # Optionally, add a message to indicate successful logout
    messages.success(request, 'You have successfully logged out.')

    # Redirect to the login page or home page after logout
    return redirect('/index')  # Change 'login' to the name of your login view or homepage

def report(request):
    if request.method == 'POST':
        # Extract data from the form
        reporter_name = request.POST.get('reporter_name')
        reporter_email = request.POST.get('reporter_email')
        reporter_ph = request.POST.get('reporter_ph')
        news_title = request.POST.get('news_title')
        news_description = request.POST.get('news_description')
        news_url = request.POST.get('news_url')

        # You can perform any validation or processing here
        if reporter_name and reporter_email and news_description:
            # Create a new report entry in the database
            new_report = Report(
                reporter_name=reporter_name,
                reporter_email=reporter_email,
                reporter_ph=reporter_ph,
                news_title=news_title,
                news_description=news_description,
                news_url=news_url
            )
            new_report.save()  # Save the report to the database

            messages.success(request, 'Your report has been submitted successfully!')
            return redirect('report')  # Redirect to the report page or another page
        else:
            messages.error(request, 'Please fill in all required fields.')
    return render(request, 'report.html') 

def admin_panel(request):
    # Fetch all reports from the database
    reports = Report.objects.all()

    # Render the admin panel template with the reports
    return render(request, 'admin_panel.html', {'reports': reports})

from django.shortcuts import redirect
from django.contrib import messages
from .models import Report  # Adjust according to your project structure

def delete_report(request, report_id):
    if request.method == 'POST':
        # Use get_object_or_404 to simplify the logic
        try:
            report = Report.objects.get(id=report_id)  # Now it's safe to get the report
            report.delete()
            messages.success(request, 'Report deleted successfully.')
        except Report.DoesNotExist:
            messages.error(request, 'Report not found.')
        
        return redirect('admin_panel')  # Ensure you always return an HttpResponse
    
    # Handle non-POST requests
    messages.error(request, 'Invalid request method.')
    return redirect('admin_panel')  # Redirect if method is not POST


import pandas as pd
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Report

def append_report_to_csv(request, report_id):
    if request.method == 'POST':
        # Get the title and text from the form
        report_title = request.POST.get('report_title')
        report_text = request.POST.get('report_text')

        # Call the function to append the report to the CSV
        append_to_csv(report_title, report_text)

        delete_report_from_db(report_id)

        messages.success(request, 'Report updated successfully.')
        return redirect('admin_panel')  # Redirect to your admin panel after editing

    messages.error(request, 'Invalid request method.')
    return redirect('admin_panel')

def append_to_csv(title, text):
    # Read the existing CSV file
    csv_filepath = "C:/Users/abinv/OneDrive/Desktop/PROJECTS/VeriNews/Datasets/fake_or_real_news.csv"
    df = pd.read_csv(csv_filepath)

    # Create a new DataFrame for the report
    new_report = pd.DataFrame({
        'title': [title],
        'text': [text],
        'label': "REAL"
    })

    # Append the new report to the existing DataFrame
    df = pd.concat([df, new_report], ignore_index=True)

    # Write the updated DataFrame back to the CSV file
    df.to_csv(csv_filepath, index=False)

def delete_report_from_db(report_id):
    # Check if report exists and delete it
    if Report.objects.filter(id=report_id).exists():
        report = Report.objects.get(id=report_id)
        report.delete()
    else:
        messages.error(request, 'Report not found.')
