$(function () {
    $(".popover input[type='checkbox']").click(function () {
        let amenities = checkInputs()
        $('.amenities h4').text(amenities);
        if (amenities.length == 0)
        $('.amenities h4').html('&nbsp;');
    });

})
let checkInputs = () => {
    let checks = $('.popover input:checked')
    let checbox = []
    $.each(checks, (item, data) => {
        let object = $(data)
        let name = object.attr('data-name')
        let id = object.attr('data-id')
        checbox.push(name)

    })
    return checbox
}
$.get('http://0.0.0.0:5001/api/v1/status/', function(data) {
    if (data.status === 'OK') {
        $('#api_status').addClass('available')
    }
})
