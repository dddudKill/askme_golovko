from django.core.paginator import Paginator, EmptyPage, InvalidPage


def paginate(request, model, num_per_page=10):
    paginator = Paginator(model, num_per_page)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        content = paginator.page(page)
    except (EmptyPage, InvalidPage):
        content = paginator.page(paginator.num_pages)
    scope_min_page = int(page) - 2
    scope_max_page = int(page) + 2

    context = {
        'content': content,
        'scope_min_page': scope_min_page,
        'scope_max_page': scope_max_page,
        'end_page': paginator.num_pages
    }
    return context
