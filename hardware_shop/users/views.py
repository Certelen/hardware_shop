from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
    pass


@login_required
def orders(request):
    pass


@login_required
def cart(request):
    pass


@login_required
def favorite(request):
    pass
