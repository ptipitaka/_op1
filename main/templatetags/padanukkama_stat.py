from django import template
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db.models import Q, Count
from django.db.models.functions import TruncDate
from django.utils.translation import gettext_lazy as _


import json
import datetime 
import calendar

from padanukkama.models import *
from padanukkama.workflows import SaddaTranslationWorkflow

register = template.Library()

@register.filter
def replace(value, arg):
    return value.replace(arg, '')

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
    waiting = Pada.objects.filter(
            Q(padanukkama=padanukkama_id) & Q(children__isnull=True) & Q(sadda__isnull=True)
        ).count()
    onprocess = Pada.objects.filter(
            Q(padanukkama=padanukkama_id) & Q(children__isnull=True) & Q(sadda__isnull=False)
        ).count()
    return {
        'padanukkama_id': padanukkama_id,
        'waiting': waiting,
        'onprocess': onprocess
        }



@register.inclusion_tag('main/statistic/last_update.html', takes_context=True)
def last_10_updates(context):
    current_user = context.request.user
    result = None
    if current_user.id:
        result = Sadda.get_last_3_pada_updates(current_user)
    return { 'result': result }



@register.inclusion_tag('main/statistic/relate_pada.html')
def relate_pada(sadda):
    result = Pada.objects.filter(sadda__sadda=sadda)[:10]
    return {'result': result}



@register.inclusion_tag('main/statistic/translation_process.html')
def translation_process(padanukkama_id):
    # Count Sadda objects for each workflow state
    sadda_by_state = Sadda.objects.filter(
        padanukkama_id=padanukkama_id).values('state').annotate(count=Count('state'))
    return {
        'padanukkama_id': padanukkama_id,
        'sadda_by_state': sadda_by_state,
        }



@register.inclusion_tag('main/statistic/monthly_progress.html')
def monthly_progress(padanukkama_id):
    # Get the current date and time
    current_date = datetime.datetime.now().date()
    _, last_day = calendar.monthrange(current_date.year, current_date.month)

    # Calculate the start and end dates of the current month
    start_date = current_date.replace(day=1)
    end_date = current_date.replace(day=last_day)

    workflow_states = SaddaTranslationWorkflow.states

    result = []

    # Query the newly added 'Sadda' objects
    # -------------------------------------
    for wfs in workflow_states:
        q_sadda_summary_by_wf_by_date = (
            Sadda.history
            .filter(
                padanukkama=padanukkama_id,
                history_date__range=(start_date, end_date),
                state=wfs.name
            )
            .annotate(date=TruncDate('history_date'))
            .values('date')
            .annotate(sadda_count=Count('id'))
            .order_by('date')
        )

        # Create a dictionary to store the date-count pairs
        sadda_summary_by_wf_by_date = {item['date']: item['sadda_count'] for item in q_sadda_summary_by_wf_by_date}

        # Create a list to store the formatted results
        result_of_sadda_summary_by_wf_by_date = []

        # Iterate over each date in the current month
        date_cursor = start_date
        while date_cursor <= end_date:
            formatted_date = date_cursor.strftime("%Y-%m-%d")
            sadda_count = sadda_summary_by_wf_by_date.get(date_cursor, 0)  # Get the count for the date or default to 0
            formatted_item = {'date': formatted_date, 'sadda_count': sadda_count}
            result_of_sadda_summary_by_wf_by_date.append(formatted_item)
            date_cursor += datetime.timedelta(days=1)  # Move to the next date

        result.append({'wfs': wfs.name, 'data': result_of_sadda_summary_by_wf_by_date})

    return {
        'padanukkama_id': padanukkama_id,
        'result': json.dumps({'result': result})
        }