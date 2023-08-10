import inspect

from django.db import transaction
from django.db.models import Q, Max, F
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.views import View

from padanukkama.models import Pada, TranslatedWord, VerbConjugation
from padanukkama.tables import TranslatePadaParentChildTable, Sadda
from padanukkama.forms import AddChildPadaForm, LiteralTranslationSaddaForm, TranslatedWordForm

from tipitaka.models import Structure

from utils.pali_char import *
from utils.declension import *

class TranslationPadaView(LoginRequiredMixin, View):
    template_name = 'padanukkama/htmx/htmx_translation_pada.html'

    def get(self, request, pk):
        translation_word = get_object_or_404(TranslatedWord, id=pk)
        pada = translation_word.pada
        add_child_pada_form = AddChildPadaForm()
        translated_word_form = TranslatedWordForm()
        table = TranslatePadaParentChildTable(
            data=pada.get_current_with_descendants(),
            request=request, translate_word_id=pk)
        
        has_parent = pada.has_parent()
        has_sadda = pada.has_sadda()
        split_pada = True if pada.get_descendant_count() > 0 else False
        merge_pada = True if pada.is_descendant() else False
        new_sentence = False if translation_word.word_position == 1 else True
        backspace = True if (translation_word.sentence > 1 and translation_word.word_position == 1) else False

        return render(
            request, self.template_name,
            {
                'pk': pk,
                'table': table,
                'has_parent': has_parent,
                'has_sadda': has_sadda,
                'split_pada': split_pada,
                'merge_pada': merge_pada,
                'new_sentence': new_sentence,
                'backspace': backspace,
                'add_child_pada_form': add_child_pada_form,
                'translated_word_form': translated_word_form,
            })



class updateTranslationWord(LoginRequiredMixin, View):
    pass



class addSentenceView(LoginRequiredMixin, View):
    template_name = 'padanukkama/htmx/htmx_add_sentence.html'

    def post(self, request, translate_word_id):
        translate_word = get_object_or_404(TranslatedWord, id=translate_word_id)
        literal_translation_id = translate_word.literal_translation_id
        structure = translate_word.structure

        # Update data
        sentence = translate_word.sentence

        word_in_other_sentence = TranslatedWord.objects.filter(
            literal_translation=literal_translation_id,
            structure=structure,
            sentence__gt=sentence
        ).order_by('sentence', 'word_position')
        word_in_other_sentence.update(sentence=F('sentence') + 1)


        words_to_update = TranslatedWord.objects.filter(
            literal_translation=literal_translation_id,
            structure=structure,
            sentence=sentence,
            word_position__gte=translate_word.word_position
        ).order_by('sentence', 'word_position')

        word_position = 1
        sentence += 1
        for word in words_to_update:
            word.word_position = word_position
            word.word_order_by_translation = word_position
            word.sentence = sentence
            word.save()
            word_position += 1

        # return context to template
        words_list = TranslatedWord.objects.filter(
            Q(literal_translation=translate_word.literal_translation) & Q(structure=structure.id)
        ).order_by('sentence', 'word_position')
 
        words_list_with_breaks = []
        previous_sentence = None

        for word in words_list:
            if previous_sentence is not None and word.sentence != previous_sentence:
                words_list_with_breaks.append({'break': True})
            words_list_with_breaks.append({'word': word})
            previous_sentence = word.sentence

        context = {
            'structure': structure,
            'words_list_with_breaks': words_list_with_breaks,
        }

        return render(request, self.template_name, context)



