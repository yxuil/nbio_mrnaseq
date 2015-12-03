function displayTable(data) {
	$('#tab-1').hide();
	$('#tab-2').hide();
	$('#tab-3').hide();
	$('#tab-4').hide();
	$('#tab-5').hide();
	$('#tab-6').hide();
	$('#tab-7').hide();
	$('#tab-8').hide();
	$('#tab-9').hide();
	$('#tab-10').hide();
	$('#tab-11').hide();
	$('#tab-12').hide();
	$('#tab-13').hide();
	$('#tab-14').hide();
	$('#tab-15').hide();
	$('#tab-16').hide();
	if(data == null) {
		$('#' + $('#tableSelect').val()).show();
	}
	else {
		$('#' + data).show();
		$('#tableSelect').val(data);
	}
}