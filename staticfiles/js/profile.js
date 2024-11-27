const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

var toastMixin = Swal.mixin({
    toast: true,
    icon: 'success',
    title: 'General Title',
    animation: false,
    background: 'black',
    position: 'top-right',
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    didOpen: (toast) => {
    toast.addEventListener('mouseenter', Swal.stopTimer)
    toast.addEventListener('mouseleave', Swal.resumeTimer)
    }
});

var loadFile = function (event) {
    var image = document.getElementById("output");
    image.src = URL.createObjectURL(event.target.files[0]);

    formdata = new FormData();
    formdata.append("file", event.target.files[0]);

    $.ajax({
        method: "POST",
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin',
        data: formdata,
        cache: false,
        processData: false,
        contentType: false,
        success: function (data){
            if(data == 'success'){
                toastMixin.fire({
                    animation: true,
                    title: 'Profile Picture Changed Successfully'
                });
            }else{
                toastMixin.fire({
                    animation: true,
                    title: 'Profile Picture Not Changed Successfully',
                    icon: 'error'
                });
            }
        },
    });
};


var changeInfo = function (){
    var user_name = $("#user_name").val();
    var user_address = $("#user_address").val();
    var user_email = $("#user_email").val();
    var user_phone = $("#user_phone").val();

    $.ajax({
        method: "POST",
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin',
        data: {user_name:user_name, user_address:user_address, user_email:user_email, user_phone:user_phone},
        success: function (data){
            if(data == 'success'){
                toastMixin.fire({
                    animation: true,
                    title: 'User Information Changed Successfully'
                });
            }else{
                toastMixin.fire({
                    animation: true,
                    title: 'User Information Not Changed Successfully',
                    icon: 'error'
                });
            }

            $('#user_name_text').text(user_name);
            $('#user_address_text').text(user_address);
            $('#user_email_text').text(user_email);
            $('#user_phone_text').text(user_phone);

            $('#user_info_close').trigger('click');
        }
    });
}

var i = 1
$(document).on('click', '.btn-add', function(){
    i++;
    $("#dynamic-field").append(
        '<tr id="row'+i+'"><td><input class="form-control" name="fields[]" type="text" placeholder="Type something" /></td><td><button id="'+i+'" class="btn btn-danger btn-remove" type="button"><span> <i class="fas fa-minus"></i> </span></button></td></tr>'
    );
});

$(document).on('click', '.btn-remove', function(){
    var btn_id = $(this).attr('id');

    $("#row"+btn_id).remove();
});

var changeDetail = function(){
    // console.log($("#u_dt_form").serialize());
    $.ajax({
        method: "POST",
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin',
        data: $("#u_dt_form").serialize(),
        success: function (data){
            if(data == 'success'){
                toastMixin.fire({
                    animation: true,
                    title: 'User Details Changed Successfully'
                });
            }else{
                toastMixin.fire({
                    animation: true,
                    title: 'User Details Not Changed Successfully',
                    icon: 'error'
                });
            }

            $('#user_detail_close').trigger('click');

            setTimeout(function(){
                location = ''
              },2000)
        }
        
    });
}

var changeSocial = function(){
    $.ajax({
        method: "POST",
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin',
        data: $("#user_social_form").serialize(),
        success: function (data){

            if(data == 'success'){
                toastMixin.fire({
                    animation: true,
                    title: 'User Social Url Changed Successfully'
                });
            }else{
                toastMixin.fire({
                    animation: true,
                    title: 'User Social Url Not Changed Successfully',
                    icon: 'error'
                });
            }

            $('#user_social_close').trigger('click');

            setTimeout(function(){
                location = ''
              },2000)
        }
        
    }); 
}