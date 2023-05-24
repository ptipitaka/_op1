$(document).ready(function() {    
    $.ajax({
        url: '{% url "find_abidan_closest_matches" %}',
        type: 'GET',
        data: {
            'string': '{{ pada.pada }}'
        },
        beforeSend: function() {
            // Show the loading message before making the AJAX request
            $('#abidan-closest-matches').html("<i id='loading-icon' class='fa fa-spinner fa-spin'></i> {% trans 'Loading...' %}");
        },
        success: function(response) {
            var closestMatches = response.closest_matches;
            var matchesHtml = '';

            // Generate the HTML for displaying the closest matches
            if (closestMatches.length === 0) {
                matchesHtml = '<li>No matches found.</li>';
            } else {
                for (var i = 0; i < closestMatches.length; i++) {
                    var abidanDetailsUrl = '{% url "abidan_details" pk=0 %}'.replace('0', closestMatches[i].id);

                    // Wrap the image with a link to open the modal
                    matchesHtml += '<div class="w3-cell-row">';
                    matchesHtml +=      '<div class="w3-container w3-cell" style="width:15%">';
                    matchesHtml +=          '<img src="' + closestMatches[i].image_ref + '" class="responsive" ';
                    matchesHtml +=          'style="cursor: pointer;" ';
                    matchesHtml +=          'onclick="openModal(\'' + closestMatches[i].image_ref + '\')"/>';
                    matchesHtml +=      '</div>'

                    matchesHtml +=      '<div class="w3-container w3-cell">';
                    matchesHtml +=           '<p>' + closestMatches[i].dict + '<br>';
                    matchesHtml +=           closestMatches[i].burmese;
                    matchesHtml +=           '<a class="w3-btn" style="text-decoration:None;hover:pointer;" target="_blank" ';
                    matchesHtml +=           'href="' + abidanDetailsUrl + '"> <i class="fas fa-link"></i></a><br>';
                    matchesHtml +=           '<div class="w3-light-grey w3-tiny" style="width:100px;">'
                    matchesHtml +=               '<div class="w3-container w3-green" style="width:'+ closestMatches[i].score +'%">'
                    matchesHtml +=                  closestMatches[i].score + '%';
                    matchesHtml +=               '</div>';
                    matchesHtml +=           '</div>';
                    matchesHtml +=      '</div>';
                    matchesHtml += '</div>';
                }
            }

            // Update the abidan-closest-matches ul with the generated HTML
            $('#abidan-closest-matches').html(matchesHtml);
        }
    });
})
