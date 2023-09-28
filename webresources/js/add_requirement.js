$(document).ready(function(){
    $('.add_step').click(function(){
        let sequence_div = $('#sequence');
        let id = $(this).data('id');
        id++;
        $(this).data('id', id);
        sequence_div.append('' +
            '<div id="step'+id+'" data-id="0">' +
                '<div class="d-flex">' +
                    '<span class="step_number">' + id +'</span>' +
                    '<input type="text" name="sequence'+id+'" id="benefit" class="form-control">' +
                    '<button type="button" class="btn btn-warning ml-3 sequence add_alternative_step" data-id="'+id+'" data-toggle="tooltip" title="Add an alternative step">' +
                        '<i class="fas fa-step-forward"></i>' +
                    '</button>' +
                '</div>' +
            '</div>'
        );
    });
    $(document).on('click', '.add_alternative_step', function(){
        let id = $(this).data('id');
        let step = $('#step'+id);
        let alt_id = step.data('id');
        alt_id++;
        step.data('id', alt_id);
        step.append('' +
            '<div class="d-flex">' +
                '<span class="step_number alt">' + id + '.' + alt_id + '</span>' +
                '<input type="text" name="alt_sequence'+id+'.'+alt_id+'" id="benefit" class="form-control">' +
            '</div>'
        );
    });
    $('[data-toggle="tooltip"]').tooltip();
});
