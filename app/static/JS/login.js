$( function () {
  $("#submit").click(function () {
    let formData = new FormData;
    formData.append("username", $("#username").val());
    formData.append("password", $("#password").val());
    formData.append("remember_me", $("#remember_me").val());

    $.ajax('autorization', {
      type: "POST",
      dataType: "json",
      async: true,
      data: formData,
      success: function (response) {
        if (response.login) {
          $('#error').text(response.login_error);
        } else if (response.password) {
          $('#error').text(response.password_error);
        }
      },
    });
  });
});
