$(function () {
  $("#btn").click(function () {
    var serviceId = $(this).data("id");
    $.ajax({
      url: "/add_to_pcart/" + serviceId,
      type: "POST",
      dataType: "json",
      async: true,
      success: function (response) {
        if (response.success) {
          $(".cart-counter").text(response.counter);
          $(".price").text(response.price_counter + '€');

          console.log("Product is successfully added");
        } else {
          console.error("Произошла ошибка:", response.error);
        }
      },
      error: function (xhr, status, error) {
        console.error("Произошла ошибка:", status, error);
      },
    });
  });
});
