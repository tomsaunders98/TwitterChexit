

$(document).ready(function(){ //I think there are better ways to do this in boostrap but this wasn't developed in 4.
    //Keep track of last scroll
    var lastScroll = 0;
    $(window).scroll(function(event){  
        //Sets the current scroll position
        var st = $(this).scrollTop();
        //Determines up-or-down scrolling
        if (st > lastScroll){//Downwards scroll
            var currentItem = $(".navbar-nav a.active").attr('href'); //cheeky hack for tapping into Bootstrap scrollspy
            if (currentItem == "#section3"){
              $(".visual2").css('background-image', 'url(img/visual2-2.png)');
            }
           
        }
        else {// Upwards scroll
          var currentItem = $(".navbar-nav a.active").attr('href');
          if (currentItem == "#section2"){
              $(".visual2").css('background-image', 'url(img/visual2-1.png)');
          }
        }
        //Updates scroll position
        lastScroll = st;
    });
    // Simple fancy scroll animation for inpage links
  $(".nav-link").click(function() {
    var goto = $(this).attr('href');
    $([document.documentElement, document.body]).animate({
        scrollTop: $(goto).offset().top
    }, 1000);
  });
});
//Bar Charts function, define styling layout colours here. 
function CreateGraph(Titles, Values, location){
  if (Titles.length == 2){
    var data = [
                {
                  x: Titles,
                  y: Values,
                  type: 'bar',
                  marker:{
                    color: ['rgba(52, 94, 235, 0.8)', 'rgba(235, 64, 52, 0.8)']
                  },
                  text: Values.map(String),
                  textposition: 'auto',
                  hoverinfo: 'none'
                }
              ];
            
  }else{
    var data = [
                {
                  x: Titles,
                  y: Values,
                  type: 'bar',
                  text: Values.map(String),
                  textposition: 'auto',
                  hoverinfo: 'none'
                }
              ];
  }
  var layout = {
                  xaxis: {
                    showgrid: false
                  },
                  font: {
                        family: 'Times New Roman, Times, serif',
                        size: 18,
                        color: '#121212'
                      },
                  yaxis: {
                    showgrid: false,
                    title: {
                      text: 'Number of Hashtags',
                    }
                  },
                  margin: {
                      t: 0
                      }
              };
  return Plotly.newPlot(location, data, layout, {staticPlot: true, responsive: true});
  //return [data, layout];
}