function generateModifyPrompt(id){
    $('#' + id).slideDown()
}

function hideModForm(id){
    $('#' + id).slideUp()
}

function submitPasswordChange(id,user,pass){
    //prevent massive username/passwords
    if(user.length <= 15 && pass.length <= 15){
        var url = 'modifylogin.php';
        var data = {
            id: id,
            user: user,
            pass: pass
        };
        console.log(data);
        $.ajax({
            type: "POST",
            datatype: 'json',
            url: url,
            data: data,

            success: function(xhr, status){
                console.log(xhr);
            }
        });
    } else {
        alert("Username and password are limited to 15 characters.")
    }
}