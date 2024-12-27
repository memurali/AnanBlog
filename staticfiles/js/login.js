var showPass = true;

$(".btn-password-toggle").click(function(){
    if (showPass){
        $(".login-password").attr("type", "text");
        showPass = false;
    }else{
        $(".login-password").attr("type", "password");
        showPass = true;
    }
});

// Login 
$('#LoginForm').on('submit', function (e) {
    e.preventDefault();
    var formdata = $(this).serialize()
    $.ajax({
        url: 'login_view',
        type: "POST",
        data: formdata,
        success: function (res) {
            if (res['message'] == 'Logged in successfully') {
                Swal.fire({
                    icon: "success",
                    title: res['message'],
                });
                window.location.href = "Blogs";
            } else if (res['message'] == 'Invalid username or password') {
                Swal.fire({
                    icon: "error",
                    title: res['message'],
                });
            }
        },
    })
})

// Register 
$('#SignupForm').on('submit', function (e) {
    e.preventDefault();
    var formdata = $(this).serialize()
    $.ajax({
        url: 'signup_view',
        type: "POST",
        data: formdata,
        success: function (res) {
            console.log(res,">>>>>>>>>>>>>>>>")
            if (res['message'] == 'Your account has been created') {
                Swal.fire({
                    icon: "success",
                    title: res['message'],
                });
                window.location.href = "Login";
            } else if (res['message'] == res['message']) {
                Swal.fire({
                    icon: "error",
                    title: res['message'],
                });
            }
        },
    })
})