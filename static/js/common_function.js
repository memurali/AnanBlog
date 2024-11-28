
// Get category for Menu Toggle
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

// Contact form 
$('#contact_form').on('submit', function (e) {
    e.preventDefault();
    var formdata = $(this).serialize()
    $.ajax({
        url: 'set_contact',
        type: "POST",
        data: formdata,
        success: function (res) {
            // if (res['message'] == 'Category created successfully') {
            //     $('#category_form').trigger('reset')
            //     window.location.href = "view_form";
            // }

        },
    })
})