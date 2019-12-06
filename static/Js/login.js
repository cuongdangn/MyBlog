$(function() {
    $('#btnLogin').click(function() {
 
        $.ajax({
            url: '/',
            data: $('#formLogin').serialize() + "&formID=formLogin",
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});