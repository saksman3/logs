
//////
$(function() {
  $("#search").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#tbl > tbody > tr").filter(function() {  $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      console.log("xxxxx");
    });
  });
});
