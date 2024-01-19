$(document).ready(function () {
  var selectId = $("#selectId");
  var encodeFaceBtn = $("#encodeFaceBtn");

  var data = [
    { id: 1, name: "Người 1" },
    { id: 2, name: "Người 2" },
    { id: 3, name: "Người 3" },
    { id: 4, name: "Người 4" },
    { id: 5, name: "Người 5" },
    { id: 6, name: "Người 6" },
  ];

  $.each(data, function (_index, item) {
    var option = $("<option>").attr("value", item.id).text(item.name);
    selectId.append(option);
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
