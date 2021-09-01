$(document).ready(function(){
    $("#add_evang").click(function(){
        $(".rempl_descrip").hide();
        $("#id_evang_form").removeClass("evang_form");
    })

    $("#id_evang_form_annul").click(function(){
        $("#id_evang_form").addClass("evang_form");
        $(".rempl_descrip").show();
    })
    
    var loadPersonneDetailImage = function(){
        var btn = $(this); 
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend:function() {
                $('#modal-personne-detail .modal-content').html("");
                $('#modal-personne-detail').modal("show");
            },
            success:function(resp) {
                $('#modal-personne-detail .modal-content').html(resp.detail_personne);
            }
        })
    }

    $('.personne-btn-detail').click(loadPersonneDetailImage);



    $(".evang_detail").click(function(){
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend:function() {
                $('#modal-evang-detail .modal-content').html("");
                $('#modal-evang-detail').modal("show");
            },
            success:function(resp) {
                $('#modal-evang-detail .modal-content').html(resp.evang_detail);
            }
        })
    });



//==============================================================modal participant add
    $("#add_autre_participant").click(function(){
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            csrfmiddlewaretoken: '{{ csrf_token }}',
            beforeSend:function() {
                $('#modal-ajout-autre-participant .modal-content').html("");
                $('#modal-ajout-autre-participant').modal("show");
            },
            success:function(resp) {
                $('#modal-ajout-autre-participant .modal-content').html(resp.form_html);
            }
            
        })
    })

    //==============================================================modal site add
    $("#ajout_modal_site").click(function(){
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            csrfmiddlewaretoken: '{{ csrf_token }}',
            beforeSend:function() {
                $('#modal-ajout-site .modal-content').html("");
                $('#modal-ajout-site').modal("show");
            },
            success:function(resp) {
                $('#modal-ajout-site .modal-content').html(resp.form_html);
            }
            
        })
    })
      
      
});