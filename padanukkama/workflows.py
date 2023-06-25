from django.utils.translation import gettext_lazy as _
from django_xworkflows import models as xwf_models

class SaddaTranslationWorkflow(xwf_models.Workflow):
    states = (
        ('new', _('New')),
        ('translation', _('Translation')),
        ('review', _('Review')),
        ('approved', _('Approved')),
    )

    transitions = (
        ('start', 'new', 'translation'),
        ('reviewing', 'translation', 'review'),
        ('complete', 'review', 'approved'),
    )

    initial_state = 'new'
