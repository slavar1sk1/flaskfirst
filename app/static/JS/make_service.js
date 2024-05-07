$( function () {
  $('#confirm').click(function () {
    let formData = new FormData;
    formData.append('img', document.getElementById('img').files[0])
    formData.append('title', $('#title').val())
    formData.append('intro', $('#intro').val())
    formData.append('text', $('#text').val())
    formData.append('catalog', $('#catalog').val())
    formData.append('price', $('#price').val())

    $.ajax('make_service',{
      type: 'POST',
      dataType: 'json',
      async: true,
      data: formData,
      processData: false,
      contentType: false,
      success: function (response) {

          if (response.success) {
            document.getElementById('error').textContent = response.confirm
            document.getElementById('img').value = ''
          $('#title').val('')
          $('#intro').val('')
          $('#text').val('')
          $('#catalog').val('')
          $('#price').val('')
            } else {
                $('#title').val('')
                document.getElementById('error').textContent = response.error}
      }

    })
  })
})