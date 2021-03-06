function is_greater_than_today(dt) {
	dt.setHours(0,0,0,0);
	today = new Date();
	today.setHours(0,0,0,0);
	
	if (dt >=today) return today; else return dt;
}

function set_datepicker(date1, date2) {
	$('#datepicker1').datepicker('setDate', date1);
	$('#datepicker2').datepicker('setDate', date2);
}

function google_chart(list, title){                                                               
  google.charts.load('current', {'packages':['corechart']});                               
  google.charts.setOnLoadCallback(drawChart);                                              
                                                                                           
    function drawChart() {                                                                 
      var data = google.visualization.arrayToDataTable(list);                              
                                                                                           
      var options = {                                                                      
        title: title,
        titleTextStyle: {
            color: '333333',
            fontName: 'Arial',
            fontSize: 30
          },
        hAxis: {title: '날짜',  titleTextStyle: {color: '#333'}, slantedTextAngle:45},                                                                                       
        fontSize: 12,
        'height':500,
        pointSize: 7,
        pointShape: { type: 'star', sides: 5, dent: 0.5 }
      };                                                                                   
                                                                                           
      var chart = new google.visualization.AreaChart(document.getElementById('chart_div'));
      chart.draw(data, options);                                                           
    }			                                                                           
}                                                                                          

$(document).ready(function() {
	//date picker 설정
    $( ".datepicker" ).datepicker({
    	changeMonth: true,
    	changeYear: true,
    	dateFormat: 'yy-mm-dd',
    	maxDate: 0
    });

    //datepicker 클릭 이벤트
    $('#datepicker1').datepicker("option", "onClose", function ( selectedDate ) {
    	$("#datepicker2").datepicker( "option", "minDate", selectedDate );
    });
    $('#datepicker2').datepicker("option", "onClose", function ( selectedDate ) {
    	$("#datepicker1").datepicker( "option", "maxDate", selectedDate );
    });
});

function button_disable(dt) {
	dt.setHours(0,0,0,0)
	today = new Date();
	today.setHours(0,0,0,0);
	if (dt.getTime() == today.getTime()) {
		$('#next').attr("disabled","disabled")
	}
	else {
		$('#next').removeAttr("disabled")
	}
}
function ajax_chart(is_update_article, target_page) {
	var stock_id = $("#stock_input").val().match(/\d{6}/g);
	var date1 = $('#datepicker1').val();
	var date2 = $('#datepicker2').val();
	var arr = [stock_id, date1, date2, ''];
	var parameter = arr.join('/');
	var url = '/board/chart/' + parameter;

	$.ajax ({
		type:"GET",
		url: url,
		data:{'is_update_article': is_update_article, 'target_page':target_page},
		success: function (response) {
			$("#article-div").empty();
			$("#article-div").append(response.article_html);
			if (response.chart_update){
				set_datepicker(response.date1,response.date2);
				$("#stock_iniput").val(response.stock_str);
				
				var list = JSON.parse("[" + response.price_list + "]");
				google_chart(list, response.stock_str);				
			}
		},
		error: function(jqXHR, textStatus, errorThrown) {
		    if(jqXHR.status==404) {
		        alert('올바른 값을 입력해주세요');
		    }
		    else alert(jqXHR + "\n" + textStatus + "\n" + errorThrown);
		}
	});                         
}

function date_form(dt) {
	return dt.getYear() + "-" + dt.getMonth() + "-" + dt.getDate();
}


function chart_button(x) {
	if (x < 0) {
		dt1 = new Date($("#datepicker1").val());
	}
	else {
		dt1 = new Date($("#datepicker2").val());
	}
	dt2 = new Date(dt1.getTime());
	dt2.setDate(dt2.getDate() + x)
	
	dt_1 = is_greater_than_today(dt1);
	dt_2 = is_greater_than_today(dt2);
	
	if (dt_1.getTime() > dt_2.getTime()) {
		set_datepicker(dt_2, dt_1);
		ajax_chart('',1);
		button_disable(dt_1);
	}
	else {
		set_datepicker(dt_1, dt_2);			
		ajax_chart('',1);
		button_disable(dt_2);
	}
}
