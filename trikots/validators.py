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

def validate_match_home_away_club(home_club_id, away_club_id):
    if home_club_id is None or away_club_id is None:
        return

    if home_club_id == away_club_id:
        raise ValidationError({
            'away_club': 'Heim- und Auswärtsteam müssen unterschiedlich sein.'
        })
