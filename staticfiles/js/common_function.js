
// Get category 
$.ajax({
    url: `getcategory`,
    type: "GET",
    success: function (res) {
        if (res.u_id && Array.isArray(res.u_id)) {
            var services = res.u_id.sort((a, b) => a.service_id - b.service_id);

            services.forEach(function (week) {
                // Dynamically classify services into two arrays based on certain logic
                const firstTabServices = [1, 2, 5, 6, 9, 10, 13, 14]; // Service IDs for the first tab structure
                const elseTabServices = [3, 4, 8, 7, 11, 12, 15, 16]; // Service IDs for the else tab structure

                // Get both service_id and category
                const serviceInfo = {
                    service_id: week['service_id'],
                    category: week['category']
                };

                const formattedServiceId = String(serviceInfo.service_id).padStart(2, '0');

                // Create the HTML structure based on service_id
                let tabHtml = '';
                if (firstTabServices.includes(serviceInfo.service_id)) {

                    // First tab structure
                    tabHtml = `
                    <div class="cell small-12 medium-6  service-item align-start">
                        <h1>${formattedServiceId}</h1>
                        <h2><a href="Service_details?${serviceInfo.category}" class="service_category">${serviceInfo.category} <span class="highlight">.</span></a></h2>
                    </div>`;
                } else if (elseTabServices.includes(serviceInfo.service_id)) {
                    // Else tab structure
                    tabHtml = `
                    <div class="cell small-12 medium-6 service-item align-end">
                        <h1>${formattedServiceId}</h1>
                        <h2><a href="Service_details?${serviceInfo.category}" class="service_category">${serviceInfo.category} <span class="highlight">.</span></a></h2>
                    </div>`;
                }

                // Append the tabHtml to your desired container (e.g., #cat_service)
                $('#cat_service').append(tabHtml);
            });
        } else {
            console.error("Category not found or u_id is not an array");
        }
    }
});

// Function to get the category and service_id based on the service_id (updated to return both values)
function getCategoryByServiceId(serviceId) {
    // Find the service object based on service_id
    const service = serviceId.find(s => s.service_id === serviceId);
    return service ? service : {
        service_id: serviceId,
        category: 'Unknown Category'
    };
}

// Get category for Menu Toggle
$.ajax({
    url: `getcategory`,
    type: "GET",
    success: function (res) {
        if (res.u_id && Array.isArray(res.u_id)) {
            // Service id ASC order 
            var services = res.u_id.sort((a, b) => a.service_id - b.service_id);

            // Insights And Resources 
            services.forEach(function (service) {
                var insightshtml = ''
                var Main_toggle = ''

                insightshtml = `<div class="cell medium-6">
                <p class="toggle-icon">+ <a class="insights_resources" value="${service.category}">${service.category}</a></p>
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
        success: function (res) {},
    })
})


let queryString = window.location.search;
let queryValue = queryString.substring(1);
let value = queryValue.replaceAll('%20', ' ')
$('.service_name,.service_heading,.service_tittle').html(value);


$.ajax({
    url: 'findServiceDescription',
    type: "POST",
    data: {
        'category': value
    },
    success: function (res) {
        const description = res.u_id;
        var temp = ''
        // Insights And Resources 
        description.forEach(function (desc) {
            temp += `<p>${desc.Description}</p>`
        })
        $('.description').html(temp)
    },
})

// Service  Insights And Resources 
// $(document).on('click', '.insights_resources', function () {
//     var value = $(this).attr('value');
//     console.log(value); // Outputs "Technology"
//     $('.service_insights').css('display', 'block')
//     $('.insight_service_name').html(`<span>:: </span>` + value + " Insights And Resources")

// });

// Add click event listener for toggle functionality
$('.insight-inner-sec').on('click', '.toggle-icon', function () {
    // Revert all other elements to "+"
    $('.toggle-icon').each(function () {
        if ($(this).text().trim().startsWith('-')) {
            $(this).html(`+ <a class="insights_resources" value="${$(this).find('.insights_resources').attr('value')}">${$(this).find('.insights_resources').text()}</a>`);

        }
    });

    // Toggle the clicked element
    var text = $(this).text().trim();
    console.log(text,">>>>>>>>>>>>>")
    if (text.startsWith('+')) {
        var updatedText = text.replace('+', ''); 
        $(this).html(`- <a class="insights_resources" value="${$(this).find('.insights_resources').attr('value')}">${$(this).find('.insights_resources').text()}</a>`);

    }

    $('.service_insights').css('display', 'block')
    $('.insight_service_name').html(`<span>:: </span>` + updatedText + " Insights And Resources")
});