// Function clear result
function clearResult () {
    $("#submit_data").css("display", "none");
    $('#result-container').html('');
};

// Function get construction
function saddaConst(event, string) {
    event.preventDefault();
    var extractedText;
    var startIndex = string.indexOf('[');
    var endIndex = string.indexOf(']');

    if (startIndex !== -1 && endIndex !== -1 && endIndex > startIndex) {
        extractedText = string.substring(startIndex + 1, endIndex);
        extractedText = extractedText.replace(/(\S)\+/g, '$1 + ');
    } else {
        extractedText = null;
    }

    $("#id_construction").val(extractedText);
}


// Function to handle preview btn
function handlePreview(event) {
    event.preventDefault();

    // Call your desired functions here
    create_vipatti();
    find_abidan_closest_matches();
    find_sadda_closest_matches();
};

// Function manage input fields
function manageInputFields(event) {
    $('#fieldWrapper_id_namasaddamala, #fieldWrapper_id_akhyatasaddamala').hide();

    // detact change from input value
    var selectedValue = $('#id_sadda_type').val();
    if (selectedValue === 'NamaSaddamala') {
        $('#fieldWrapper_id_namasaddamala').show();
        $('#fieldWrapper_id_akhyatasaddamala').hide();
    } else if (selectedValue === 'AkhyataSaddamala') {
        $('#fieldWrapper_id_namasaddamala').hide();
        $('#fieldWrapper_id_akhyatasaddamala').show();
    };
};

$(document).ready(function () {
    // Get the button element by its ID
    var previewButton = $('#preview_vipatti');
    var submitButton = $("#submit_data");
    
    var padaPada = $('#id_sadda').val();

    // manage input fields
    manageInputFields();

    $('#id_sadda').on('change', function() {
        check_existing_sadda(padaPada)
    });

    $('#id_sadda_type').change(function() {
        manageInputFields();
    });

    // Attach change event listener to the inputs
    $('#id_namasaddamala, #id_akhyatasaddamala').on('change', function() {
        // Retrieve the updated values from the inputs
        var namasaddamalaValues = $('#id_namasaddamala').val();
        var akhyatasaddamalaValues = $('#id_akhyatasaddamala').val();

        // Check if each array has a value
        var isNamasaddamalaSelected = namasaddamalaValues.length > 0;
        var isAkhyatasaddamalaSelected = akhyatasaddamalaValues.length > 0;
        
        
        // Perform your desired actions with the updated values
        $('#id_sadda').on('input', function() {
            var inputValue = $(this).val();
            if (inputValue.trim() !== '') {
                previewButton.prop('disabled', false);
            }
            else {
                previewButton.prop('disabled', true);
                submitButton.css("display", "none");
            }
        });

        if (isNamasaddamalaSelected || isAkhyatasaddamalaSelected ) {
            previewButton.prop('disabled', false);
        }
        else {
            previewButton.prop('disabled', true);
            submitButton.css("display", "none");
        }
    });

    // find closet matches
    find_abidan_closest_matches();
    find_sadda_closest_matches();
});