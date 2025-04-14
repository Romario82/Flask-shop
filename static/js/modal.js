$(document).ready(function() {
        //  "Quick View"
        $('.quickview-btn').on('click', function(e) {
            e.preventDefault(); 
            // data-product-id
            var productId = $(this).data('product-id');
            // AJAX 
            $.ajax({
                url: '/get_product_details/' + productId,
                method: 'GET',
                success: function(response) {
                    console.log(response); 
                    $('#modal_product_name').text(response.name);
                    
                    if (response.promotion && response.promotion != 0) {
                        $('#modal_product_price').text((response.price - response.promotion).toFixed(1) + ' USD');
                        $('#modal_product_old_price').text(response.price + ' USD');
                    } 
                    else {
                        $('#modal_product_price').text(response.price + ' USD');
                        $('#modal_product_old_price').text('');
                    }
                    $('#modal_product_description').text(response.description);
                    $('#modal_product_manufacturer').text('Manufacturer: ' + ' ' + response.manufacturer);
                    $('#modal_product_image').attr('src', '/uploads/' + response.image);
                    $('#modal_box').modal('show');
                },
                error: function(error) {
                    console.log('Error loading product details:', error);
                }
            });
        });
    });