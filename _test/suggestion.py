    <span id="toolbar">
        <!-- htmx Split button -->
        {% if split_pada %} 
        <button
            class="btn-toolbar w3-bar-item w3-button w3-white w3-tooltip {% if not split_pada %} w3-disabled {% endif %}"
            hx-post="{% url 'htmx_split_pada_in_sentence' translate_word_id=pk %}"
            hx-target="#translation-pada"
            hx-trigger.once="click"
            hx-boost="once"
            hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'
            onclick="$('#htmx-translation-form').hide(); $('#pages-preview').show();"
        >
            <icon class="far fa-object-ungroup"></icon>
            <span class="w3-text w3-tag w3-light-grey">
                {% trans 'Split' %}
            </span>
        </button>
        {% endif %}
        <!-- htmx Merge button -->
        merge_pada: {{ merge_pada }}
        <button
            class="btn-toolbar w3-bar-item w3-button w3-white w3-tooltip {% if not merge_pada %} w3-disabled {% endif %}"
            hx-post="{% url 'htmx_merge_pada_in_sentence' translate_word_id=pk %}"
            hx-target="#translation-pada"
            hx-trigger.once="click"
            hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'
            onclick="$('#htmx-translation-form').hide(); $('#pages-preview').show();"
        >
            <icon class="far fa-object-group"></icon>
            <span class="w3-text w3-tag w3-light-grey">
                {% trans 'Merge' %}
            </span>
        </button>
        <!-- htmx Backspace button -->
        <button
            class="btn-toolbar w3-bar-item w3-right w3-button w3-white w3-tooltip {% if not backspace %} w3-disabled {% endif %}"
            hx-post="{% url 'htmx_backspace' translate_word_id=pk %}"
            hx-trigger.once="click"
            hx-target="#translation-pada"
            hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'
            onclick="$('#htmx-translation-form').hide(); $('#pages-preview').show();"
        >
            <icon class="fas fa-backspace"></icon>
            <span class="w3-text w3-tag w3-light-grey">
                {% trans 'Backspace' %}
            </span>
        </button>
        <!-- htmx Add Sentence button -->
        <button
            class="btn-toolbar w3-bar-item w3-right w3-button w3-white w3-tooltip {% if not new_sentence %} w3-disabled {% endif %}"
            hx-post="{% url 'htmx_add_sentence' translate_word_id=pk %}"
            hx-trigger.once="click"
            hx-target="#translation-pada"
            hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'
            onclick="$('#htmx-translation-form').hide(); $('#pages-preview').show();"
        >
            <icon class="fas fa-stream"></icon>
            <span class="w3-text w3-tag w3-light-grey">
                {% trans '+Sentence' %}
            </span>
        </button>
    </span>