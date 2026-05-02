from datetime import datetime
from django.core.exceptions import ValidationError

def max_year():
    return datetime.now().year + 1


def validate_year_range(start, end):
    if start is None or end is None:
        return

    if start >= end:
        raise ValidationError({
            'endYear': 'Endjahr muss grösser als Startjahr sein.'
        })

    if (start + 1) != end:
        raise ValidationError({
            'endYear': 'Start- und Endjahr müssen ein Jahr auseinander liegen.'
        })