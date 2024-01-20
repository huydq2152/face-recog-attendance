$(document).ready(function () {
  var selectIdForEncodeDataset = $("#selectIdForEncodeDataset");
  var selectIdForCheckAttendance = $("#selectIdForCheckAttendance");
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
      selectIdForEncodeDataset.append(option);
      selectIdForCheckAttendance.append(option.clone());
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
    var formData = new FormData();
    formData.append("person_id", selectIdForEncodeDataset.val());

    $.ajax({
      url: "/encode_face",
      type: "POST",
      data: formData,
      processData: false,
      contentType: false,
    }).done(function (data) {
      alert(data.message);
    });
  });
});
