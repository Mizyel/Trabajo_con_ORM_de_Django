google.charts.load('current', { 'packages': ['corechart'] });


$(function(){
    google.charts.setOnLoadCallback(graficar);
    $.ajaxSetup({
        header:{
            'X-CSRF-TOKEN':getCookie('csrftoken')
        }
    })
})

function getCookie(name){
    let cookieValue = null;
    if (document.cookie && document.cookie!== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;l
}


function graficar() {
    $.ajax({
        url: '/grafica1Google/',
        dataType: 'json',
        typo: 'post',
        cache:false,
        async:false,
        success: function(resultado) {
            console.log(resultado);
            var data = google.visualization.arrayToDataTable(resultado.datos);
            var options={
                title: 'Ventas por producto',
                length: 'none',
                //is3D: true,
            };
            var grafica= document.getElementById('grafica');
            var chart = new google.visualization.ColumnChart(grafica);
            chart.draw(data, options);
        }
    })

}