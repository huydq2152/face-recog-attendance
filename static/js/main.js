$(document).ready(function () {
  var selectId = $("#selectId");
  var encodeFaceBtn = $("#encodeFaceBtn");

  $.ajax({
    url: "/get_all_person_id",
    type: "GET",
    contentType: "application/json",
  }).done(function (data) {
    let person_ids = data.person_ids;
    $.each(person_ids, function (_index, item) {
      var option = $("<option>")
        .attr("value", item)
        .text(`Người có id = ${item}`);
      selectId.append(option);
    });
  });

  encodeFaceBtn.on("click", function () {
    $.ajax({
      url: "/encode_faces",
      type: "POST",
      contentType: "application/json",
    }).done(function (data) {
      alert(data.message);
    });
  });
});
