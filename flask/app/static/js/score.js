function randomInt(min, max) {
    return min + Math.floor((max - min) * Math.random());
}

$(document).ready(function() {

    $.getJSON('/score_data', function(json) {

        data = json.data
        count_solves = json.labels

        Chart.defaults.global.defaultFontColor = 'white';
        Chart.defaults.global.defaultFontStyle = 'Bold';

        var colors = ['#00e676','#ffeb3b','#b71c1c','#2196f3','#ff9800'];
        var data_solves = []

        for(var i = 0; i < data.length; i++){
            var score = [0]
            if ((data[i].solve).length != undefined){
                tmp = 0;
                for(var x = 0; x < (data[i].solve).length; x++){
                    tmp = tmp + data[i].solve[x].score
                    score.push(tmp)
                }
                data_solves.push(
                    { 
                        data: score,
                        label: data[i].name,
                        borderColor: colors[i],
                        borderWidth: 3,
                        pointBackgroundColor: colors[i],
                        fill: false
                    }
                )
            }
        }

        title = 'Top 5 user'
        if (count_solves.length == 0){
            title = 'W8 SOLVES!'
        }
        
        new Chart(document.getElementById("chLine"), {
            type: 'line',
            data: {
                labels: count_solves,
                datasets: data_solves
            },
            options: {
            title: {
                display: true,
                position: "top",
                text: title
            },
            legend: {
                display: true,
                position: "bottom"
                }
            }
        });

    });

});