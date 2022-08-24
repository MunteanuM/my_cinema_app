function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

jQuery(function($){
    $(document).ready(function(){
        $("#id_city").change(function(){
            $.ajax({
                url:"/ajax/cinema/",
                type:"POST",
                data:{city: $(this).val(),},
                success: function(result) {
                    cols = document.getElementById("id_cinema");
                    cols.options.length = 0;
                    for(var k in result){
                        cols.options.add(new Option(k, result[k]));
                    }
                },
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                },
                error: function(e){
                    console.error(JSON.stringify(e));
                },
            });
        });
        $("#id_cinema").change(function(){
            $.ajax({
                url:"/ajax/hall/",
                type:"POST",
                data:{cinema: $(this).val(),},
                success: function(result) {
                    cols = document.getElementById("id_hall");
                    cols.options.length = 0;
                    for(var k in result){
                        cols.options.add(new Option(k, result[k]));
                    }
                },
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                },
                error: function(e){
                    console.error(JSON.stringify(e));
                },
            });
        });
      /*  $("#id_district").change(function(){
            $.ajax({
                url:"/admindrop/subdistricts/",
                type:"POST",
                data:{district: $(this).val(),},
                success: function(result) {
                    console.log(result);
                    cols = document.getElementById("id_subdistrict");
                    cols.options.length = 0;
                    cols.options.add(new Option("SubDistrict", "SubDistrict"));
                    for(var k in result){
                        cols.options.add(new Option(k, result[k]));
                    }
                },
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                },
                error: function(e){
                    console.error(JSON.stringify(e));
                },
            });

        });
        */
    });
});