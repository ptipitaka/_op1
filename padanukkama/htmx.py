import inspect
import json

from django.db import transaction
from django.db.models import Q, Max, F, Count
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView, DetailView
from django.views.generic.detail import SingleObjectMixin

from padanukkama.models import Pada, TranslatedWord, VerbConjugation
from padanukkama.tables import TranslatePadaParentChildTable, Sadda
from padanukkama.forms import AddChildPadaForm, LiteralTranslationSaddaForm, TranslatedWordForm, TranslatedWordAddForm

from tipitaka.models import Structure

from utils.pali_char import *
from utils.declension import *


class TranslationPadaView(LoginRequiredMixin, View):
    template_name = 'padanukkama/htmx/htmx_translation_pada.html'

    def get(self, request, pk):
        translate_word = get_object_or_404(TranslatedWord, id=pk)
        has_pada = translate_word.has_pada()

        translated_word_form = TranslatedWordForm(
            instance=translate_word,
            prefix="translated_word_form")
        if has_pada:
            translated_word_add_form = TranslatedWordAddForm(
                prefix="translated_word_add_form")
        else:
            translated_word_add_form = TranslatedWordAddForm(
                instance=translate_word,
                prefix="translated_word_add_form")

        add_child_pada_form = AddChildPadaForm(
            prefix="add_child_pada_form")

        return self._render_page(
            request,
            translated_word_form,
            translated_word_add_form,
            add_child_pada_form,
            pk
        )

    def post(self, request, pk):
        # initial vars
        translate_word = get_object_or_404(TranslatedWord, id=pk)

        # forms
        translated_word_form = TranslatedWordForm(
            instance=translate_word,
            prefix="translated_word_form",
            data=request.POST)
        translated_word_add_form = TranslatedWordAddForm(
            prefix="translated_word_add_form",
            data=request.POST)
        add_child_pada_form = AddChildPadaForm(
            prefix="add_child_pada_form",
            data=request.POST)

        # each process form
        if add_child_pada_form.is_valid():
            padanukkama = translate_word.literal_translation.padanukkama
            pada = Pada.objects.filter(
                Q(padanukkama=padanukkama) & Q(pada=translate_word.word)).first()
            existing_pada = Pada.objects.filter(
                Q(pada=add_child_pada_form.cleaned_data['pada']),
                Q(padanukkama=padanukkama)
            ).first()
            
            child_pada = add_child_pada_form.save(commit=False)
            child_pada.parent = pada
            child_pada.padanukkama = pada.padanukkama
            child_pada.pada_seq = encode(extract(clean(pada.pada)))
            child_pada.pada_roman_script = cv_pali_to_roman(extract(clean(pada.pada)))

            if existing_pada:
                child_pada.sadda = existing_pada.sadda
            child_pada.save()


        # update current page
        return self._render_page(
            request,
            translated_word_form,
            translated_word_add_form,
            add_child_pada_form, pk)

    def _render_page(self, request, translated_word_form, translated_word_add_form, add_child_pada_form, pk):
        translation_word = get_object_or_404(TranslatedWord, id=pk)
        
        pada = table = has_parent = has_sadda = split_pada = merge_pada = False
        has_pada = translation_word.has_pada()

        if has_pada:
            pada = translation_word.pada
        
            table = TranslatePadaParentChildTable(
                data=pada.get_current_with_descendants().order_by('tree_id', 'lft'),
                request=request, translate_word_id=pk)
            
            has_parent = pada.has_parent()
            has_sadda = pada.has_sadda()
            split_pada = True if pada.get_descendant_count() > 0 else False
            merge_pada = True if pada.is_descendant() else False

        add_word = has_pada
        new_sentence = False if translation_word.word_position == 1 else True
        backspace = True if (translation_word.sentence > 1 and translation_word.word_position == 1) else False

        return render(
            request, self.template_name,
            {
                'pk': pk,
                'translation_word': translation_word,
                'has_pada': has_pada,
                'pada': pada,
                'table': table,
                'has_parent': has_parent,
                'has_sadda': has_sadda,
                'split_pada': split_pada,
                'merge_pada': merge_pada,
                'add_word': add_word,
                'new_sentence': new_sentence,
                'backspace': backspace,
                'add_child_pada_form': add_child_pada_form,
                'translated_word_form': translated_word_form,
                'translated_word_add_form': translated_word_add_form,
            }
        )



