import datetime


def filter_date(
    queryset,
    start=None,
    end=None,
    format="%Y-%m-%d %H:%M",
    kind=0,
    attr="time",
):
    if start:
        start = datetime.datetime.strptime(start, format)
        if kind == 1:
            start = start.date()
            attr += "__date"
        elif kind == 2:
            start = start.time()
            attr += "__time"

        queryset = queryset.filter(**{attr + "__gte": start})

    if end:
        end = datetime.datetime.strptime(end, format)
        if kind == 1:
            end = end.date()
            attr += "__date"
        elif kind == 2:
            end = end.time()
            attr += "__time"

        queryset = queryset.filter(**{attr + "__lte": end})

    return queryset
