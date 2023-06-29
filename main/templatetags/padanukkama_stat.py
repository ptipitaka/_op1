from django import template
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db.models import Q, Count
from django.db.models.functions import TruncDate
from django.utils import timezone

import datetime 
from simple_history.models import HistoricalRecords

from padanukkama.models import *

register = template.Library()

# ---------------------
# Padanukkama dashboard
# ---------------------
@register.inclusion_tag('main/statistic/dashboard.html')
def dashboard():
    padanukkama = Padanukkama.objects.all()
    return {'padanukkama': padanukkama}



@register.simple_tag()
def all_padas(padanukkama_id):
    count = Pada.objects.filter(
            Q(padanukkama=padanukkama_id) & Q(children__isnull=True)
        ).count()
    return intcomma(count)



@register.simple_tag()
def all_saddas(padanukkama_id):
    count = Sadda.objects.filter(padanukkama=padanukkama_id).count()
    return intcomma(count)



@register.inclusion_tag('main/statistic/milestone.html')
def milestone(padanukkama_id):
    non_translated = Pada.objects.filter(
            Q(padanukkama=padanukkama_id) & Q(children__isnull=True) & Q(sadda__isnull=True)
        ).count()
    translated = Pada.objects.filter(
            Q(padanukkama=padanukkama_id) & Q(children__isnull=True) & Q(sadda__isnull=False)
        ).count()
    return {
        'nonTranslated': non_translated,
        'translated': translated
        }



@register.inclusion_tag('main/statistic/translation_process.html')
def translation_process(padanukkama_id):
    # Count Sadda objects for each workflow state
    sadda_by_state = Sadda.objects.filter(
        padanukkama_id=padanukkama_id).values('state').annotate(count=Count('state'))
    return {'sadda_by_state': sadda_by_state}



@register.inclusion_tag('main/statistic/monthly_progress.html')
def monthly_progress(padanukkama_id):
    # Get the current date and time
    current_date = datetime.datetime.now().date()

    # Calculate the start and end dates of the current month
    start_date = current_date.replace(day=1)
    end_date = current_date

    # Query the newly added 'Sadda' objects
    # -------------------------------------
    q_newly_added_sadda_summary = (
        Sadda.history
        .filter(
            padanukkama=padanukkama_id,
            history_date__range=(start_date, end_date),
            history_type='+'
        )
        .annotate(date=TruncDate('history_date'))
        .values('date')
        .annotate(new_sadda_count=Count('id'))
        .order_by('date')
    )

    # Create a dictionary to store the date-count pairs
    newly_added_sadda_summary = {item['date']: item['new_sadda_count'] for item in q_newly_added_sadda_summary}

    # Create a list to store the formatted results
    result_of_newly_added_sadda_summary = []

    # Iterate over each date in the current month
    date_cursor = start_date
    while date_cursor <= end_date:
        formatted_date = date_cursor.strftime("%Y-%m-%d")
        new_sadda_count = newly_added_sadda_summary.get(date_cursor, 0)  # Get the count for the date or default to 0
        formatted_item = {'date': formatted_date, 'new_sadda_count': new_sadda_count}
        result_of_newly_added_sadda_summary.append(formatted_item)
        date_cursor += datetime.timedelta(days=1)  # Move to the next date

    return {'newly_added_sadda_summary': result_of_newly_added_sadda_summary}