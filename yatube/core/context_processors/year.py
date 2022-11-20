from datetime import datetime as dt


def year(request):
    """Добавляет переменную с текущим годом."""
    return {'year': dt.now().year}
