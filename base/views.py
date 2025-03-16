from django.shortcuts import render, redirect
from django.http import HttpResponse
from base.models import Notes, NoteType
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# Home page
def home(request):
    return render(request, 'index.html')

# View notes of the logged-in user
@login_required
def views_note(request):
    # Fetch only the notes that belong to the logged-in user
    note = Notes.objects.filter(user=request.user)
    note_type = NoteType.objects.all()
    return render(request, 'views_note.html', context={'Notes': note, 'Notetype': note_type})

# Create a new note for the logged-in user
@login_required
def create_note(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        file = request.FILES.get('file')
        type = request.POST.get('type')
        deadline_at = request.POST.get('deadline_at')
        type_id = NoteType.objects.get(id=type)
        
        # Create the note and associate it with the logged-in user
        Notes.objects.create(
            name=name,
            description=description,
            file=file,
            type=type_id,
            deadline_at=deadline_at,
            user=request.user  # Link the note to the logged-in user
        )
        return redirect('views_note')
    
    note_types = NoteType.objects.all()
    return render(request, 'create_notes.html', context={'NoteType': note_types})

# Create a new note type (for categorizing notes)
@login_required
def create_notetype(request):
    if request.method == 'POST':
        name = request.POST.get('note-type')
        NoteType.objects.create(name=name)
        return redirect('view_notetype')
        
    return render(request, 'create_notetype.html')

# View all note types
@login_required
def view_notetype(request):
    note_type = NoteType.objects.all()
    return render(request, 'view_notetype.html', context={'NoteType': note_type})

# Edit a note, only if it belongs to the logged-in user
@login_required
def edit_note(request, pk):
    note_obj = Notes.objects.get(id=pk, user=request.user)  # Fetch the note only if it belongs to the logged-in user
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        file = request.FILES.get('file')
        type = request.POST.get('type')
        deadline_at = request.POST.get('deadline_at')
        type_id = NoteType.objects.get(id=type)
        
        note_obj.name = name
        note_obj.description = description
        note_obj.file = file if file else note_obj.file  # Only update the file if a new one is provided
        note_obj.type = type_id
        note_obj.deadline_at = deadline_at
        note_obj.save()
        return redirect('views_note')
    
    notetype_objs = NoteType.objects.all()
    return render(request, 'edit_note.html', context={'Note': note_obj, 'NoteType': notetype_objs})

# Delete a note, only if it belongs to the logged-in user
@login_required
def delete_note(request, pk):
    note_obj = Notes.objects.get(id=pk, user=request.user)  # Ensure the note belongs to the logged-in user
    note_obj.delete()
    return redirect('views_note')

# Edit a note type
@login_required
def edit_notetype(request, pk):
    notetype_obj = NoteType.objects.get(id=pk)
    if request.method == 'POST':
        name = request.POST.get('note-type')
        notetype_obj.name = name
        notetype_obj.save()
        return redirect('view_notetype')
    
    return render(request, 'edit_notetype.html', context={'NoteType': notetype_obj})

# Delete a note type
@login_required
def delete_notetype(request, pk):
    note_type = NoteType.objects.get(id=pk)
    note_type.delete()
    return redirect('view_notetype')

# User login
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("views_note")  # Ensure you redirect to a logged-in page
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")


# User registration
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Basic validation
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
        elif password1 != password2:
            messages.error(request, "Passwords do not match.")
        elif len(password1) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
        else:
            # Create user
            user = User.objects.create(
                username=username, email=email, password=make_password(password1)
            )
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect("login")

    return render(request, "register.html")

# User logout
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")  # Ensure the logout view redirects to the login page after logout

