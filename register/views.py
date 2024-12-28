from django.shortcuts import render, redirect
from django.contrib import messages
from register.models import Users


def registerAction(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        email = request.POST.get('email')
        raw_password = request.POST.get('password')
        age = request.POST.get("age")
        
        if Users.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('register')
        
        user = Users(username=name, email=email, age=age)
        user.set_password(raw_password)
        user.save()
        request.session['user1_id'] = user.id
        return redirect('/login')
    
    return render(request, 'register.html')
