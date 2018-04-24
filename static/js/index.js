function loadData(event) {
    var min = $('#min').val();
    var max = $('#max').val();
    var order = $('input[name=order]:checked').val();
    var stock = $('input[name=stock]:checked');
    stock = $.map(stock, function (s) {
        return s.value
    });
    var price = $('input[name=price]:checked');
    price = $.map(price, function (s) {
        return s.value
    });

    option = {
        min: min,
        max: max,
        order: order,
        stock: stock,
        price: price
    };

    $.ajax({
        url: "/product",
        type: "POST",
        data: JSON.stringify(option),
        contentType: 'application/json;charset=utf-8',
        dataType: 'json',
        success: renderProduct
    });

    event.preventDefault();
}

function renderProduct(data) {
    var container = $("#product-container");
    var pagination = $("#pagination");
    container.empty();
    pagination.empty();
    if (data['error']) {
        container.html('<h1>' + data['error'] + '</h1>');
        return container.show();
    }
    var options = {
        dataSource: data,
        pageSize: 50,
        callback: function (res, page) {
            var dataHtml = '<div>';

            $.each(res, function (index, item) {
                if (Number(item.price) < 0)
                    item.price = 'Unknown';
                else
                    item.price = '$' + item.price;

                if (Number(item.stock) < 0) {
                    item.stock = 'Stock Unknown';
                } else if (Number(item.stock) === 0) {
                    item.stock = 'Out of Stock';
                } else if (Number(item.stock) === 101) {
                    item.stock = 'In Stock';
                } else if (Number(item.stock) === 102) {
                    item.stock = 'Discontinued';
                } else {
                    item.stock = item.stock + ' In Stock';
                }

                dataHtml += '<div class="row">' +
                    '<div class="col-md-4">' +
                    '<a href="' + item.url + '">' +
                    '<img class="img-fluid rounded mb-3 mb-md-0" src="' + item.img + '">' +
                    '</a>' +
                    '</div>' +
                    '<div class="col-md-8">' +
                    '<a href="' + item.url + '">' +
                    '<h4>' + item.name + '</h4>' +
                    '</a>' +
                    '<div>Product ID: ' + item.id + '</div>' +
                    '<div>Price: ' + item.price + '</div>' +
                    '<div>' + item.stock + '</div>' +
                    '</div>' +
                    '</div>' +
                    '<hr>';
            });
            dataHtml += '</div>';
            container.html(dataHtml);
        },
        className: "page-item"
    };
    pagination.pagination(options);
    container.show();
    pagination.show();
//    console.log(count);
}

$('#form-container').submit(loadData);