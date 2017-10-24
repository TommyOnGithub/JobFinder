$(document).ready( function(){
    setupSearch();
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