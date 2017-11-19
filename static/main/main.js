$(document).ready( function(){
    setupSearch();
    setupRows();
    $('#majorCheck').prop('checked', true);
    $('#jobCheck').prop('checked', true);
})
function setupSearch(){
    $('#searchFilt').keyup(function(e){
        /* Ignore tab key */
        var code = e.keyCode || e.which;
        if (code == '9') return;
        /* Useful DOM data and selectors */
        var input = $(this);
        var inputContent = input.val().toLowerCase();
        model = input.parents();
        if ($('#jobCheck').is(':checked')){
            table = model.find('#jobTable');
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
        }
        else{
            table = model.find('#jobTable');
            table.hide();
        }
        if ($('#majorCheck').is(':checked')){
            table = model.find('#majorTable');
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
        }
        else{
            table = model.find('#majorTable');
            table.hide();
        }
    })
}

$(function(){
    $('#majorCheck').on('click', function(e){
        $('#searchFilt').keyup();
    })
    $('#jobCheck').on('click', function(e){
        $('#searchFilt').keyup();
    })
});

function logout(){
    window.location.href = ("logout");
}

function showInfo(header, description){
    $('#infoTitle').text(header);
    $('#description').text(description);
    $('#infoModal').modal('show');
}

function runMatch(){
    $('#infoModal').modal('hide');
    $.post('/runMatch', {name: $('#infoTitle').text()});
    window.location.href = ("results");
}

function setupRows(){
    mtable = $('#majorTable');
    mrows = mtable.find('tbody tr');
    jtable = $('#jobTable');
    jrows = jtable.find('tbody tr');

    mrows.on('click', function(e){
        var row = $(this);
        mrows.removeClass('highlight');
        mrows.removeClass('lightlight');
        jrows.removeClass('highlight');
        jrows.removeClass('lightlight');
        row.addClass('highlight');
        showInfo("Degree - " + row[0].innerText, row[0].getAttribute("data-desc"));
    })
    mrows.on('mouseenter', function(e)
    {
        var row = $(this);
        if ($(row).hasClass( "highlight" ))
        {
            mrows.removeClass('lightlight');
            jrows.removeClass('lightlight');
        }
        else
        {
            mrows.removeClass('lightlight');
            jrows.removeClass('lightlight');
            row.addClass('lightlight');
        }
    })
    jrows.on('click', function(e){
        var row = $(this);
        jrows.removeClass('highlight');
        jrows.removeClass('lightlight');
        mrows.removeClass('highlight');
        mrows.removeClass('lightlight');
        row.addClass('highlight');
        showInfo("Job - " + row[0].innerText, row[0].getAttribute("data-desc"));
    })
    jrows.on('mouseenter', function(e)
    {
        var row = $(this);
        if ($(row).hasClass( "highlight" ))
        {
            jrows.removeClass('lightlight');
            mrows.removeClass('lightlight');
        }
        else
        {
            jrows.removeClass('lightlight');
            mrows.removeClass('lightlight');
            row.addClass('lightlight');
        }
    })
}