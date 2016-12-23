$('.js-like').on('click', function(){
    var $btn = $(this)
    console.log( $btn.data('id') );

    $.ajax({
        url: '/like/',
        method: 'POST',
        data:{
            id: $btn.data('id'),
            type: $btn.data('type'),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        }
    }).done( function(resp){
        console.log(resp);
        if(resp && resp.status == 'ok'){
            window.location.reload();
        }
        else{
            alert(resp.status);
        }
    });
    return false;
});

$('.js-correct').on('click', function(){
    var $btn = $(this)
    console.log( $btn.data('id') );

    $.ajax({
        url: '/correct/',
        method: 'POST',
        data:{
            id: $btn.data('id'),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        }
    }).done( function(resp){
        console.log(resp);
        if(resp && resp.status == 'ok'){
            window.location.reload();
        }
        else{
            alert(resp.status);
        }
    });
    return false;
});