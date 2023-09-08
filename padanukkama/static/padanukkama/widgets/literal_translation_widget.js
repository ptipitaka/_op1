(function() {
    var widgetContainer = document.getElementById('my-widget-container');
    var literal_translation_id = widgetContainer.getAttribute('data-literal_translation_id');
    var structure_id = widgetContainer.getAttribute('data-structure_id');
    
    var url = new URL('https://openpali.org/th/padanukkama/literal-translation/widget/');
    if (literal_translation_id) url.searchParams.append('literal_translation_id', literal_translation_id);
    if (structure_id) url.searchParams.append('structure_id', structure_id);
    
    fetch(url)
        .then(response => response.text())
        .then(html => {
            var shadowRoot = widgetContainer.attachShadow({ mode: 'open' });
            shadowRoot.innerHTML = html;
        })
        .catch(err => {
            console.warn('Error: ', err);
        });
})();
