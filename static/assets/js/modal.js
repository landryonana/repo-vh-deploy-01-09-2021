$(document).ready(function() {
    chart();
    $('.displ_tog').hide();
    var loadForm = function(){
        var btn = $(this);
        $.ajax({
            url:btn.attr("data-url"),
            type:'get',
            dataType:'json',
            beforeSend:function(){
                $("#modal-person .modal-content").html("");
                $('#modal-person').modal('show');
            },
            success:function(data){
                $("#modal-person .modal-content").html(data.html_form);
            }
        })
    };
    var saveForm = function() {
        var form = $(this);
        $.ajax({
            url:form.attr('action'),
            data:form.serialize(),
            type: form.attr('method'),
            dataType: 'json',
            success: function(data){
                $('.displ_tog').show();
                if(data.form_is_valid){
                    $("#person-table tbody").html(data.html_person_list);
                    $("#modal-person").modal("hide");
                    $("#is_action_ok").show();
                    if(data.is_del){
                        $("#is_action_ok").html('<span style="background: tomato;padding: 15px;display: block; width: 100%;color: #fff; text-align:center;font-size:20px;font-weight:bold; border-radius:7px;">Supression réussie</span>');
                    }

                    if(data.is_created){
                        $("#is_action_ok").html('<span style="background: #2697FF;padding: 15px;display: block; width: 100%;color: #fff; text-align:center;font-size:20px;font-weight:bold; border-radius:7px;">Ajout réussie</span>');
                    }

                    if(data.is_updated){
                        $("#is_action_ok").html('<span style="background: #70d87e;padding: 15px;display: block; width: 100%;color: #fff; text-align:center;font-size:20px;font-weight:bold; border-radius:7px;">Modification réussie</span>');
                    }
                    setTimeout(() => {
                        $("#is_action_ok").hide();
                    }, 3000);
                }else{
                    $("#modal-person .modal-content").html(data.html_form);
                }
                
            }
        })
        
        return false;
    }

    /*=========== binding ===========*/
    $(".js_create_person").click(loadForm);
    $("#modal-person").on("submit", ".js_person_create_form", saveForm)

    /*===========update personne */
    $("#person-table").on("click", ".js_update_person", loadForm);
    //$("#person-table").on("click", ".js_update_person_row", loadForm);
    $("#modal-person").on("submit", ".js_person_update_form", saveForm);

    /*///===========delte personne */
    //$("#person-table").on("click", ".js_update_person", loadForm);
    $("#person-table").on("click", ".js_delete_person_btn", loadForm);
    $("#modal-person").on("submit", ".js_person_delete_form", saveForm);

    //======================================================== SITE =============================================

    var loadFormSite = function(){
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type:'get',
            dataType:'json',
            beforeSend:function(){
                $("#modal-site .modal-content").html("");
                $("#modal-site").modal("show");
            },
            success:function(data){
                $("#modal-site .modal-content").html(data.html_form);
            }
        })
    };

    var saveFormSite = function() {
        var form = $(this);
        $.ajax({
            url: form.attr('action'),
            data: form.serialize(),
            type: form.attr('method'),
            dataType: 'json',
            success: function(data){
                $('.displ_tog').show();
                if(data.form_is_valid){
                    $("#site-table tbody").html(data.html_site_list);
                    $("#modal-site").modal("hide");
                    $("#is_action_ok").show();
                    if(data.is_del){
                        $("#is_action_ok").html('<span style="background: tomato;padding: 15px;display: block; width: 100%;color: #fff; text-align:center;font-size:20px;font-weight:bold; border-radius:7px;">Supression réussie</span>');
                    }

                    if(data.is_created){
                        $("#is_action_ok").html('<span style="background: #2697FF;padding: 15px;display: block; width: 100%;color: #fff; text-align:center;font-size:20px;font-weight:bold; border-radius:7px;">Ajout réussie</span>');
                    }

                    if(data.is_updated){
                        $("#is_action_ok").html('<span style="background: #70d87e;padding: 15px;display: block; width: 100%;color: #fff; text-align:center;font-size:20px;font-weight:bold; border-radius:7px;">Modification réussie</span>');
                    }
                    setTimeout(() => {
                        $("#is_action_ok").hide();
                    }, 3000);
                }else{
                    $("#modal-site .modal-content").html(data.html_form);
                }
            }
        })
        return false;
    }

    $(".js_create_site").click(loadFormSite);
    $("#modal-site").on("submit", ".js_site_create_form", saveFormSite);

    /*===========update site */
    $("#site-table").on("click", ".js_update_site_btn", loadFormSite);
    //$("#site-table").on("click", ".js_update_site_row", loadFormSite);
    $("#modal-site").on("submit", ".js_site_update_form", saveFormSite);

    /*///===========delete site */
    //$("#site-table").on("click", ".js_update_person", loadFormSite);
    $("#site-table").on("click", ".js_delete_site_btn", loadFormSite);
    $("#modal-site").on("submit", ".js_site_delete_form", saveFormSite);



    //=========================================================== FICHE ===============================================
     var loadFormFiche = function(){
        var btn = $(this); 
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend:function() {
                $('#modal-fiche .modal-content').html("");
                $('#modal-fiche').modal("show");
            },
            success:function(resp) {
                $('#modal-fiche .modal-content').html(resp.html_form);
            }
        })
    }

    var saveFormFiche = function(){
        var form = $(this);
        $.ajax({
            url: form.attr('action'),
            type: form.attr('method'),
            dataType: 'json',
            data: form.serialize(),
            success: function(resp){
                $('.displ_tog').show();
                if (resp.form_is_valid) {
                    $("#fiche-table tbody").html(resp.html_fiche_list);
                    $("#modal-fiche").modal("hide");
                    $("#is_action_ok").show();
                    if(resp.is_del){
                        $("#is_action_ok").html('<span style="background: tomato;padding: 15px;display: block; width: 100%;color: #fff; text-align:center;font-size:20px;font-weight:bold; border-radius:7px;">Supression réussie</span>');
                    }

                    if(resp.is_created){
                        $("#is_action_ok").html('<span style="background: #2697FF;padding: 15px;display: block; width: 100%;color: #fff; text-align:center;font-size:20px;font-weight:bold; border-radius:7px;">Ajout réussie</span>');
                    }

                    if(resp.is_updated){
                        $("#is_action_ok").html('<span style="background: #70d87e;padding: 15px;display: block; width: 100%;color: #fff; text-align:center;font-size:20px;font-weight:bold; border-radius:7px;">Modification réussie</span>');
                    }
                    setTimeout(() => {
                        $("#is_action_ok").hide();
                    }, 2000);
                } else {
                    $("#modal-fiche .modal-content").html(resp.html_form); 
                }
                
            }
        });
        return false;
    }
    //============ create fiche
    $('.js_create_fiche').click(loadFormFiche);
    $("#modal-fiche").on("submit", ".js_fiche_create_form", saveFormFiche);

    /*===========update fiche */
    $("#fiche-table").on("click", ".js_update_fiche_btn", loadFormFiche);
    //$("#fiche-table").on("click", ".js_fiche_row", loadFormFiche);
    $("#modal-fiche").on("submit", ".js_fiche_update_form", saveFormFiche);

    /*///===========delete fiche */
    //$("#site-table").on("click", ".js_update_person", loadFormSite);
    $("#fiche-table").on("click", ".js_delete_fiche_btn", loadFormFiche);
    $("#modal-fiche").on("submit", ".js_fiche_delete_form", saveFormFiche);


    //=========================================================== SEARCH ===============================================
    $("#search_input").keyup(function(){
        console.log($("#search_input").val())
        search_input = $("#search_input");
        fetch(`${search_input.attr("data-url")}`, {
            method: "post",
            body: JSON.stringify({'text_search': search_input.val()})
        }).then((resp) => resp.json()).then((data) => {
            console.log(data)
            $("#person-table tbody").html(data.html_personnes);
            $("#fiche-table tbody").html(data.html_fiches);
            $("#site-table tbody").html(data.html_sites);
            
        })
    })    

   function chart() {
        var $populationChart = $("#population-chart");
        $.get({
        url: $populationChart.data("url"),
        success: function (data) {

            console.log(data)
            var ctx = $populationChart[0].getContext("2d");

            new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [{
                backgroundColor: [
                    'rgba(75, 192, 192, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)'
                ],
                data: data.data
                }]          
            },
            options: {
                responsive: true,
                legend: {
                position: 'top',
                },
                title: {
                display: true,
                text: "Statistique d'évangélisaation"
                }
            }
            });

        }
        });   
    }

    $("#wrapconfig-heur").hide();
    $("#btn-config-heur").click(function(){
        $("#wrapconfig-heur").toggle();
    });