class backspaceView(LoginRequiredMixin, View):
    template_name = 'padanukkama/htmx/htmx_add_sentence.html'

    def post(self, request, translate_word_id):
        translate_word = get_object_or_404(TranslatedWord, id=translate_word_id)
        literal_translation_id = translate_word.literal_translation_id
        structure = translate_word.structure
        sentence = translate_word.sentence
        prev_sentence_number = sentence - 1

        last_word_position_in_prev_sentence = TranslatedWord.objects.filter(
            literal_translation=literal_translation_id,
            structure=structure,
            sentence=prev_sentence_number,
        ).aggregate(Max('word_position'))

        # Update data
        words_to_update = TranslatedWord.objects.filter(
            literal_translation=literal_translation_id,
            structure=structure,
            sentence=sentence,
            word_position__gte=translate_word.word_position
        ).order_by('sentence', 'word_position')

        word_in_other_sentence = TranslatedWord.objects.filter(
            literal_translation=literal_translation_id,
            structure=structure,
            sentence__gt=sentence
        )
        word_in_other_sentence.update(sentence=F('sentence') + 1)

        word_position = last_word_position_in_prev_sentence['word_position__max'] + 1
        sentence = sentence - 1
        for word in words_to_update:
            word.word_position = word_position
            word.word_order_by_translation = word_position
            word.sentence = prev_sentence_number
            word.save()
            word_position += 1

        word_in_other_sentence.update(sentence=F('sentence') -2)

        # return context to template
        words_list = TranslatedWord.objects.filter(
            Q(literal_translation=translate_word.literal_translation) & Q(structure=structure.id)
        ).order_by('sentence', 'word_position')
 
        words_list_with_breaks = []
        previous_sentence = None

        for word in words_list:
            if previous_sentence is not None and word.sentence != previous_sentence:
                words_list_with_breaks.append({'break': True})
            words_list_with_breaks.append({'word': word})
            previous_sentence = word.sentence

        context = {
            'structure': structure,
            'words_list_with_breaks': words_list_with_breaks,
        }

        return render(request, self.template_name, context)



class splitPadaInSentenceView(LoginRequiredMixin, View):
    template_name = 'padanukkama/htmx/htmx_add_sentence.html'

    def post(self, request, translate_word_id):
        translate_word = get_object_or_404(TranslatedWord, id=translate_word_id)
        literal_translation_id = translate_word.literal_translation_id
        structure = translate_word.structure
        sentence = translate_word.sentence
        word_position = translate_word.word_position
        pada = translate_word.pada
        descendants = pada.get_only_descendants()

        # Update data
        words_to_update = TranslatedWord.objects.filter(
            literal_translation=literal_translation_id,
            structure=structure,
            sentence=sentence,
            word_position__gt=word_position
        ).order_by('sentence', 'word_position')
        
        for word in words_to_update:
            word.word_position = word.word_position + 1
            word.word_order_by_translation = word.word_position + 1
            word.save()

        word_position = word_position
        for word in descendants:
            tw = TranslatedWord.objects.create(
                literal_translation=translate_word.literal_translation,
                structure=structure,
                wordlist=translate_word.wordlist,
                word=word.pada,
                pada=word,
                sentence=sentence,
                word_position=word_position,
                word_order_by_translation=word_position,
            )
            print(tw.word)
            word_position += 1
        
        TranslatedWord.objects.filter(pk=translate_word_id).delete()

        # return context to template
        words_list = TranslatedWord.objects.filter(
            Q(literal_translation=translate_word.literal_translation) & Q(structure=structure.id)
        ).order_by('sentence', 'word_position')
 
        words_list_with_breaks = []
        previous_sentence = None

        for word in words_list:
            if previous_sentence is not None and word.sentence != previous_sentence:
                words_list_with_breaks.append({'break': True})
            words_list_with_breaks.append({'word': word})
            previous_sentence = word.sentence

        context = {
            'structure': structure,
            'words_list_with_breaks': words_list_with_breaks,
        }

        return render(request, self.template_name, context)



