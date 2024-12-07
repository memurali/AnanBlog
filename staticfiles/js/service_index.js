// Add Service 
$('#category_form').on('submit', function (e) {
    e.preventDefault();
    var formdata = $(this).serialize()
    $.ajax({
        url: 'CategoryDetails',
        type: "POST",
        data: formdata,
        success: function (res) {
            if (res['message'] == 'Category created successfully') {
                Swal.fire({
                    icon: "success",
                    title: res['message'],
                });
                $('#category_form').trigger('reset')
                window.location.href = "view_form";
            }
            else if (res['message'] == 'Category already exists'){
                Swal.fire({
                    icon: "error",
                    title: res['message'],
                });
            }
        },
    })
})


function fetchcategory() {
    $.ajax({
        url: 'CategoryDetails',
        type: "GET",
        success: function (res) {
            var categories = res.categories;

            // Service Id ASC order 
            categories.sort(function (a, b) {
                return a.service_id - b.service_id;
            });

            var tbody = $('#CategoryTable tbody');
            tbody.empty();
            categories.forEach(function (category) {
                var row = `<tr>
                <td>${category.service_id}</td>
                <td>${category.category}</td>
                <td>${category.Description}</td>
                <td><a href="Add_CaseStudy">Add Form</a><br><a href="view_CaseStudy">View Tables</a></td>
                <td><a href="Add_CaseStudy">Add Form</a><br><a href="view_CaseStudy">View Tables</a></td>
                <td><span class="fi-page-edit edit_icon" data-toggle="edit_offCanvas" onclick="editcategory(${category.service_id})"></span></td>
                <td><span class="fi-trash delete_icon" onclick="deletecategory(${category.service_id})"></span></td>
            </tr>`;
                tbody.append(row);
            });
        },
    })
}

// Edit Services 
function editcategory(categoryID) {
    $.ajax({
        url: `CategoryDetails?id=${categoryID}`,
        type: "GET",
        success: function (res) {
            if (res.categories) {
                var category = res.categories;
                $('#category_id').val(category.service_id);
                $('#category_name').val(category.category);
                $('#description').val(category.Description);

            } else {
                console.error("Category not found");
            }
        }
    })
}

$('#edit_category_form').on('submit', function (e) {
    e.preventDefault();
    var formdata = {
        'id': $('#category_id').val(),
        'category_name': $('#category_name').val(),
        'Description': $('#description').val(),
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
                Swal.fire({
                    icon: "success",
                    title: res['message'],
                });
                // $('#edit_category_form').trigger('reset')
                fetchcategory()
                // window.location.href = "view_form";

            } else if (res['message'] == 'Category Name already exists') {
                Swal.fire({
                    icon: "error",
                    title: res['message'],
                });
            }
        })
});

