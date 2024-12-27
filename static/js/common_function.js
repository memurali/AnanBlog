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

console.log(value,".............")


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

        console.log(temp,">>>>>>>>>>>")
        $('.description').html(temp)
    },
})


// Add click event listener for toggle functionality
$('.insight-inner-sec').on('click', '.toggle-icon', function () {
    // Revert all other toggle-icon elements to "+"
    $('.toggle-icon').each(function () {
        if ($(this).text().trim().startsWith('-')) {
            $(this).html(`+ <a class="insights_resources" value="${$(this).find('.insights_resources').attr('value')}">${$(this).find('.insights_resources').text()}</a>`);
        }
    });

    // Toggle the clicked element
    const text = $(this).text().trim();
    let updatedText = text.replace('+', '').replace('-', '').trim();

    if (text.startsWith('+')) {
        $(this).html(`- <a class="insights_resources" value="${$(this).find('.insights_resources').attr('value')}">${$(this).find('.insights_resources').text()}</a>`);
    }

    // Show service insights
    $('.service_insights').css('display', 'block');
    $('.insight_service_name').html(`<span>:: </span>` + updatedText + " Insights And Resources");
});

// Ensure the click event for .insights_resources is bound only once
$('.insight-inner-sec').off('click', '.insights_resources').on('click', '.insights_resources', function (e) {
    e.preventDefault();
    $('.insight_service_name').empty(); // Clear the previous insight name
    $('#insights_table').empty(); // Clear the insights table if needed
    const insightName = $(this).attr('value');
    $('.insight_service_name').html(`<span>:: </span>${insightName} Insights And Resources`);
    InsightTable(insightName);
});


// Case study 
$.ajax({
    url: `getCaseStudy`,
    type: "POST",
    data: {
        'service_id': $('.service_name').text()
    },
    success: function (res) {
        if (res.u_id && Array.isArray(res.u_id)) {
            // Service id ASC order 
            var services = res.u_id.sort((a, b) => a.service_id - b.service_id);

            // Insights And Resources 
            services.forEach(function (service) {
                var CaseStudy = ''

                CaseStudy = `<div class="grid-x">
                        <div class="cell small-12 medium-6">
                            <div class="case-study1">
                                <h1 class="case-title">${service['CaseStudyName']}</h1>
                                <p class="case-description">${service['Description']}</p>
                                <a href="#" class="case-link">Case Study</a>
                            </div>
                        </div>

                        <div class="cell small-12 medium-6">
                            <div class="case-study-title1">
                                <h1 class="case-title"><img src="/media/${service.Images.trim()}" alt="${service.Images}" class="thumbnail" style="width:80px; cursor:pointer;"></h1>
                            </div>
                        </div>
                </div>`

                $('#Case_study').append(CaseStudy);
            })

        } else {
            console.error("Category not found or u_id is not an array");
        }
    }
});

function InsightTable(insightName) {
    $.ajax({
        url: `getInsights`,
        type: "POST",
        data: {
            'service_id': insightName
        },
        success: function (res) {
            if (res.u_id && Array.isArray(res.u_id)) {
                var services = res.u_id.sort((a, b) => a.service_id - b.service_id);

                const totalItems = services.length;
                const itemsPerPage = 6;
                const totalPages = Math.ceil(totalItems / itemsPerPage);

                $('#insights_table').empty(); // Clear existing data

                // Show pagination if more than one page
                if (totalPages > 1) {
                    $('.pagination').show();
                } else {
                    $('.pagination').hide();
                }

                // Clear pagination controls to prevent duplicates
                $('.pagination').empty();

                // Add previous button
                let paginationControls = `<li class="pagination-previous disabled"><i class="fa-thin fa-less-than"></i></li>`;

                // Add page number buttons dynamically
                for (let i = 1; i <= totalPages; i++) {
                    paginationControls += `<li><a href="#" class="page-btn" data-page="${i}" aria-label="Page ${i}">${i}</a></li>`;
                }

                // Add next button
                paginationControls += `<li class="pagination-next"><a href="#" class="next-btn" aria-label="Next page"><i class="fa-thin fa-greater-than"></i></a></li>`;

                // Append pagination controls to the container
                $('.pagination').html(paginationControls);

                // Render first page initially
                renderPage(1, services, itemsPerPage);

                // Handle page number click
                $('.page-btn').on('click', function (e) {
                    e.preventDefault();
                    const page = $(this).data('page');
                    renderPage(page, services, itemsPerPage);
                    updatePagination(page, totalPages);
                });

                // Handle next button click
                $('.next-btn').on('click', function (e) {
                    e.preventDefault();
                    const currentPage = parseInt($('.current').text().trim());
                    const nextPage = currentPage + 1;
                    if (nextPage <= totalPages) {
                        renderPage(nextPage, services, itemsPerPage);
                        updatePagination(nextPage, totalPages);
                    }
                });

                // Handle previous button click
                $('.pagination-previous').on('click', function (e) {
                    e.preventDefault();
                    const currentPage = parseInt($('.current').text().trim());
                    const prevPage = currentPage - 1;
                    if (prevPage > 0) {
                        renderPage(prevPage, services, itemsPerPage);
                        updatePagination(prevPage, totalPages);
                    }
                });

                // Render page function
                function renderPage(page, services, itemsPerPage) {
                    const start = (page - 1) * itemsPerPage;
                    const end = page * itemsPerPage;
                    const currentPageServices = services.slice(start, end);
                    let row = `<div class="grid-x grid-margin-x">`;

                    currentPageServices.forEach(function (service, index) {
                        const serialNo = start + index + 1;

                        const column = `
                            <div class="cell small-12 medium-4 latest-tec__blog">
                                <div class="latest-tec__num">
                                    <h4>${serialNo}</h4>
                                </div>
                                <h4>/ ${service['ServiceHeading']} /</h4>
                                <p>${service['Description']}</p>
                                <button class="button">Preview</button>
                                <button class="button secondary">Buy</button>
                            </div>`;

                        row += column;
                    });

                    row += `</div>`;
                    $('#insights_table').html(row);
                }

                // Update pagination controls
                function updatePagination(currentPage, totalPages) {
                    $('.page-btn').removeClass('current');
                    $(`.page-btn[data-page=${currentPage}]`).addClass('current');

                    if (currentPage <= 1) {
                        $('.pagination-previous').addClass('disabled');
                    } else {
                        $('.pagination-previous').removeClass('disabled');
                    }

                    if (currentPage >= totalPages) {
                        $('.pagination-next').addClass('disabled');
                    } else {
                        $('.pagination-next').removeClass('disabled');
                    }
                }
            } else {
                console.error("Category not found or u_id is not an array");
            }
        },
        error: function (xhr, status, error) {
            console.error("Error during AJAX request:", error);
            alert("Failed to fetch insights. Please try again.");
        }
    });
}

