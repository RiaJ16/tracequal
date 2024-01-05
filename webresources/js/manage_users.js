$(document).ready(function() {
    $('#username_input').on('input', function(){
        let input_text = $(this).val().trim();
        let csrftoken = $("[name='csrfmiddlewaretoken']").val();
        if (input_text !== '') {
            $.ajax({
                url: '/autocomplete_user/',
                method: 'POST',
                data: { query: input_text },
                headers: {
                    'X-CSRFToken': csrftoken
                },
                success: function(response) {
                    let suggestions = response.usernames;
                    let suggestion_list = '';
                    suggestions.forEach(function(username) {
                        suggestion_list += `<option>${username}</option>`;
                    });
                    $('#username_list').html(suggestion_list);
                }
            });
        } else {
            $('#username_list').html('');
        }
    });
    let add_button = $('#add_button');
    add_button.hover(
        function(){
            $('.fa-solid.fa-user-plus').addClass("hovered");
        },
        function(){
            $('.fa-solid.fa-user-plus').removeClass("hovered");
        }
    );
    add_button.click(function(){
        let csrftoken = $("[name='csrfmiddlewaretoken']").val();
        let name = $('#username_input').val().trim();
        let project_id= parseInt($("#project_id").val());
        $.ajax({
            url: '/add_user_project/',
            method: 'POST',
            data: {project_id: project_id, username:name},
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function(response){
                let tbody = $("#users_table tbody");
                let total_users_element = $("#total_users");
                total_users_element.data("total", total_users_element.data("total")+1);
                tbody.append("<tr>" +
                    "<td>"+response.name+"</td>" +
                    "<td>"+response.lastname+" "+response.lastname2+"</td>" +
                    "<td>@"+response.username+"</td>" +
                    "<td>" +
                        "<div class='btn-group'>" +
                            "<a role='button' class='btn btn-secondary btn-sm dropdown-toggle' type='button' data-bs-toggle='dropdown' aria-expanded='false'>" +
                                response.role +
                            "</a>" +
                            "<ul class='dropdown-menu' data-user_id='" + response.id + "' data-project_id='" + project_id +"'>" +
                                "<li><a class='dropdown-item' data-role='user' href='#'>User</a></li>" +
                                "<li><a class='dropdown-item' data-role='admin' href='#'>Admin</a></li>" +
                            "</ul>" +
                        "</div>" +
                    "</td>" +
                    "<td><a class='remove_button' href='javascript:void(0)' data-user_id='" + response.id + "'>" +
                        "<i class='fa-solid fa-user-minus'></i>" +
                    "</a></td>" +
                "</tr>");
            },
            error: function(response){
                alert_appear(
                    'Such user cannot be added',
                    '.custom-alert.failure',
                    1500,
                );
            }
        });
    });
    let users_table = $('#users_table');
    users_table.on('click', '.remove_button', function(event){
        event.preventDefault();
        let confirmation_dialog= $('#confirmation_dialog');
        let button = $(this);
        let project_id= parseInt($("#project_id").val());
        confirmation_dialog.data('project_id', project_id);
        confirmation_dialog.data('user_id', button.data('user_id')).show();
        $('.custom-alert-info').html('Are you sure you want to remove this user from the project?');
    });
    users_table.on('click', '.dropdown-item', function(event){
        const atag = $(this);
        let role = atag.data('role');
        let dropdown_menu = atag.closest('.dropdown-menu');
        let csrftoken = $("[name='csrfmiddlewaretoken']").val();
        $.ajax({
            url: '/change_user_role/',
            method: 'POST',
            data: {
                project_id: dropdown_menu.data('project_id'),
                user_id: dropdown_menu.data('user_id'),
                new_role: role,
            },
            headers: {
                'X-CSRFToken': csrftoken,
            },
            success: function (response){
                dropdown_menu.siblings('.dropdown-toggle').text(role);
            },
            error: function (response){
                alert_appear(
                    'Such user cannot be added',
                    '.custom-alert.failure',
                    1500,
                );
            }
        });
    });
    $('#confirm_button').click(function() {
        let confirmation_dialog= $('#confirmation_dialog');
        let csrftoken = $("[name='csrfmiddlewaretoken']").val();
        confirmation_dialog.hide();
        let project_id = confirmation_dialog.data('project_id');
        let user_id = confirmation_dialog.data('user_id');
        let button = $('.remove_button[data-user_id='+user_id+']');
        $.ajax({
            url: '/remove_user_project/',
            method: 'POST',
            data: {project_id: project_id, user_id: user_id},
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function (response) {
                button.closest('tr').remove();
            },
            error: function (response) {
                alert_appear(
                    'Such user cannot be removed',
                    '.custom-alert.failure',
                    1500,
                );
            }
        });
    });
    let confirmation_dialog= $('#confirmation_dialog');
    $('#cancel_button').click(function(){
        confirmation_dialog.hide();
    });
});