// Delete Services 
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
                        Swal.fire({
                            title: "Deleted!",
                            text: "Category deleted successfully.",
                            icon: "success"
                        }).then(() => {
                            fetchcategory()
                            window.location.href = "view_form";
                        });
                    } else {
                        Swal.fire({
                            title: "Error!",
                            text: res['error'] || "An error occurred while deleting the Category.",
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

// Add Case Study 
$.ajax({
    url: `getcategory`,
    type: "GET",
    success: function (res) {
        if (res.u_id && Array.isArray(res.u_id)) {
            // Service id ASC order 
            var services = res.u_id.sort((a, b) => a.service_id - b.service_id);

            // Insights And Resources 
            var temp_service = ''

            services.forEach(function (service) {
                temp_service += `<option value="${service.service_id}">${service.category}</option>`

                $('#Serice_Category').html(temp_service);
            })

        } else {
            console.error("Category not found or u_id is not an array");
        }
    }
});


// Case Study 
$(document).ready(function () {
    $('#case_study_form').on('submit', function (e) {
        e.preventDefault(); // Prevent default form submission

        let formData = new FormData(this);

        $.ajax({
            url: 'CaseStudyDetails', // Replace with your server endpoint
            type: 'POST',
            data: formData,
            processData: false, // Required for FormData
            contentType: false, // Required for FormData
            success: function (res) {
                if (res['message'] == 'Case Study created successfully') {
                    Swal.fire({
                        icon: "success",
                        title: res['message'],
                    });
                    fetchCaseStudy()
                } else if (res['message'] == 'CaseStudy already exists for this Service') {
                    Swal.fire({
                        icon: "error",
                        title: res['message'],
                    });
                }
            },
            error: function (xhr, status, error) {
                // Handle error response
                alert('An error occurred: ' + error);
            }
        });
    });
});

const findServiceName = (serviceId, callback) => {
    if (!serviceId) {
        console.error("Invalid service ID provided:", serviceId);
        callback("Unknown Service"); // Provide a default value if the ID is invalid
        return;
    }

    $.ajax({
        url: 'findServiceID', // Endpoint for service name lookup
        type: 'POST',
        data: {
            service_id: serviceId
        },
        success: function (res) {
            if (res && res.u_id && res.u_id.length > 0) {
                const serviceCategory = res.u_id[0].category; // Access the category
                callback(serviceCategory);
            } else {
                console.warn("Service name not found for ID:", serviceId);
                callback("Unknown Service");
            }
        },
        error: function (xhr, status, error) {
            console.error(`Error fetching service name for ID ${serviceId}:`, error);
            callback("Unknown Service");
        }
    });
};


function fetchCaseStudy() {
    $.ajax({
        url: 'CaseStudyDetails', // Endpoint for fetching case studies
        type: "GET",
        success: function (res) {
            if (!res.casestudy || !Array.isArray(res.casestudy)) {
                console.error("Invalid response format:", res);
                alert("Failed to fetch case studies. Please try again.");
                return;
            }

            const casestudy = res.casestudy;

            // Sort case studies by cs_id in ascending order
            casestudy.sort((a, b) => a.cs_id - b.cs_id);

            const tbody = $('#CaseStudyTable tbody');
            tbody.empty(); // Clear existing table rows

            casestudy.forEach(category => {
                const Images = category.Images.split(',');

                // Fetch the service name asynchronously
                findServiceName(category.service_id, function (serviceName) {
                    // Generate a table row after fetching the service name
                    const row = `
                        <tr>
                            <td>${category.cs_id}</td>
                            <td>${serviceName}</td>
                            <td>${category.CaseStudyName}</td>
                            <td>${category.Description}</td>
                            <td>${Images[0]}</td>
                            <td>
                                <span class="fi-page-edit edit_icon" data-toggle="edit_offCanvas" onclick="editCasestudy(${category.cs_id})"></span>
                            </td>
                            <td>
                                <span class="fi-trash delete_icon" onclick="deleteStudy(${category.cs_id})"></span>
                            </td>
                        </tr>`;
                    tbody.append(row); // Append the row to the table
                });
            });
        },
        error: function (xhr, status, error) {
            console.error("Error fetching case studies:", error);
            alert("An error occurred while fetching case studies. Please try again.");
        }
    });
}


// INsights &  Resources 
$('#insights_resource_form').on('submit', function (e) {
    e.preventDefault(); // Prevent default form submission
    let formData = $(this).serialize();
    $.ajax({
        url: 'InsightsDetails', // Replace with your server endpoint
        type: 'POST',
        data: formData,
        success: function (res) {
            if (res['message'] == 'Insights & Resources created successfully') {
                Swal.fire({
                    icon: "success",
                    title: res['message'],
                });
                fetchInsights();
            } else if (res['message'] == 'Insights already exists for this Service') {
                Swal.fire({
                    icon: "error",
                    title: res['message'],
                });
            }
        },
        error: function (xhr, status, error) {
            // Handle error response
            alert('An error occurred: ' + error);
        }
    });
});


function fetchInsights() {
    $.ajax({
        url: 'InsightsDetails', // Endpoint for fetching case studies
        type: "GET",
        success: function (res) {
            if (!res.insights || !Array.isArray(res.insights)) {
                console.error("Invalid response format:", res);
                alert("Failed to fetch case studies. Please try again.");
                return;
            }

            const insights = res.insights;

            // Sort case studies by cs_id in ascending order
            insights.sort((a, b) => a.insight_id - b.insight_id);

            const tbody = $('#InsightsTable tbody');
            tbody.empty(); // Clear existing table rows

            insights.forEach(category => {

                // Fetch the service name asynchronously
                findServiceName(category.service_id, function (serviceName) {
                    // Generate a table row after fetching the service name
                    const row = `
                        <tr>
                            <td>${category.insight_id}</td>
                            <td>${serviceName}</td>
                            <td>${category.ServiceHeading}</td>
                            <td>${category.Description}</td>
                            <td>${category.Preview}</td>
                            <td>${category.Buy}</td>
                            <td>
                                <span class="fi-page-edit edit_icon" data-toggle="edit_offCanvas" onclick="editInsights(${category.insight_id})"></span>
                            </td>
                            <td>
                                <span class="fi-trash delete_icon" onclick="deleteInsights(${category.insight_id})"></span>
                            </td>
                        </tr>`;
                    tbody.append(row); // Append the row to the table
                });
            });
        },
        error: function (xhr, status, error) {
            console.error("Error fetching case studies:", error);
            alert("An error occurred while fetching case studies. Please try again.");
        }
    });
}

// Edit Insights 
function editInsights(InsightsID) {
    $.ajax({
        url: `InsightsDetails?id=${InsightsID}`,
        type: "GET",
        success: function (res) {
            if (res.insights) {
                var category = res.insights;
                $('#insight_id').val(category.insight_id)
                $('#Serice_Category').val(category.service_id);
                $('#edit_service_heading').val(category.ServiceHeading);
                $('#edit_description').val(category.Description);
                $('#edit_Preview').val(category.Preview);
                $('#edit_buy').val(category.Buy);

            } else {
                console.error("Case Study not found");
            }
        }
    })
}


$('#edit_insights_resource_form').on('submit', function (e) {
    e.preventDefault();
    var formdata = {
        'id': parseInt($('#insight_id').val()),
        'Serice_Category': parseInt($('#Serice_Category').val()),
        'service_heading': $('#edit_service_heading').val(),
        'Description': $('#edit_description').val(),
        'Preview': $('#edit_Preview').val(),
        'buy': $('#edit_buy').val(),
    }
    fetch('InsightsDetails', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formdata)
        })
        .then(response => response.json())
        .then(res => {
            if (res['message'] == 'Insights updated successfully') {
                Swal.fire({
                    icon: "success",
                    title: res['message'],
                });
                fetchInsights();
                $('#edit_insights_resource_form').trigger('reset')
            } else if (res['message'] == 'Insights already exists') {
                Swal.fire({
                    icon: "error",
                    title: res['message'],
                });
            }
        })
});

// Delete Insights 
function deleteInsights(cat_tId) {
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
                url: 'InsightsDetails',
                type: 'DELETE',
                contentType: 'application/json',
                data: JSON.stringify({
                    id: cat_tId
                }),
                success: function (res) {
                    if (res['message'] === 'Insights deleted successfully') {
                        Swal.fire({
                            title: "Deleted!",
                            text: res['message'],
                            icon: "success"
                        }).then(() => {
                            // window.location.href = "view_form";
                            fetchInsights();
                        });
                    } else {
                        Swal.fire({
                            title: "Error!",
                            text: res['error'] || "An error occurred while deleting the Category.",
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

$(document).ready(function () {
    fetchInsights()
    fetchcategory()
    fetchCaseStudy()
})