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
                <td><span class="fi-page-edit edit_icon" data-toggle="edit_offCanvas" onclick="editcategory(${category.service_id})"></span></td>
                <td><span class="fi-trash delete_icon" onclick="deletecategory(${category.service_id})"></span></td>
            </tr>`;
                tbody.append(row);
            });
        },
    })
}


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
                fetchcategory();
                Swal.fire({
                    icon: "success",
                    title: res['message'],
                });
                $('#edit_category_form').trigger('reset')
                var modal = $('#edit_offCanvas');
                if (modal.length) {
                    $(document).foundation()
                    modal.foundation('close');
                };
                window.location.href = "view_form";

            } else if (res['message'] == 'Category Name already exists') {
                Swal.fire({
                    icon: "error",
                    title: res['message'],
                });
            }
        })
});


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
                        fetchcategory();
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
