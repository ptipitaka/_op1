from django.utils.translation import gettext_lazy as _
from django_xworkflows import models as xwf_models

class SaddaTranslationWorkflow(xwf_models.Workflow):
    states = (
        ('new', _('New')),
        ('translated', _('Translated')),
        ('reviewed', _('Review')),
        ('approved', _('Approved')),
    )

    transitions = (
        ('translated', 'new', 'translated'),
        ('reviewed', 'translated', 'reviewed'),
        ('approved', 'reviewed', 'approved'),
    )

    initial_state = 'new'