class UpdateSentenceView(LoginRequiredMixin, View):
    template_name = 'padanukkama/htmx/htmx_update_sentence.html'

    def post(self, request, translate_word_id):
        # initial vars
        try:
            translate_word = get_object_or_404(TranslatedWord, id=translate_word_id)
            has_pada = translate_word.has_pada()
            success_message = ''
            error_message = ''
        except Http404:
            context = {'error_message':_('Word not found.')}
            return render(request, self.template_name, context)

        # each process form
        # translated_word_form
        if "translate-submit" in request.POST:
            translated_word_form = TranslatedWordForm(
                instance=translate_word,
                prefix="translated_word_form",
                data=request.POST)
            if translated_word_form.is_valid():
                try:
                    translated_word_form.save()
                    success_message = _('Form saved successfully.')
                except:
                    error_message = _('Form saved unsuccessfully')
        
        # translated_word_add_form
        elif "add-word-submit" in request.POST:
            # การตรวจสอบ has_pada เพื่อดูว่าเป็นการเพิ่ม โดยเลือกจาก บท ในประโยค
            # เป็นการเพิ่ม คำโยค จึงต้องปรับปรุงลำดับคำไปพร้อมกับ
            if has_pada:
                translated_word_add_form = TranslatedWordAddForm(
                    prefix="translated_word_add_form",
                    data=request.POST)
            
                if translated_word_add_form.is_valid():
                    words_to_update = TranslatedWord.objects.filter(
                        literal_translation=translate_word.literal_translation,
                        structure=translate_word.structure,
                        sentence=translate_word.sentence,
                        word_position__gt=translate_word.word_position
                    ).order_by('sentence', 'word_position')
                    words_to_update.update(
                        word_position=F('word_position') + 1, 
                        word_order_by_translation=F('word_position') + 1)

                    new_word_instance = translated_word_add_form.save(commit=False)
                    new_word_instance.literal_translation = translate_word.literal_translation
                    new_word_instance.structure = translate_word.structure
                    new_word_instance.sentence = translate_word.sentence
                    new_word_instance.word_position = translate_word.word_position + 1
                    new_word_instance.word_order_by_translation = translate_word.word_position + 1
                    new_word_instance.insert_reference = translate_word
                
                    try:
                        new_word_instance.save()
                        success_message = _('Form saved successfully.')
                    except:
                        error_message = _('Form saved unsuccessfully')
            else:
                translated_word_add_form = TranslatedWordAddForm(
                    instance=translate_word,
                    prefix="translated_word_add_form",
                    data=request.POST)     
                try:
                    if translated_word_add_form.is_valid():
                        translated_word_add_form.save()
                        success_message = _('Form saved successfully.')
                    else:
                        error_message = _('Form saved unsuccessfully')
                    success_message = _('Form saved successfully.')
                except:
                    error_message = _('Form saved unsuccessfully')        
        
        # delete-word-submit
        elif "delete-word-submit" in request.POST:
            words_to_update = TranslatedWord.objects.filter(
                literal_translation=translate_word.literal_translation,
                structure=translate_word.structure,
                sentence=translate_word.sentence,
                word_position__gt=translate_word.word_position
            ).order_by('sentence', 'word_position')

            word_position = translate_word.word_position
            for word in words_to_update:
                word.word_position = word_position
                word.word_order_by_translation = word_position
                word.save()
                word_position += 1

            try:
                translate_word.delete()
                success_message = _('Form deleted successfully.')
            except:
                error_message = _('Form deleted unsuccessfully')

        # return context to template
        words_list = TranslatedWord.objects.filter(
            Q(literal_translation=translate_word.literal_translation) & 
            Q(structure=translate_word.structure.id)
        ).order_by('sentence', 'word_order_by_translation')

        context = {
            'structure': translate_word.structure,
            'words_list': words_list,
            'success_message': success_message,
            'error_message': error_message,
            'order_type': 'translation'
        }

        return render(request, self.template_name, context)



