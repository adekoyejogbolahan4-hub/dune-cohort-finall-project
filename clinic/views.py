from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.contrib import messages
from .models import Doctor, Service, Specialisation
from .forms import DoctorForm, RegisterForm


def is_staff(user):
    return user.is_staff


# ── Public Views ──────────────────────────────────────────────────────────────

def home(request):
    doctors = Doctor.objects.filter(is_available=True).select_related('specialisation')[:4]
    services = Service.objects.filter(is_active=True)[:6]
    context = {
        'doctors': doctors,
        'services': services,
        'doctor_count': Doctor.objects.filter(is_available=True).count(),
        'service_count': Service.objects.filter(is_active=True).count(),
    }
    return render(request, 'clinic/home.html', context)


def doctor_list(request):
    specialisation_id = request.GET.get('specialisation')
    doctors = Doctor.objects.filter(is_available=True).select_related('specialisation')
    if specialisation_id:
        doctors = doctors.filter(specialisation_id=specialisation_id)
    specialisations = Specialisation.objects.all()
    return render(request, 'clinic/doctor_list.html', {
        'doctors': doctors,
        'specialisations': specialisations,
        'selected': specialisation_id,
    })


def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    return render(request, 'clinic/doctor_detail.html', {'doctor': doctor})


def service_list(request):
    services = Service.objects.filter(is_active=True)
    return render(request, 'clinic/service_list.html', {'services': services})


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}! Your account has been created.')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'clinic/register.html', {'form': form})


# ── Staff-Only Doctor CRUD ────────────────────────────────────────────────────

@login_required
@user_passes_test(is_staff)
def doctor_create(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES)
        if form.is_valid():
            doctor = form.save()
            messages.success(request, f'{doctor} has been added successfully.')
            return redirect('doctor_detail', pk=doctor.pk)
    else:
        form = DoctorForm()
    return render(request, 'clinic/doctor_form.html', {'form': form, 'action': 'Add'})


@login_required
@user_passes_test(is_staff)
def doctor_update(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, f'{doctor} has been updated successfully.')
            return redirect('doctor_detail', pk=doctor.pk)
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'clinic/doctor_form.html', {'form': form, 'action': 'Edit', 'doctor': doctor})


@login_required
@user_passes_test(is_staff)
def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        name = str(doctor)
        doctor.delete()
        messages.success(request, f'{name} has been removed from the system.')
        return redirect('doctor_list')
    return render(request, 'clinic/doctor_confirm_delete.html', {'doctor': doctor})


# ── Auth-protected pages ──────────────────────────────────────────────────────

@login_required
def dashboard(request):
    from appointments.models import Appointment
    user_appointments = Appointment.objects.filter(
        patient=request.user
    ).select_related('doctor', 'service').order_by('-appointment_date')
    return render(request, 'clinic/dashboard.html', {'appointments': user_appointments})
