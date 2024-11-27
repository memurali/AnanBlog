// Add CategoryDetails
$('#category_form').on('submit', function (e) {
    e.preventDefault();
    var formdata = $(this).serialize()
    $.ajax({
        url: 'CategoryDetails',
        type: "POST",
        data: formdata,
        success: function (res) {
            if (res['message'] == 'Category created successfully') {
                $('#category_form').trigger('reset')
                window.location.href = "view_form";
            }
        },
    })
})

fetchcategory()

function fetchcategory() {
    $.ajax({
        url: 'CategoryDetails',
        type: "GET",
        success: function (res) {
            var categories = res.categories;
            var tbody = $('#CategoryTable tbody');
            tbody.empty();
            categories.forEach(function (category) {
                var row = `<tr>
                <td>${category.service_id}</td>
                <td>${category.category}</td>
                <td><span class="fi-page-edit edit_icon" data-toggle="edit_offCanvas" onclick="editcategory(${category.service_id})"></span></td>
                <td><span class="fi-trash delete_icon" onclick="deletecategory(${category.service_id})"></span></td>
            </tr>`;
                tbody.append(row);
            });
        },
    })
}


function editcategory(clientId) {
    $.ajax({
        url: `CategoryDetails?id=${clientId}`,
        type: "GET",
        success: function (res) {
            if (res.categories) {
                var client = res.categories;
                $('#category_id').val(client.category_id);
                $('#category_name').val(client.category_name);

            } else {
                console.error("Category not found");
            }
        }
    })
}


$('#edit_category_form').on('submit', function (e) {
    e.preventDefault();
    var formdata = {
        'id': $('#client_id').val(),
        'category_name': $('#category_name').val(),
    }
    fetch('CategoryDetails', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formdata)
        })
        .then(response => response.json())
        .then(res => {
            if (res['message'] == 'Category updated successfully') {
                fetchClients();
                Swal.fire({
                    icon: "success",
                    title: res['message'],
                });
                $('#edit_category_form').trigger('reset')
                var modal = document.getElementById('edit_offCanvas');
                if (modal) {
                    $(modal).foundation('close');
                };
                window.location.href = "view_form";

            } else if (res['message'] == 'Client Name already exists') {
                Swal.fire({
                    icon: "error",
                    title: res['message'],
                });
            }
        })
})

function deletecategory(cat_tId) {
    Swal.fire({
        title: "Are you sure?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes, delete it!"
    }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                url: 'CategoryDetails',
                type: 'DELETE',
                contentType: 'application/json',
                data: JSON.stringify({
                    id: cat_tId
                }),
                success: function (res) {
                    if (res['message'] === 'Category deleted successfully') {
                        fetchClients();
                        Swal.fire({
                            title: "Deleted!",
                            text: "Category deleted successfully.",
                            icon: "success"
                        }).then(() => {
                            window.location.href = "view_form";
                        });
                    } else {
                        Swal.fire({
                            title: "Error!",
                            text: res['error'] || "An error occurred while deleting the client.",
                            icon: "error"
                        });
                    }
                },
                error: function (xhr, status, error) {
                    Swal.fire({
                        title: "Error!",
                        text: "An error occurred: " + error,
                        icon: "error"
                    });
                }
            });
        }
    });
}

// Get category 
$.ajax({
    url: `getcategory`,
    type: "GET",
    success: function (res) {
        if (res.u_id && Array.isArray(res.u_id)) {
            const services = res.u_id;

            services.forEach(function (week) {
                // Dynamically classify services into two arrays based on certain logic
                const firstTabServices = [1, 2, 5, 6, 9, 10, 13, 14]; // Service IDs for the first tab structure
                const elseTabServices = [3, 4, 8, 7, 11, 12, 15, 16]; // Service IDs for the else tab structure

                // Get both service_id and category
                const serviceInfo = {
                    service_id: week['service_id'],
                    category: week['category']
                };

                // Create the HTML structure based on service_id
                let tabHtml = '';
                if (firstTabServices.includes(serviceInfo.service_id)) {

                    // First tab structure
                    tabHtml = `
                    <div class="cell small-12 medium-6  service-item align-start">
                        <h1>${serviceInfo.service_id}</h1>
                        <h2><a class="service_category">${serviceInfo.category} <span class="highlight">.</span></a></h2>
                    </div>`;                 
                } else if (elseTabServices.includes(serviceInfo.service_id)) {
                    // Else tab structure
                    tabHtml = `
                    <div class="cell small-12 medium-6 service-item align-end">
                        <h1>${serviceInfo.service_id}</h1>
                        <h2><a class="service_category">${serviceInfo.category} <span class="highlight">.</span></a></h2>
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
    return service ? service : { service_id: serviceId, category: 'Unknown Category' };
}

// Attach a click event to all links with the class 'service_name'
$('.service_category').on('click', function(event) {
    event.preventDefault();
    alert(">>>>>>>>>>>>>>>")
    const hrefValue = $(this).val();
    console.log(hrefValue,">>>>>>>>>>>")
    // window.location.href = `Service_details?${hrefValue}`
    console.log('The href value is:', hrefValue);
});

