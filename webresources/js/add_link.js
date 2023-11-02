let links = [];

$(document).ready(function() {
    $('button.add_link').click(function(){
        open_panel();
        $(this).addClass("disabled");
    });
    $('button.add_link.evolution').click(function(){
        let artifact = $(this).closest('.artifact-small');
        $('#links_list').append(link(artifact.data('info'), 0));
    });
    $('button.add_link.dependency').click(function(){
        let artifact = $(this).closest('.artifact-small');
        $('#links_list').append(link(artifact.data('info'), 1));
    });
    $('form').submit(function(event) {
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: '',
            data: JSON.stringify(links),
            processData: false,
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(response){
                window.location.href = $('#previous_url').html();
            },
            error: function(error){
                alert_appear(
                    'Verify that the entered information is correct',
                    '.custom-alert.failure',
                    1500,
                );
            }
        });
    });
});

$(document).on('click', '.cancel_link', function() {
    let item = $(this).closest('.list-group-item');
    item.hide();
    let id = item.data('id');
    let type = item.data('type');
    let type_text = "evolution";
    if(type===1)
        type_text = "dependency";
    let button = $('#artifact' + id).find(".add_link." + type_text);
    button.removeClass("disabled");
    links = links.filter(function(item) {
        return !(item.artifact === id && item.type === type);
    });
});

function link(artifact, type){
    let link_ = {
        'artifact': artifact.id,
        'type': type,
    };
    links.push(link_);
    let type_text = "Evolves into";
    if(type===1)
        type_text = "Depends on";
    return `
        <div data-id="${artifact.id}" data-type="${type}" class="list-group-item">
            <small class="key ${artifact.type}">${type_text}</small>
            <div class="d-flex align-items-center">
                <div class="ml-3 strikable name">${artifact.name}</div>
                <i class="fa-solid fa-xmark cancel_link"></i>
            </div>
        </div>
    `;
}
