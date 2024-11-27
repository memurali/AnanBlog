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