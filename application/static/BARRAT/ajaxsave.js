function getAns(o){
    //modificar según lo que necesito de las caractricas de la prueba
    let answers = "";
    
    o.forEach(function(element){
        answers = answers.concat(element.checked?"1":"0");
    });
    return answers;
}

function ajaxsave(){
    let answers = 0;
        //cambiar la obtencion de los elementos, en mi caso seria botones
        const inputs = document.querySelectorAll("input[type='radio']");
        
        answers = getAns(inputs);
        console.log(answers);

        //AJAX POST
        $.ajax({
            type: "POST",            
            //se modifica el url, se tiene ver en url.py
            url: "ajaxSave/",
            dataType: "json",
            data: {
                "answers": answers,
            },
            success: function (data) {
                console.log("datos guardados");
                console.log(data.message)
            }
        })
}

$(document).ready(function () {
    console.log("all good mate for now");

    //CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
})