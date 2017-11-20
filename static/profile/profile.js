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

function showModal(){
    $('#userModal').modal('show');
}

function switchUser(){
    table = $('#userTable');
    rows = table.find('tbody tr');
    $(rows).each(function(){
        var row = $(this);
        if ($(row).hasClass("highlight")){
            setUser(row[0].innerText);
        }
    });
}

function showPFaculty(){
    table = $('#userTable');
    rows = table.find('tbody tr');
    $(rows).each(function(){
        var row = $(this);
        if ($(row).hasClass("highlight")){
            if ($("#setFBtn").text() === "Set Faculty"){
                setFaculty(row[0].innerText);
            }
            else{
                unsetFaculty(row[0].innerText);
            }
        }
    });
}

function setFaculty(user){
    $.post('/setFaculty', {user: user, set:1});
    $('#userModal').modal('hide');
    location.reload();
}

function unsetFaculty(user){
    $.post('/setFaculty', {user: user, set:0});
    $('#userModal').modal('hide');
    location.reload();
}

function deleteTarget(){
    table = $('#userTable');
    rows = table.find('tbody tr');
    $(rows).each(function(){
        var row = $(this);
        if ($(row).hasClass("highlight")){
            deleteUser(row[0].innerText);
        }
    });
}

function setUser(user){
    $.post('/loginAsUser', {user: user});
    $('#userModal').modal('hide');
    location.reload();
}

function deleteUser(user){
    if (confirm("Are you sure you want to delete your account?")){
        $.post('/deleteTarget', {user: user}, function(){
            $('#userModal').modal('hide');
            location.reload();
        });
    };
}

function searchStats(){
    $.post('/statistics', function(stats){
        window.URL = window.webkitURL || window.URL;
        var contentType = 'text/csv';
        stats = JSON.parse(stats);
        var newString = [];
        var string;
        var key = 0;
        stats.map(function(arrayCell){
            string = arrayCell[0] + "," + arrayCell[1];
            newString = newString + "\n" + string;
        })
        var csvFile = new Blob([newString], {type: contentType});
        var a = document.createElement('a');
        a.download = 'JobFinderStats.csv';
        a.href = window.URL.createObjectURL(csvFile);
        a.dataset.downloadurl = [contentType, a.download, a.href].join(':');
        a.click();
    });
}

function deleteSelf(){
    if (confirm("Are you sure you want to delete your account?")){
        $.post('/deleteUser');
        window.location.href = 'main';
    };
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
        if (row[0].getAttribute("data-user") == "True"){
            $('#simBtn').prop("disabled", true);
            $('#setFBtn').text("Unset Faculty");
        }
        else{
            $("#setFBtn").text("Set Faculty");
            $('#simBtn').prop("disabled", false);
        }
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

    $('#setFFilt').keyup(function(e){
        /* Ignore tab key */
        var code = e.keyCode || e.which;
        if (code == '9') return;
        /* Useful DOM data and selectors */
        var input = $(this);
        var inputContent = input.val().toLowerCase();
        model = input.parents();
        table = model.find('#setFTable');
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
    rowsS = table.find('tbody tr');
    rowsS.on('click', function(e){
        var row = $(this);
        rowsS.removeClass('highlight');
        rowsS.removeClass('lightlight');
        row.addClass('highlight');
    })
    rowsS.on('mouseenter', function(e)
    {
        var row = $(this);
        if ($(row).hasClass( "highlight" ))
        {
            rowsS.removeClass('lightlight');
        }
        else
        {
            rowsS.removeClass('lightlight');
            row.addClass('lightlight');
        }
    })
    table = $('#userTable');
    rowsU = table.find('tbody tr');
    rowsU.on('click', function(e){
        var row = $(this);
        rowsU.removeClass('highlight');
        rowsU.removeClass('lightlight');
        row.addClass('highlight');
    })
    rowsU.on('mouseenter', function(e){
        var row = $(this);
        if ($(row).hasClass('highlight')){
            rowsU.removeClass('lightlight');
        }
        else
        {
            rowsU.removeClass('lightlight');
            row.addClass('lightlight');
        }
    })
    table = $('#setFTable');
    rowsF = table.find('tbody tr');
    rowsF.on('click', function(e){
        var row = $(this);
        rowsF.removeClass('highlight');
        rowsF.removeClass('lightlight');
        row.addClass('highlight');
    })
    rowsF.on('mouseenter', function(e){
        var row = $(this);
        if ($(row).hasClass('highlight')){
            rowsF.removeClass('lightlight');
        }
        else
        {
            rowsF.removeClass('lightlight');
        }
    })
}