// Answer query using AJAX 
function answer_query() {
  var query = document.getElementById("query").value;
  var context = document.getElementById("context").value;
  var data = {
    query: query,
    context: context,
  };

  if (query != '' && context != '') {
    var btn = document.getElementById("answer-btn");
    btn.classList.add("button--loading");
    btn.textContent = ''
    $.ajax({
      url: "model/question", 
      data: data,
      type: "post",
      success: function (response) {
        document.getElementById("answer").value = response;
      },
      error: function (response) {
        console.log(response)
        alert("An unexpected error occured...", "danger");
      },
      complete: function () {
        btn.classList.remove("button--loading");
        btn.textContent = 'Answer query'}
    });
  } else {
    alert("Please specify a query and a context!", "danger");
  }
}


// Bootstrap alert
const alert = (message, type) => {
const alertPlaceholder = document.getElementById('alerts')
  const wrapper = document.createElement('div')
  wrapper.innerHTML = [
    `<div class="alert alert-${type} alert-dismissible fade show" role="alert">`,
    `   <div>${message}</div>`,
    '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
    '</div>'
  ].join('')

  alertPlaceholder.append(wrapper)
}