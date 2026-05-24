from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Screening, Reservation


def screening_list(request):
    screenings = Screening.objects.all()

    movie_filter = request.GET.get('movie')
    date_filter = request.GET.get('date')

    if movie_filter:
        screenings = screenings.filter(movie__title__icontains=movie_filter)

    if date_filter:
        screenings = screenings.filter(date=date_filter)

    return render(request, 'reservations/screening_list.html', {'screenings': screenings})


def screening_detail(request, pk):
    screening = get_object_or_404(Screening, pk=pk)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        seats = int(request.POST.get('seats'))

        Reservation.objects.create(
            screening=screening,
            user=request.user if request.user.is_authenticated else None,
            name=name,
            email=email,
            seats=seats
        )

        screening.available_seats -= seats
        screening.save()

        return render(request, 'reservations/reservations.html', {'screening': screening})

    return render(request, 'reservations/screening_detail.html', {'screening': screening})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('screening_list')
    else:
        form = UserCreationForm()

    return render(request, 'reservations/registration.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('screening_list')
    else:
        form = AuthenticationForm()

    return render(request, 'reservations/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('screening_list')


@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'reservations/my_reservations.html', {'reservations': reservations})