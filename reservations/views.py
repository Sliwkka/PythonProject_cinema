from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
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
            name=name,
            email=email,
            seats=seats
        )

        screening.available_seats -= seats
        screening.save()

        return render(request, 'reservations/reservations.html', {'screening': screening})

    return render(request, 'reservations/screening_detail.html', {'screening': screening})
