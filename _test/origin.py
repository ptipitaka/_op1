class LiteralTranslationTranslateView(LoginRequiredMixin, DetailView):
    model = LiteralTranslation
    template_name = 'padanukkama/literal_translation_translate.html'
    context_object_name = 'literal_translation'

    def handle_no_permission(self, request):
        messages.error(request, _('You do not have permission to access this page'))
        return redirect_to_login(request.get_full_path(), login_url=self.get_login_url(), redirect_field_name=self.get_redirect_field_name())

    def get_success_url(self):
        return reverse_lazy('literal_translation')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Check if padanukkama exists and fetch structures associated with it
        padanukkama = self.object.padanukkama
        if padanukkama:
            selected_structures = padanukkama.structure.all()
        else:
            selected_structures = []

        # Fetch only structures associated with this padanukkama instance
        selected_structures = padanukkama.structure.all()

        # Fetch CommonReference objects for all selected structures
        common_references = CommonReference.objects.filter(structure__in=selected_structures)

        context['structures'] = selected_structures
        context['common_references'] = common_references

        # Get the 'toc_id' query parameter from the request's GET dictionary
        toc_id = self.request.GET.get('toc_id')
        # Retrieve the structure using get_object_or_404
        if toc_id:
            try:
                # Retrieve the structure using get_object_or_404
                selected_structure = get_object_or_404(Structure, id=toc_id)
            except Structure.DoesNotExist:
                selected_structure = None
        else:
            selected_structure = None
        
        context['selected_structure'] = selected_structure

        return context
