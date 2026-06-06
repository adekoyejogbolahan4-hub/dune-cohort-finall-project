from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment
from .forms import AppointmentForm


@login_required
def appointment_book(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.save()
            messages.success(request, 'Your appointment has been booked! We will confirm it shortly.')
            return redirect('appointment_detail', pk=appointment.pk)
    else:
        form = AppointmentForm()
    return render(request, 'appointments/appointment_form.html', {'form': form, 'action': 'Book'})


@login_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, patient=request.user)
    return render(request, 'appointments/appointment_detail.html', {'appointment': appointment})


@login_required
def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, patient=request.user)
    if appointment.status in ('completed', 'cancelled'):
        messages.error(request, 'You cannot edit a completed or cancelled appointment.')
        return redirect('appointment_detail', pk=appointment.pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your appointment has been updated.')
            return redirect('appointment_detail', pk=appointment.pk)
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'appointments/appointment_form.html', {
        'form': form, 'action': 'Edit', 'appointment': appointment
    })


@login_required
def appointment_cancel(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, patient=request.user)
    if request.method == 'POST':
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, 'Your appointment has been cancelled.')
        return redirect('dashboard')
    return render(request, 'appointments/appointment_confirm_cancel.html', {'appointment': appointment})
