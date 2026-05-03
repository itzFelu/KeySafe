from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Note
from .forms import NoteForm


@login_required
def dashboard_view(request):
    notes = Note.objects.filter(user=request.user, is_deleted=False).order_by('-created_at')
    return render(request, 'notes/dashboard.html', {'notes': notes})


@login_required
def add_note_view(request):
    form = NoteForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()

            messages.success(request, "Note created successfully!")
            return redirect('dashboard')

    return render(request, 'notes/note_form.html', {'form': form})


@login_required
def note_detail_view(request, pk):
    note = get_object_or_404(Note, id=pk, user=request.user, is_deleted=False)
    return render(request, 'notes/note_detail.html', {'note': note})


@login_required
def edit_note_view(request, pk):
    note = get_object_or_404(Note, id=pk, user=request.user)

    form = NoteForm(request.POST or None, instance=note)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Note updated successfully!")
            return redirect('note-detail', pk=note.id)

    return render(request, 'notes/note_form.html', {'form': form})


@login_required
def delete_note_view(request, pk):
    note = get_object_or_404(Note, id=pk, user=request.user)

    note.is_deleted = True
    note.save()

    messages.success(request, "Note deleted successfully!")
    return redirect('dashboard')