def reset_word_sequence(query_set, sentence, init):
    # Update word positions
    for index, word in enumerate(query_set, start=init):
        word.sentence = sentence
        word.word_position = index
        word.word_order_by_translation = index

    # Bulk update to save all changes in one query
    fields_to_update = ['sentence', 'word_position', 'word_order_by_translation']
    query_set.bulk_update(query_set, fields_to_update)



class AddSentenceView(LoginRequiredMixin, View):
    template_name = 'padanukkama/htmx/htmx_update_sentence.html'

    def post(self, request, translate_word_id):
        # ค่าตั้งต้น
        translate_word = get_object_or_404(TranslatedWord, id=translate_word_id)
        literal_translation_id = translate_word.literal_translation_id
        structure = translate_word.structure
        original_sentence  = translate_word.sentence

        # ปรับปรุงข้อมูล
        # ประโยคอื่น ๆ ที่ปรากฏหลังจากประโยคของคำที่เลือกนั้น ให้ +1 เพราะการเพิ่มประโยค 
        words_in_gt_sentence = TranslatedWord.objects.filter(
            literal_translation=literal_translation_id,
            structure=structure,
            sentence__gt=original_sentence
        ).order_by('sentence', 'word_position')
        words_in_gt_sentence.update(sentence=F('sentence') + 1)

        # รีเซ็ตการลำดับ word_position และ word_order_by_translation
        # สำหรับบรรทัดใหม่
        words_in_new_sentence = TranslatedWord.objects.filter(
            literal_translation=literal_translation_id,
            structure=structure,
            sentence=original_sentence,
            word_position__gte=translate_word.word_position
        ).order_by('sentence', 'word_position')
        new_sentence = original_sentence + 1
        reset_word_sequence(words_in_new_sentence, new_sentence, 1)
        
        # สำหรับบรรทัดปัจจุบัน
        words_in_current_sentence = TranslatedWord.objects.filter(
            literal_translation=literal_translation_id,
            structure=structure,
            sentence=original_sentence
        ).order_by('sentence', 'word_position')
        reset_word_sequence(words_in_current_sentence, original_sentence, 1)

        # คืนค่าเพื่อแสดงใน template
        words_list = TranslatedWord.objects.filter(
            Q(literal_translation=translate_word.literal_translation) & 
            Q(structure=structure.id)
        ).order_by('sentence', 'word_order_by_translation')

        context = {
            'structure': structure,
            'words_list': words_list,
            'success_message': _('Form saved successfully.')
        }

        return render(request, self.template_name, context)



class BackspaceView(LoginRequiredMixin, View):
    template_name = 'padanukkama/htmx/htmx_update_sentence.html'

    def post(self, request, translate_word_id):
        # ค่าตั้งต้น
        translate_word = get_object_or_404(TranslatedWord, id=translate_word_id)
        literal_translation_id = translate_word.literal_translation_id
        structure = translate_word.structure
        sentence = translate_word.sentence
        prev_sentence_number = sentence - 1
        # ตำแหน่งในบรรทัดก่อนหน้า
        last_word_position_in_prev_sentence = TranslatedWord.get_max_word_order_by_translation(
            literal_translation_id, structure, prev_sentence_number)


        # ปรับปรุงข้อมูล
        words_in_current_sentence = TranslatedWord.objects.filter(
            literal_translation=literal_translation_id,
            structure=structure,
            sentence=sentence,
            word_position__gte=translate_word.word_position
        ).order_by('sentence', 'word_position')
        next_word_position = last_word_position_in_prev_sentence + 1
        reset_word_sequence(words_in_current_sentence, prev_sentence_number, next_word_position)

        word_in_other_sentence = TranslatedWord.objects.filter(
            literal_translation=literal_translation_id,
            structure=structure,
            sentence__gt=sentence
        )
        word_in_other_sentence.update(sentence=F('sentence') - 1)

        # return context to template
        words_list = TranslatedWord.objects.filter(
            Q(literal_translation=translate_word.literal_translation) & 
            Q(structure=structure.id)
        ).order_by('sentence', 'word_order_by_translation')

        context = {
            'structure': structure,
            'words_list': words_list,
            'success_message': _('Form saved successfully.')
        }

        return render(request, self.template_name, context)