class mergePadaInSentenceView(LoginRequiredMixin, View):
    template_name = 'padanukkama/htmx/htmx_add_sentence.html'
    
    def post(self, request, translate_word_id):
        translate_word = get_object_or_404(TranslatedWord, id=translate_word_id)
        literal_translation_id = translate_word.literal_translation_id  # Get the primary key
        structure = translate_word.structure
        sentence = translate_word.sentence
        pada = translate_word.pada
        parent = pada.get_parent()
        descendants = parent.get_only_descendants()

        # Filter TranslatedWord instances linked to the descendants of the parent pada
        related_translated_words = TranslatedWord.objects.filter(pada__in=descendants)
        related_translated_words_ids = related_translated_words.values_list('id', flat=True)

        words_to_update = TranslatedWord.objects.filter(
            literal_translation=literal_translation_id,
            structure=structure,
            sentence=sentence,
        ).order_by('sentence', 'word_position')

        flag_create = False
        incresment = 0

        for word in words_to_update:
            if word.id in related_translated_words_ids:
                if not flag_create:
                    incresment += 1
                    with transaction.atomic():
                        TranslatedWord.objects.create(
                            literal_translation=translate_word.literal_translation,
                            structure=translate_word.structure,
                            wordlist=translate_word.wordlist,
                            word=parent.pada,
                            pada=parent,
                            sentence=sentence,
                            word_position=incresment,
                            word_order_by_translation=incresment,
                        )
                    flag_create = True
            else:
                incresment += 1
                with transaction.atomic():
                    word.word_position = incresment
                    word.word_order_by_translation = incresment
                    word.save()

        # delete descendents
        related_translated_words.delete()
            
        # return context to template
        words_list = TranslatedWord.objects.filter(
            Q(literal_translation=translate_word.literal_translation) & Q(structure=structure.id)
        ).order_by('sentence', 'word_position')
 
        words_list_with_breaks = []
        previous_sentence = None

        for word in words_list:
            if previous_sentence is not None and word.sentence != previous_sentence:
                words_list_with_breaks.append({'break': True})
            words_list_with_breaks.append({'word': word})
            previous_sentence = word.sentence

        context = {
            'structure': structure,
            'words_list_with_breaks': words_list_with_breaks,
        }

        return render(request, self.template_name, context)
    


class TranslationPadaCreateView(LoginRequiredMixin, View):
    template_name = 'padanukkama/htmx/htmx_translation_pada.html'

    def post(self, request, pk):                
        translation_word = get_object_or_404(TranslatedWord, id=pk)
        padanukkama = translation_word.literal_translation.padanukkama
        pada = Pada.objects.filter(
            Q(padanukkama=padanukkama) & Q(pada=translation_word.word)).first()
            
        form = AddChildPadaForm(request.POST)
        if form.is_valid():
            existing_pada = Pada.objects.filter(
                Q(pada=form.cleaned_data['pada']),
                Q(padanukkama=padanukkama)
            ).first()
            
            child_pada = form.save(commit=False)
            child_pada.parent = pada
            child_pada.padanukkama = pada.padanukkama
            child_pada.pada_seq = encode(extract(clean(pada.pada)))
            child_pada.pada_roman_script = cv_pali_to_roman(extract(clean(pada.pada)))

            if existing_pada:
                child_pada.sadda = existing_pada.sadda
            
            child_pada.save()
            
            # If it is an AJAX request, return a JSON response
            if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return JsonResponse({'success': True})

            # If it is a regular form submission, redirect to the same view
            return redirect(reverse_lazy('htmx_translation_pada', args=[pk]))



class TranslationPadaDeleteView(LoginRequiredMixin, View):
    template_name = 'padanukkama/htmx/htmx_translation_pada.html'

    def post(self, request, translate_word_id, pk): 
        # Retrieve the Pada record to be deleted
        pada = get_object_or_404(Pada, pk=pk)

        if not pada.parent:
            # Record has descendants, do not perform delete action
            messages.error(self.request, _('Delete action failed: Record has descendants'))
            return redirect(reverse_lazy('htmx_translation_pada', args=[translate_word_id]))

        try:
            pada.delete()
        except:
            messages.error(self.request, _('Error: Record deletion unsuccessful'))
        
        # If it is an AJAX request, return a JSON response
        if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return JsonResponse({'success': True})

        # If it is a regular form submission, redirect to the same view
        return redirect(reverse_lazy('htmx_translation_pada', args=[translate_word_id]))



