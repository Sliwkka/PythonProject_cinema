from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Movie, Screening, Reservation


def movie_list(request):
    movies = Movie.objects.all()
    title_filter = request.GET.get('title')
    if title_filter:
        movies = movies.filter(title__icontains=title_filter)
    return render(request, 'reservations/movie_list.html', {'movies': movies})


def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    screenings = Screening.objects.filter(movie=movie)
    date_filter = request.GET.get('date')
    if date_filter:
        screenings = screenings.filter(date=date_filter)
    return render(request, 'reservations/movie_detail.html', {'movie': movie, 'screenings': screenings})

@login_required
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
            return redirect('movie_list')
    else:
        form = UserCreationForm()
    return render(request, 'reservations/registration.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('movie_list')
    else:
        form = AuthenticationForm()
    return render(request, 'reservations/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('movie_list')


@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    movie_filter = request.GET.get('movie')
    if movie_filter:
        reservations = reservations.filter(screening__movie__title__icontains=movie_filter)
    return render(request, 'reservations/my_reservations.html', {'reservations': reservations})

@login_required
def delete_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    if request.method == 'POST':
        reservation.screening.available_seats += reservation.seats
        reservation.screening.save()
        reservation.delete()
        return redirect('my_reservations')
    return render(request, 'reservations/delete_reservation.html', {'reservation': reservation})