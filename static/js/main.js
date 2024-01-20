$(document).ready(function () {
  var selectId = $("#selectId");
  var encodeFacesBtn = $("#encodeFacesBtn");
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

  encodeFacesBtn.on("click", function () {
    $.ajax({
      url: "/encode_faces",
      type: "POST",
      contentType: "application/json",
    }).done(function (data) {
      alert(data.message);
    });
  });

  encodeFaceBtn.on("click", function () {
    var person_id = selectId.val();
    console.log("person_id", person_id);
    $.ajax({
      url: "/encode_face",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify({ person_id: person_id }),
    }).done(function (data) {
      alert(data.message);
    });
  });
});
