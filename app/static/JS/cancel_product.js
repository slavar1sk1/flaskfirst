$(function () {
  $(".cancel-btn").click(function () {
    var serviceId = $(this).data("id");
    $.ajax({
      url: "/cancel_service/" + serviceId,
      type: "POST",
      dataType: "json",
      async: true,
      success: function (response) {
        if (response.success) {
          $(".cart-counter").text(response.counter);
          $(".price").text(response.price_counter + "€");

          document.getElementById('card-' + serviceId).outerHTML = ''
          console.log("Услуга успешно отменена");
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
