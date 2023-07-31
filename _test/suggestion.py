class LiteralTranslationTranslateView(LoginRequiredMixin, DetailView):
    model = LiteralTranslation
    template_name = 'padanukkama/literal_translation_translate.html'
    context_object_name = 'literal_translation'

    # ... (other methods and attributes) ...

    def handle_no_permission(self, request):
        messages.error(request, _('You do not have permission to access this page'))
        return redirect_to_login(request.get_full_path(), login_url=self.get_login_url(), redirect_field_name=self.get_redirect_field_name())

    def get_success_url(self):
        return reverse_lazy('literal_translation')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        padanukkama = self.object.padanukkama

        # Fetch structures associated with this padanukkama instance
        selected_structures = padanukkama.structure.all()

        # Fetch CommonReference objects for all selected structures using select_related
        common_references = CommonReference.objects.filter(structure__in=selected_structures).select_related('wordlist_version')

        context['structures'] = selected_structures
        context['common_references'] = common_references

        # Get the 'toc_id' query parameter from the request's GET dictionary
        toc_id = self.request.GET.get('toc_id')
        
        # Retrieve the structure using get_object_or_404 or set to None
        selected_structure = None
        if toc_id:
            selected_structure = get_object_or_404(Structure, id=toc_id, padanukkama=padanukkama)

            # Get the wordlist_version from the selected_structure
            wordlist_version = selected_structure.wordlist_version.first()

            # Get the CommonReference instance for the selected structure and wordlist_version
            common_reference = common_references.filter(structure=selected_structure, wordlist_version=wordlist_version).first()

            if common_reference:
                # Fetch WordList instances based on the provided from_position and to_position
                from_position = common_reference.from_position
                to_position = common_reference.to_position
                wordlist_version = common_reference.wordlist_version

                word_lists = WordList.objects.filter(
                    Q(code__gte=from_position, code__lte=to_position),
                    wordlist_version=wordlist_version
                )

                context['word_lists'] = word_lists

        context['selected_structure'] = selected_structure

        return context
