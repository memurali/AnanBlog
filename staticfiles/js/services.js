let queryString = window.location.search;
let queryValue = queryString.substring(1);
let value = queryValue.replaceAll('%20', ' ')
$('.service_name,.service_heading,.service_tittle').html(value);
// $('').html(value);


// Get category 
$.ajax({
    url: `getcategory`,
    type: "GET",
    success: function (res) {
        if (res.u_id && Array.isArray(res.u_id)) {
            const services = res.u_id;
            // Insights And Resources 
            services.forEach(function (service) {
                var insightshtml = ''
                var Main_toggle = ''

                insightshtml = `<div class="cell medium-6">
                <p>+ <a href="Service_details?${service.category}">${service.category}</a></p>
                </div>`

                Main_toggle = `<a href="Service_details?${service.category}">${service.category}</a>`

                $('.insight-inner-sec').append(insightshtml);
                $('.main-options').append(Main_toggle);

            })
        } else {
            console.error("Category not found or u_id is not an array");
        }
    }
});