class SplitPadaInSentenceView(LoginRequiredMixin, View):
    template_name = 'padanukkama/htmx/htmx_update_sentence.html'

    def post(self, request, translate_word_id):
        translate_word = get_object_or_404(TranslatedWord, id=translate_word_id)
        literal_translation_id = translate_word.literal_translation_id
        structure = translate_word.structure
        sentence = translate_word.sentence
        word_position = translate_word.word_position
        pada = translate_word.pada
        descendants = pada.get_only_descendants().order_by('tree_id', 'lft')
        descendants_count = pada.has_descendants()

        # Update data
        words_to_update = TranslatedWord.objects.filter(
            literal_translation=literal_translation_id,
            structure=structure,
            sentence=sentence,
            word_position__gt=word_position
        ).order_by('sentence', 'word_position')
        words_to_update.update(
            word_position=F('word_position') + (descendants_count - 1), 
            word_order_by_translation=F('word_position') + (descendants_count - 1))
        
        for word_position, word in enumerate(descendants, start=word_position):
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
        
        TranslatedWord.objects.filter(pk=translate_word_id).delete()

        # return context to template
        words_list = TranslatedWord.objects.filter(
            Q(literal_translation=translate_word.literal_translation) & 
            Q(structure=structure.id)
        ).order_by('sentence', 'word_order_by_translation')
 

        context = {
            'structure': structure,
            'words_list': words_list,
            'success_message': _('Form saved successfully.')
        }

        return render(request, self.template_name, context)



