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
    min_page = int(page) - 2
    max_page = int(page) + 2

    context = {
        'content': content,
        'min_page': min_page,
        'max_page': max_page,
        'end_page': paginator.num_pages
    }
    return context
