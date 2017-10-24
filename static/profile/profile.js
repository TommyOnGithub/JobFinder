function updateProf(){
    var proPass = 0;
    var proEmail = 0;
    if ($('#proPass').val().length > 0){
        proPass = $('#proPass').val();
    }
    if ($('#proEmail').val().length > 0){
        proEmail = $('#proEmail').val();
    }

    $.post('/updateProf', {pass: proPass, email: proEmail}, function(){
        $('#profileInfo').load(location.href+" #profileInfo>*","");
    });
}