//======================================================================================
    var loadEvangForm = function(){
        var btn = $(this)
        $.ajax({
            url: btn.attr("data-url"),
            dataType: 'json',
            type: 'get',
            beforeSend:function(){
                $("#modal-conf .modal-content").html("");
                $("#modal-conf").modal("show");
            },
            success: function(resp){
                $("#modal-conf .modal-content").html(resp.form_evang);
            }
        })
    }


    var saveEvanForm = function(){
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            type: 'post',
            dataType: 'json',
            data: form.serialize(),
            success: function(resp){
                console.log(resp)
                if (resp.form_is_valid){
                    $("#evang_heur_infos").html(resp.evang_heur_infos);
                    $("#modal-conf").modal("hide");
                    if (resp.is_created) {
                        $("#heur_is_created_update").html("creation réussie");   
                    }else if (resp.is_updated) {
                        $("#heur_is_created_update").html("mise à jour réussie");
                    }
                    setTimeout(() => {
                        $("#heur_is_created_update").hide();
                    }, 2000);
                    
                }else{
                    $("#modal-conf .modal-content").html(resp.form_evang); 
                }
            }
        })
        return false
    }

    $("#heur_is_created_update").hide();
    //======================================CREATE EVANG============================================================
    //======================================CREATE EVANG============================================================
    //======================================CREATE EVANG============================================================
    $("#btn_ajout_heur").click(loadEvangForm);
    $("#modal-conf").on("submit", ".js_evang_create_form", saveEvanForm);

    //======================================UPDATE EVANG============================================================
    //======================================UPDATE EVANG============================================================
    //======================================UPDATE EVANG============================================================
    $("#evang_heur_infos").on("click", "#btn_update_heur", loadEvangForm);
    $("#modal-conf").on("submit", ".js_evang_update_form", saveEvanForm);

    /*///===========delete fiche */
    $("#table-evang").on("click", ".btn_delete_heur", loadEvangForm);
    $("#modal-conf").on("submit", ".js_evang_delete_form", saveEvanForm);
    


//==================== delete evangelisation
    $(".btn_delete_heur").click(function(){
        var btn = $(this);
        console.log("btn_delete_heur");
        $.ajax({
            url: btn.attr("data-url"),
            dataType: 'json',
            type: 'get',
            beforeSend:function(){
                $("#modal-conf .modal-content").html("");
                $("#modal-conf").modal("show");
            },
            success: function(resp){
                $("#modal-conf .modal-content").html(resp.form_evang);
            }
        })
    });

    $("#is_delete").hide();
    $("#modal-conf").on("submit", "#js_evang_delete_form", function(){
        $.ajax({
            url: $(this).attr("action"),
            type: 'post',
            dataType: 'json',
            data: $(this).serialize(),
            success: function(resp){
                if (resp.is_delete){
                    $("#table-evang tbody").html(resp.table_evang);
                    $("#modal-conf").modal("hide");
                    $("#is_delete").html("suppression réussie");
                    $("#is_delete").show();
                    setTimeout(() => {
                        $("#is_delete").hide();
                    }, 2000);
                    
                }else{
                    $("#modal-conf .modal-content").html(resp.form_evang); 
                }
            }
        })
        return false;
    })

});

