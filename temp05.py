import json
import re


data='''
	$(function () {
		$('#dtPickerFrom').datetimepicker({
			format: 'Y-m-d H:i',
			onShow: function (ct) {
				// 巜掕壜擻擔偼To傑偱
				var strTo = jQuery('#dtPickerTo').val().split(" ")[0].replace(/-/g, "/");
				this.setOptions({
					maxDate: jQuery('#dtPickerTo').val() ? strTo : false
				})
			}
		});
		$('#dtPickerTo').datetimepicker({
			format: 'Y-m-d H:i',
			onShow: function (ct) {
				// 巜掕壜擻擔偼From偐傜崱擔傑偱
				var strFrom = jQuery('#dtPickerFrom').val().split(" ")[0].replace(/-/g, "/");
				myD = new Date();
				myYear = myD.getFullYear();
				myMonth = myD.getMonth() + 1;
				myDate = myD.getDate();
				this.setOptions({
					minDate: jQuery('#dtPickerFrom').val() ? strFrom : false,
					maxDate: myYear + "/" + myMonth + "/" + myDate
				})
			}
		});
	});


$(function () {
	var interval=600*1000;
    // 僞僀儅乕僙僢僩
	setTimer();
	function setTimer(){
		timerId=setTimeout(timeProcess,interval);
		$('#countdown').countdown({until: +600, format: 'MS', layout: '{mn}{sep}{snn}'}); 
		return false;
	}
	// 僞僀儅乕張棟
	// 峏怴儃僞儞傪墴偡
	function timeProcess(){
		document.getElementById('LinkButtonRefresh').click();
		timerId=setTimeout(arguments.callee,interval);
	}
	// 僇僂儞僩僟僂儞僋儕僢僋偱帺摦峏怴掆巭
	$('#countdown').on('click', function (event) {
		$('#countdown').css('visibility', 'hidden');
		$('#countdown').countdown('destroy');
		clearTimeout(timerId);
	});
});


	$(document).ready(function () {

		function exportTableToCSV($table, filename) {
			var bom = new Uint8Array([0xEF, 0xBB, 0xBF]);
			var csvData = "";
			var $target = ["th", "td"];

			for (var k = 0; k < 2; k++) {
				var tempFind = 'tr:has(' + $target[k] + '):not(.noexport)';
				var $rows = $table.find(tempFind),

				// Temporary delimiter characters unlikely to be typed by keyboard
				// This is to avoid accidentally splitting the actual contents
				tmpColDelim = String.fromCharCode(11), // vertical tab character
				tmpRowDelim = String.fromCharCode(0), // null character

				// actual delimiter characters for CSV format
				colDelim = '","',
				rowDelim = '"\r\n"',

				// Grab text from table into CSV formatted string
				csv = '"' + $rows.map(function (i, row) {
            		var $row = $(row),
						$cols = $row.find($target[k]);

            		return $cols.map(function (j, col) {
            			var $col = $(col),
							text = $col.text();

            			return text.replace(/"/g, '""').replace(/^\xA0/g,''); // escape double quotes	// 愭摢偵僑儈(0xA0)偑偮偔偙偲偑偁傞偐傜徚偡

            		}).get().join(tmpColDelim);

				}).get().join(tmpRowDelim)
					.split(tmpRowDelim).join(rowDelim)
					.split(tmpColDelim).join(colDelim) + '"',

				csvData = csv.length > 2 ? csvData + csv + "\r\n" : csvData;
			}

			var ua = navigator.userAgent; // 儐乕僓乕僄乕僕僃儞僩傪戙擖
			if (ua.match("MSIE") || ua.match("Trident")) { //MSIE傑偨偼Trident偑擖偭偰偄偨傜
				if (window.navigator.msSaveBlob) {
					var blob = new Blob([bom,csvData], { type: "application/csv;charset=utf-8;" });
					navigator.msSaveBlob(blob, filename);
				}
				else {
					alert('This feature is available in IE10 or more');
				}
			}
			else {
				csvData = "data:application/csv;charset=utf-8," + encodeURIComponent(csvData);
				$(this).attr({
					"href": csvData,
					"target": "_blank",
					"download": filename
				});
			}
		}

		// This must be a hyperlink
		$(".export").on('click', function (event) {
			var ua = navigator.userAgent; // 儐乕僓乕僄乕僕僃儞僩傪戙擖
			if (ua.match("MSIE") || ua.match("Trident")) { //MSIE傑偨偼Trident偑擖偭偰偄偨傜
				if (window.navigator.msSaveBlob) {
				}
				else {
					alert('This feature is available in IE10 or more');
					return;
				}
			}
			// CSV
			if ($(this).attr('data-exporttarget') != null) {
				var tableId = '#' + $(this).attr('data-exporttarget');
				var exportFile = $(this).attr('data-exportfile') + '@' + $('#LabelLine').text() + '{' + $('#dtPickerFrom').val() + '}~{' + $('#dtPickerTo').val() + '}.csv';
				exportTableToCSV.apply(this, [$(tableId), exportFile]);
			}

			// IF CSV, don't do event.preventDefault() or return false
			// We actually need this to be a typical hyperlink
		});
	});




	$(function () {
		$("#dl-xlsx").css("visibility","visible");
		$("#dl-xlsx").on('click', function (event) {
			var wopts = {
				bookType: 'xlsx',
				bookSST: false,
				type: 'binary'
			};

			var workbook = {SheetNames: [], Sheets: {}};

			$('table.table-to-export').each(function (index,currentValue) {
				// sheet_to_workbook()偺幚憰傪嶲峫偵婰弎
				var n = currentValue.getAttribute('data-sheet-name');
				if (!n) {
					n = 'Sheet' + index;
				}
				workbook.SheetNames.push(n);
				workbook.Sheets[n] = XLSX.utils.table_to_sheet(currentValue, wopts);
			});

			var wbout = XLSX.write(workbook, wopts);

			function s2ab(s) {
				var buf = new ArrayBuffer(s.length);
				var view = new Uint8Array(buf);
				for (var i = 0; i != s.length; ++i) {
					view[i] = s.charCodeAt(i) & 0xFF;
				}
				return buf;
			}

			var exportfile = $('#TabTitle').text() + '@' + $('#LabelLine').text() + '{' + $('#dtPickerFrom').val() + '}~{' + $('#dtPickerTo').val() + '}.xlsx';

			saveAs(new Blob([s2ab(wbout)], {type: 'application/octet-stream'}), exportfile);
		});
	});


	function CheckInput() {
		var re = /\d\d\d\d-\d\d-\d\d \d\d:\d\d/;
		if (re.test(document.getElementById('dtPickerFrom').value) == false || re.test(document.getElementById('dtPickerTo').value) == false) {
			alert('Date and time of the wrong format.\n\nExample\n2016-01-01 01:01');
			return false;
		}
		return true;
	}


//<![CDATA[
var theForm = document.forms['TactInfo'];
if (!theForm) {
    theForm = document.TactInfo;
}
function __doPostBack(eventTarget, eventArgument) {
    if (!theForm.onsubmit || (theForm.onsubmit() != false)) {
        theForm.__EVENTTARGET.value = eventTarget;
        theForm.__EVENTARGUMENT.value = eventArgument;
        theForm.submit();
    }
}
//]]>


<!--
	// 惗嶻枃悢偺僇僂儞僩傪儕僙僢僩偟傑偡丅
	function ConfirmCountReset(strMsg)
	{
		if (window.confirm(strMsg))
			window.location.href = "./Trend.aspx?Reset=1";
	}
	
	function CancelEnterKeySubmit()
	{
		// ENTER僉乕墴壓帪偵儊僯儏乕偑偨偨傓審偺懳嶔
		var src = window.event.srcElement;
		if (13 == event.keyCode)
		{
			if ('' == src.type)
				src.click();
			else if ('submit' != src.type  && 'button' != src.type && 'textarea' != src.type)
				return false;
		}
	}
// -->


		<!-- 
		function DispManual(form)
		{
			var id = form.McManualList.selectedIndex;
			var strPath = form.McManualList.options[id].value;
			if ("" != strPath)
				window.open(strPath, "_blank");
		}
		// -->
		



			$(function () {
				var ua = navigator.userAgent.toLowerCase();
				var ver = navigator.appVersion.toLowerCase();

				$('#clock_hou').jClocksGMT({ title: 'China', offset: '8', timeformat: 'H:mm', date: true, dateformat: 'YYYY/M/D', imgpath: 'js/jClocksGMT-master/' });
			});
		



										$(function () {
											$('#ModGraph').highcharts({
												chart: { type: 'column'	},
												title: { text: 'Module Utilization' },
											//	subtitle: { text: '<span style='visibility:hidden'>(Last 10 minutes)</span>' },
												credits : { enabled : false },
												xAxis: {
													categories: ['M1','M2','M3','M4','M5']
												},
												yAxis: {
													min: 0,
													title: {
														text: 'percentage'
													}
												},
												tooltip: {
													pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.percentage:.0f}%)<br/>',
													shared: true
												},
												plotOptions: {
													column: {
														stacking: 'percent',
														dataLabels: {
															enabled: true,
															color: 'white',
															formatter:function(){return this.percentage>=5?(this.percentage).toFixed(0)+'':'';}
														}
													}
												},
												legend: {
													borderWidth: 1,
													borderRadius: 5,
													shadow: false
												},
												series: [
													{name: 'Product',color: '#1E90FF',data: [20,183,180,224,232]},{name: 'Wait Previous',color: '#32CD32',data: [10,2,2,3,5]},{name: 'Wait Next',color: '#9ACD32',data: [570,415,418,373,135]},{name: 'Changeover',color: '#BDB76B',data: [0,0,0,0,88]},{name: 'Part Supply',color: '#808000',data: [0,0,0,0,120]},{name: 'Machine Error',color: '#FF4500',data: [0,0,0,0,16]},{name: 'Operator Downtime',color: '#FF8C00',data: [0,0,0,0,2]},{name: 'Maintenance',color: '#800080',data: [0,0,0,0,0]},{name: 'Other',color: '#c0c0c0',data: [0,0,0,0,2]}
												]
											});
										});
									

										$(function () {
											$('#LineGraph').highcharts({
												chart: {
													plotBackgroundColor: null,
													plotBorderWidth: null,
													plotShadow: false
												},
												title: { text: 'Line Utilization' },
											//	subtitle: { text: '<span style='visibility:hidden'>(Last 10 minutes)</span>' },
												credits : { enabled : false },
												tooltip: {
        											pointFormat: '<b>{point.percentage}%</b>',
													valueDecimals: 0
												},
												plotOptions: {
													pie: {
														allowPointSelect: true,
														cursor: 'pointer',
														dataLabels: {
															enabled: false,
															color: '#000000',
															connectorColor: '#000000',
															formatter: function() {
																return '<b>'+ this.point.name +'</b>: '+ (Math.floor(this.percentage*10) / 10) +' %';
															}
														},
														size: '150%',
														showInLegend: true,
														dataLabels: {
															enabled: false,
															distance:-30,
															formatter:function(){
																return (this.percentage).toFixed(0)+'%';
															}
														}
													}
												},
												legend: {
												    borderWidth: 1,
												    borderRadius: 5,
												    shadow: false
												},
												series: [
													{
														type: 	'pie',
														data: [
															{name:'Product',color:'#1E90FF', y:839,dataLabels:{enabled:true,color:'white'} },{name:'Wait Previous',color:'#32CD32', y:22 },{name:'Wait Next',color:'#9ACD32', y:1911,dataLabels:{enabled:true,color:'white'} },{name:'Changeover',color:'#BDB76B', y:88 },{name:'Part Supply',color:'#808000', y:120 },{name:'Machine Error',color:'#FF4500', y:16 },{name:'Operator Downtime',color:'#FF8C00', y:2 },{name:'Maintenance',color:'#800080', y:0 },{name:'Other',color:'#c0c0c0', y:2 }
														]
													}
												]
											});
										});
									'''


a=re.search(r'series: \[(.*?)\t\].*?',data,re.M|re.S).group(1).strip()

print(a)

b=re.findall(r'data: (.*?)\}',a)

print(b)
print(type(b))
