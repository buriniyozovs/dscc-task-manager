from django.utils import timezone

from .models import Category, Task


def sidebar_context(request):
    if not request.user.is_authenticated:
        return {}

    categories = Category.objects.filter(user=request.user).order_by('name')
    tasks = Task.objects.filter(user=request.user)
    total = tasks.count()
    completed = tasks.filter(status=Task.Status.COMPLETED).count()
    rate = round((completed / total * 100) if total else 0)
    upcoming = list(
        tasks.exclude(status=Task.Status.COMPLETED)
        .filter(deadline__gte=timezone.now())
        .order_by('deadline')[:5]
    )

    url_name = getattr(request.resolver_match, 'url_name', None) if request.resolver_match else None
    active_category_id = None
    try:
        cid = request.GET.get('category')
        if cid and cid.isdigit():
            active_category_id = int(cid)
    except (ValueError, TypeError):
        pass

    return {
        'sidebar_categories': categories,
        'activity_completion_rate': rate,
        'activity_upcoming_deadlines': upcoming,
        'active_page': url_name,
        'active_category_id': active_category_id,
    }
