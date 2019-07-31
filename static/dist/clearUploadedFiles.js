fetch("/clear_uploaded_files")
  .then(function(response) {
    return response.text();
  })