$(document).ready( function(){
    setupRows();
    setupSearch();
    setupClick();
    $('#skillRadio').hide();
})

function updateProf(){
    var proPass = 0;
    var proEmail = 0;
    var skills = {};
    if ($('#proEmail').val().length > 0){
        proEmail = $('#proEmail').val();
    }
    $("#mainSkillTab tr").each(function() {
        skills[$(this)[0].children[0].innerText] = $(this)[0].children[1].innerText;
    });
    $.post('/updateProf', {email: proEmail, skills: JSON.stringify(skills)}, function(){
        $('#profileInfo').load(location.href+" #profileInfo>*","");
    });
}

function updateSkills(){
    $('#skillModal').modal('show');
}

function switchUser(){
    $('#userModal').modal('show');
}

function setUser(user){
    $.post('/loginAsUser', {user: user});
    $('#userModal').modal('hide');
    location.reload();
}

function setupClick(){
    table = $('#skillTable');
    rows = table.find('tbody tr');
    rows.on('click', function(e)
    {
        $('#skillRadio').show();
        var row = $(this);
        var value = row[0].children[1].innerText;
        var name = row[0].children[0].innerText;
        $("#rad" + value).prop("checked", true);
    });
    radio = $("#skillRadio");
    radio.on('click', function(e){
        var updateVal =$(  $(":radio[name=skillVal]:checked").prop("labels") ).text()
        var name = $('.highlight')[0].children[0].innerText;
        setRadio(name, updateVal);
    })

    table = $('#userTable');
    rows = table.find('tbody tr');
    rows.on('click', function(e)
    {
        var row = $(this);
        setUser(row[0].innerText);
    })
}

function setRadio(name, val){
    $('.highlight')[0].children[1].innerText = val;
    $("#mainSkillTab tr").each(function() {
        if (name == $(this)[0].children[0].innerText){
            $(this)[0].children[1].innerText = val;
            return false;
        }
    });
}

function setupSearch(){
    $('#skillFilt').keyup(function(e){
        /* Ignore tab key */
        var code = e.keyCode || e.which;
        if (code == '9') return;
        /* Useful DOM data and selectors */
        var input = $(this);
        var inputContent = input.val().toLowerCase();
        model = input.parents();
        table = model.find('#skillTable');
        table.show();
        rows = table.find('tbody tr');
        rows.removeClass('highlight');
        rows.removeClass('lightlight');
        $('#skillRadio').hide();
        var filteredRows = rows.filter(function(){
            var value = $(this).find('td').text().toLowerCase();
            return value.indexOf(inputContent) === -1;
        });
        table.find('tbody .no-result').remove();
        rows.show();
        filteredRows.hide();
        if (filteredRows.length == rows.length) {
            table.find('tbody').prepend($('<tr class="no-result text-center"><td>No Result found</td></tr>'));
        }
    })

    $('#userFilt').keyup(function(e){
        /* Ignore tab key */
        var code = e.keyCode || e.which;
        if (code == '9') return;
        /* Useful DOM data and selectors */
        var input = $(this);
        var inputContent = input.val().toLowerCase();
        model = input.parents();
        table = model.find('#userTable');
        table.show();
        rows = table.find('tbody tr');
        rows.removeClass('highlight');
        rows.removeClass('lightlight');
        var filteredRows = rows.filter(function(){
            var value = $(this).find('td').text().toLowerCase();
            return value.indexOf(inputContent) === -1;
        });
        table.find('tbody .no-result').remove();
        rows.show();
        filteredRows.hide();
        if (filteredRows.length == rows.length) {
            table.find('tbody').prepend($('<tr class="no-result text-center"><td>No Result found</td></tr>'));
        }
    })
}

function setupRows(){
    table = $('#skillTable');
    rows = table.find('tbody tr');
    rows.on('click', function(e){
        var row = $(this);
        rows.removeClass('highlight');
        rows.removeClass('lightlight');
        row.addClass('highlight');
    })
    rows.on('mouseenter', function(e)
    {
        var row = $(this);
        if ($(row).hasClass( "highlight" ))
        {
            rows.removeClass('lightlight');
        }
        else
        {
            rows.removeClass('lightlight');
            row.addClass('lightlight');
        }
    })
    table = $('#userTable');
    rows = table.find('tbody tr');
    rows.on('click', function(e){
        var row = $(this);
        rows.removeClass('highlight');
        rows.removeClass('lightlight');
        row.addClass('highlight');
    })
    rows.on('mouseenter', function(e){
        var row = $(this);
        if ($(row).hasClass('highlight')){
            rows.removeClass('lightlight');
        }
        else
        {
            rows.removeClass('lightlight');
            row.addClass('lightlight');
        }
    })
}