class MergePadaInSentenceView(LoginRequiredMixin, View):
    template_name = 'padanukkama/htmx/htmx_update_sentence.html'
    
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
        ).order_by('sentence', 'word_order_by_translation')

        context = {
            'structure': structure,
            'words_list': words_list,
            'success_message': _('Form saved successfully.')
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
                    'verb_conjugation': [item.pk for item in pada.sadda.verb_conjugation.all()],
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
            noun_decl_meaning = NounDeclension.objects.all().order_by('code').values_list('description', 'ekavacana')

            context = {
                'pada_id': pk,
                'pada': pada,
                'translate_word_id': translate_word_id,
                'padanukkama_id': pada.padanukkama.id,
                'padanukkama': pada.padanukkama,
                'form': form,
                'verb_conjugation': verb_conjugation,
                'nom': list(noun_decl_meaning)[0],
                'acc': list(noun_decl_meaning)[1],
                'instr': list(noun_decl_meaning)[2],
                'dat': list(noun_decl_meaning)[3],
                'abl': list(noun_decl_meaning)[4],
                'gen': list(noun_decl_meaning)[5],
                'loc': list(noun_decl_meaning)[6],
                'voc': list(noun_decl_meaning)[7],
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
        redirect_url = reverse_lazy('htmx_translation_pada', args=[translate_word_id])

        return redirect(redirect_url)




class TranslationHelperView(LoginRequiredMixin, SingleObjectMixin, TemplateView):
    model = TranslatedWord
    template_name = "padanukkama/htmx/htmx_translation_helper.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)
    
    def create_noun_decl_table(self, pada):
        # วนลูปแบบการแจกวิภัตติแต่ละแบบ เพื่อสร้างและเทียบข้อมูลในตาราง
        namasaddamala_related_objects = pada.sadda.namasaddamala.all().order_by('-popularity')
        sadda = pada.sadda.sadda
        result = []
        declension_groups = {}
        for tid in namasaddamala_related_objects:
            # namasaddamala
            namasaddamala = {
                'title': tid.title,
                'nama_type': tid.nama_type.title,
                'linga': tid.linga.code,
                'karanta': tid.karanta.title,
            }
            # declension
            declension = []
            result_list = noun_declension(sadda, tid.id)
            filtered_dict = {k: v for k, v in result_list.items() if k == 'error' or pada.pada in v.split()}
            for key, value in filtered_dict.items():
                declension_detail = {}
                if key != 'error':
                    code = key.split('_')[0]
                    vacana = key.split('_')[1]
                    try:
                        declension_obj = NounDeclension.objects.get(code=code)
                        declension_detail = {
                            'title': declension_obj.title,
                            'description': declension_obj.description,
                            'ekavacana': declension_obj.ekavacana,
                            'bahuvachana': declension_obj.bahuvachana,
                            'vacana': vacana
                        }

                        declension_data = {
                            'key' : key,
                            'code' : code,
                            'vacana' : vacana,
                            'value' : value,
                            'detail' : declension_detail
                        }
                        
                        if code not in declension_groups:
                            declension_groups[code] = []
                        declension_groups[code].append(declension_data)

                    except NounDeclension.DoesNotExist:
                        # กรณีไม่พบ key นั้นใน database ควรมีการ handle error
                        print(f"Declension with code {key} not found.")

            declension = [group for group in declension_groups.values()]
            result.append({
                'namasaddamala': namasaddamala,
                'declension': declension
            })

        return result

    def create_akhyata_decl_table(self, verb_conjugation_ids):
        if verb_conjugation_ids:
            verb_conjugation = VerbConjugation.objects.filter(pk__in = verb_conjugation_ids).order_by('sequence')
        return verb_conjugation
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        translate_word = self.object
        pada = sadda = sadda_type = nama_declension_table = akhyata_declension_table = None
        noun_declension_dict = {obj.code: obj for obj in NounDeclension.objects.all()}
        vacana = {'sg': _("Ekavacana"), 'pl': _("Bahuvacana")}

        if translate_word.pada:
            pada_instance = translate_word.pada
            pada = pada_instance.pada
            if pada_instance.sadda:
                sadda_instance = pada_instance.sadda
                sadda = sadda_instance.sadda
                sadda_type = sadda_instance.sadda_type
                if sadda_type == "Nama":
                    nama_declension_table = self.create_noun_decl_table(pada_instance) 
                elif sadda_type == "Akhyata":
                    verb_conjugations = sadda_instance.verb_conjugation.all()
                    verb_conjugation_ids = [vc.id for vc in verb_conjugations]

                    akhyata_declension_table = self.create_akhyata_decl_table(verb_conjugation_ids)

        context.update({
            'translate_word': translate_word,
            'pada': pada,
            'sadda': sadda,
            'sadda_type': sadda_type,
            'nama_declension_table': nama_declension_table,
            'akhyata_declension_table': akhyata_declension_table,
            'noun_declension_dict': noun_declension_dict,
            'vacana': vacana,
        })

        return context
    



class FoundInTranslationView(LoginRequiredMixin, TemplateView):
    template_name = 'padanukkama/htmx/htmx_found_in_translation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # รับ object จาก pk ที่ส่งเข้ามา
        obj = get_object_or_404(TranslatedWord, pk=self.kwargs['pk'])

        # ค้นหา object ที่มีเนื้อหาเหมือนกันใน field 'word' กับ obj ที่รับมา
        similar_objects = TranslatedWord.objects.filter(
            word=obj.word,
            literal_translation=obj.literal_translation
        ).exclude(translation="")


        # นับจำนวนที่พบในการแปลทั้งหมด
        context['found_in_translation_count'] = similar_objects.count()
        # กรองเฉพาะรายการที่มีข้อมูลใน translation field มีความแตกต่างกัน
        unique_translations = similar_objects.order_by(
            'translation', 'id').distinct('translation')

        context['found_in_translation'] = unique_translations
        context['sentence'] = obj.sentence
        return context


class UpdateTranslationSequence(LoginRequiredMixin, View):
    template_name = 'padanukkama/htmx/htmx_update_sentence.html'

    def post(self, request, translate_word_id, direction):
        # initial vars
        translate_word = get_object_or_404(TranslatedWord, id=translate_word_id)
        max_order = TranslatedWord.get_max_word_order_by_translation(
            translate_word.literal_translation,
            translate_word.structure, translate_word.sentence)

        success_message = ''
        error_message = ''


        if direction == 'increase':
            if translate_word.word_order_by_translation < max_order:
                words_list = TranslatedWord.objects.filter(
                    Q(literal_translation=translate_word.literal_translation) & 
                    Q(structure=translate_word.structure.id) & 
                    Q(sentence=translate_word.sentence) &
                    Q(word_order_by_translation__gte=translate_word.word_order_by_translation)
                ).order_by('word_order_by_translation').all()[:2]
                # ตรวจสอบว่าได้รายการ 2 รายการจริงๆ
                if len(words_list) == 2:
                    # สลับค่า word_order_by_translation
                    words_list[0].word_order_by_translation, words_list[1].word_order_by_translation = words_list[1].word_order_by_translation, words_list[0].word_order_by_translation
                    
                    # บันทึกการเปลี่ยนแปลง
                    words_list[0].save()
                    words_list[1].save()
                    success_message = _('Form saved successfully.')
                else:
                    error_message = _('Form saved unsuccessfully')

            translate_word.word_order_by_translation
        elif direction == 'decrease':
            if translate_word.word_order_by_translation > 1:
                words_list = TranslatedWord.objects.filter(
                    Q(literal_translation=translate_word.literal_translation) & 
                    Q(structure=translate_word.structure.id) & 
                    Q(sentence=translate_word.sentence) &
                    Q(word_order_by_translation__lte=translate_word.word_order_by_translation)
                ).order_by('-word_order_by_translation').all()[:2]
                if len(words_list) == 2:
                    # สลับค่า word_order_by_translation
                    words_list[0].word_order_by_translation, words_list[1].word_order_by_translation = words_list[1].word_order_by_translation, words_list[0].word_order_by_translation
                    
                    # บันทึกการเปลี่ยนแปลง
                    words_list[0].save()
                    words_list[1].save()
                    success_message = _('Form saved successfully.')
                else:
                    error_message = _('Form saved unsuccessfully')

        # return context to template
        words_list = TranslatedWord.objects.filter(
            Q(literal_translation=translate_word.literal_translation) & 
            Q(structure=translate_word.structure.id)
        ).order_by('sentence', 'word_order_by_translation')

        context = {
            'structure': translate_word.structure,
            'words_list': words_list,
            'success_message': success_message,
            'error_message': error_message
        }        

        return render(request, self.template_name, context)
    


# UpdateTranslationSequenceBySortableJs
@require_POST
def UpdateTranslationSequenceBySortableJs(request):
    data = json.loads(request.body.decode('utf-8'))
    sorted_ids = data.get('sortedIDs', [])
    
    for index, word_id in enumerate(sorted_ids):
        word = TranslatedWord.objects.get(id=word_id)
        word.word_order_by_translation = index + 1
        word.save()
    
    return JsonResponse({'status': 'success'})



# ChangeWordOrder
class ChangeWordOrder(LoginRequiredMixin, View):
    template_name = 'padanukkama/htmx/htmx_update_sentence.html'

    def get(self, request, *args, **kwargs):
        success_message = _('Form saved successfully.')
        error_message = ''

        order_type = request.GET.get('order_type')
        structure_id = request.GET.get('structure_id')
        structure = Structure.objects.get(pk=structure_id)
        literal_translation_id = request.GET.get('literal_translation_id')

        if order_type == "translation":
            words_list = TranslatedWord.objects.filter(
                Q(literal_translation=literal_translation_id) & 
                Q(structure=structure_id)
            ).order_by('sentence', 'word_order_by_translation')
        else:
            words_list = TranslatedWord.objects.filter(
                Q(literal_translation=literal_translation_id) & 
                Q(structure=structure_id)
            ).order_by('sentence', 'word_position')

        context = {
            'structure': structure,
            'words_list': words_list,
            'success_message': success_message,
            'error_message': error_message,
            'order_type': order_type,
        }   

        return render(request, self.template_name, context)
    


# widget_helper
class TranslationWidgetHelperView(LoginRequiredMixin, DetailView):
    model = TranslatedWord
    template_name = "padanukkama/htmx/htmx_translation_widtet_helper.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # คุณสามารถเพิ่มข้อมูลเพิ่มเติมใน context ที่นี่ถ้าคุณต้องการ
        return context