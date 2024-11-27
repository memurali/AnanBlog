const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
var isPaused = false;

$(".comment-btn").click(function(){
    loggedin = $("#loggedin").val();
    
    if(loggedin != "True"){
        $(".cmnt-mssg").text("Please login");
    }else{
        comment = $(".comment").val();

        if(comment == ""){
            $(".comment").addClass("border-danger");
        }else{
            $(".comment").removeClass("border-danger");

                $.ajax({
                    method: "POST",
                    headers: {'X-CSRFToken': csrftoken},
                    mode: 'same-origin',
                    data: {add_comment:"true", comment:comment},
                    success: function (data){
                        console.log(data);
                        $(".comment").val("")
                    }
                });
        }
    }
});


setInterval(function(){ 
    blogId = $("#blogId").val();

    if(!isPaused) {
    
        $.ajax({
            method: "POST",
            headers: {'X-CSRFToken': csrftoken},
            mode: 'same-origin',
            data: {get_comment:"true", blogId:blogId},
            success: function (data){
                $(".comment-list").html(data);
            }
        });
    }

}, 10000);

$(document).on("click", '.reply-link', function(e){
    console.log("hhh")
    cmntId = $(this).attr("cmntId");

    e.preventDefault();
    isPaused = true;

    $("#rep_"+cmntId).show();
})

$("#blick").click(function(e){
    e.preventDefault();
    isPaused = false;
})

$(document).on("click", ".reply-btn", function(){
    loggedin = $("#loggedin").val();
    cmntId = $(this).attr("cmntId");
    
    if(loggedin != "True"){
        $("#rpm_"+cmntId).text("Please login");
    }else{
        comment = $("#rp_"+cmntId).val();

        if(comment == ""){
            $("#rp_"+cmntId).addClass("border-danger");
        }else{
            $("#rp_"+cmntId).removeClass("border-danger");

                $.ajax({
                    method: "POST",
                    headers: {'X-CSRFToken': csrftoken},
                    mode: 'same-origin',
                    data: {add_reply:"true", reply:comment, commentId:cmntId},
                    success: function (data){
                        console.log(data);
                        $("#rp_"+cmntId).val("")
                        $("#blick").trigger("click");
                    }
                });
        }
    }
});

$(document).on("click", ".share-btn", function(){
    $.ajax({
        method: "POST",
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin',
        data: {add_share:"true",},
        success: function (data){
            console.log(data);
        }
    });
})