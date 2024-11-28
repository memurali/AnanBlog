let queryString = window.location.search;
let queryValue = queryString.substring(1);
let value = queryValue.replaceAll('%20', ' ')
$('.service_name,.service_heading,.service_tittle').html(value);