class TranslationPadaTranslateView(LoginRequiredMixin, View):
    template_name = 'padanukkama/htmx/htmx_translation_pada_translate.html'

    def get(self, request, translate_word_id, pk):
        try:
            pada = get_object_or_404(Pada, pk=pk)
            if pada.sadda:
                # Get sadda object & assign Form
                initial_data = {
                    'padanukkama': pada.padanukkama,
                    'sadda':  pada.sadda.sadda,
                    'sadda_type':  pada.sadda.sadda_type,
                    'namasaddamala': [item.pk for item in pada.sadda.namasaddamala.all()],
                    'construction':  pada.sadda.construction,
                    'meaning': pada.sadda.meaning,
                    'description': pada.sadda.description
                }
                form = LiteralTranslationSaddaForm(initial = initial_data)
            else:
                # Initial blank form 
                form = LiteralTranslationSaddaForm(initial={
                    'padanukkama': pada.padanukkama,
                    'sadda': pada.pada,
                    'sadda_type': 'Nama'
                })

            verb_conjugation = VerbConjugation.objects.all().order_by('sequence')

            context = {
                'pada_id': pk,
                'pada': pada,
                'translate_word_id': translate_word_id,
                'padanukkama_id': pada.padanukkama.id,
                'padanukkama': pada.padanukkama,
                'form': form,
                'verb_conjugation': verb_conjugation,
            }

            return render(request, self.template_name, context)
        except ObjectDoesNotExist as e:
            line_number = inspect.currentframe().f_lineno
            error_message = _('Error: {}-{}, please contact SA').format(line_number, e)
            messages.error(request, error_message)
            return render(request, self.template_name, context)
        


class TranslationPadaTranslatePostView(LoginRequiredMixin, View):
    def post(self, request, translate_word_id, pk):
        pada = Pada.objects.get(id=pk)

        # Check if the form is for update or create
        if pada.sadda:
            form = LiteralTranslationSaddaForm(request.POST or None, instance=pada.sadda)
        else:
            form = LiteralTranslationSaddaForm(request.POST or None)

        if form.is_valid():
            existing_sadda = Sadda.objects.filter(
                Q(sadda=form.cleaned_data['sadda']),
                Q(padanukkama=pada.padanukkama)
            ).first()

            if existing_sadda:
                form = LiteralTranslationSaddaForm(request.POST or None, instance=existing_sadda)

            # Form is valid, save the data
            sadda = form.save(commit=False)
            sadda.padanukkama = pada.padanukkama
            sadda.save()
            form.save_m2m()

            # Update popularity of namasaddamala
            for e in sadda.namasaddamala.all():
                e.popularity += 1
                e.save()

            # Update Pada
            pada.sadda = sadda
            pada.save()

            # Find all related Pada
            if sadda.sadda_type == 'Nama':
                template_ids = list(sadda.namasaddamala.all())
                value_list = []
                for tid in template_ids:
                    result = noun_declension(sadda.sadda, tid.id)

                for key, value in result.items():
                    if key != 'error':
                        value_list.extend(value.split())
                unique_words = set(value_list)

                padas_to_update = Pada.objects.filter(padanukkama=pada.padanukkama, pada__in=unique_words)
                for pada in padas_to_update:
                    # Update the object based on your requirements
                    pada.sadda = sadda
                    # Save the changes
                    pada.save()

        else:
            # Invalid form, Message
            messages.error(request, _('Form is invalid. Please correct the errors'))
        
    
        if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return JsonResponse({'success': True})

        # If it is a regular form submission, redirect to the same view
        redirect_url = reverse_lazy('htmx_translation_pada_translate', args=[translate_word_id, pk])

        return redirect(redirect_url)