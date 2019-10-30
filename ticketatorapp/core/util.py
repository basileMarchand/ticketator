from django import template
from django.conf import settings
from django.core.exceptions import FieldError
register = template.Library()


@register.filter
def abssub(value, arg):
    try:
        return abs(value - arg)
    except:
        return 'error'


def paginate(queryset, page, limit=settings.PAGINATE_BY):
    start = int((page - 1) * limit)
    end = int((page * limit))
    page_count = int(queryset.count() / limit)
    queryset = queryset[start:end]
    return queryset, {
        'page': page,
        'page_count': page_count,
        'last_page': page_count + 1,
        'pages': range(1, page_count + 2),
    }


def query_view(
        model, params, order_by='-id', granted_queues=None,
        limit=settings.PAGINATE_BY, **kwargs):
    params = {key: value for key, value in params.items() if value}
    params.update({key: value for key, value in kwargs.items() if value})
    try:
        page = int(params.pop('page', 1))
    except ValueError:
        page = 1

    try:
        queryset = model.objects.filter(**params).filter(
            granted_queues).order_by(order_by)
    except FieldError:
        return {}

    data, pagination = paginate(queryset, page, limit)

    return {
        'data': data,
        'pagination': pagination,
        'query': '&'.join(['%s=%s' % (key, value)
                           for key, value in params.items()])
    }
