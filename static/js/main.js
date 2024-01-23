$(document).ready(function () {
  var selectDetectFaceMethodForEncodeFaces = $(
    "#selectDetectFaceMethodForEncodeFaces"
  );

  var selectDetectFaceMethodForEncodeFace = $(
    "#selectDetectFaceMethodForEncodeFace"
  );

  var selectIdForEncodeFace = $("#selectIdForEncodeFace");
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
      selectIdForEncodeFace.append(option);
      selectIdForCheckAttendance.append(option.clone());
    });
  });

  encodeFacesBtn.on("click", function () {
    var formData = new FormData();
    formData.append(
      "detect_face_method",
      selectDetectFaceMethodForEncodeFaces.val()
    );
    $.ajax({
      url: "/encode_faces",
      type: "POST",
      data: formData,
      processData: false,
      contentType: false,
    }).done(function (data) {
      alert(data.message);
    });
  });

  encodeFaceBtn.on("click", function () {
    var formData = new FormData();
    formData.append("person_id", selectIdForEncodeFace.val());
    formData.append(
      "detect_face_method",
      selectDetectFaceMethodForEncodeFace.val()
    );

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
