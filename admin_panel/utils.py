from .models import Fruit


def get_count_apple():
    return Fruit.objects.get(pk=1).count()
