$(function() {
    $('#btnSignUp').click(function() {
 
        $.ajax({
            url: '/',
            data: $('#formSignUp').serialize() + "&formID=formSignUp",
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