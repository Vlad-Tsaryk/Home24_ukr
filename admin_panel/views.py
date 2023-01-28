from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'admin_panel/statistic.html')


def error_404(request, exception):
    return render(request, 'admin_panel/error_404.html')


def error_403(request, exception):
    return render(request, 'admin_panel/error_403.html')
