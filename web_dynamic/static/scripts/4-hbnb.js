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

var data = {}

$.ajax({
    url: 'http://127.0.0.1:5001/api/v1/places_search',
    method: 'POST',
    dataType: "json",
    contentType: "application/json; charset=utf-8",
    data: JSON.stringify(data),
    success: function (result) {
        $.each(result, (i, data) => {
            $('.place-cards').append("<article class='dip-inl-blo'><div class='cle-bot'><div class='fs-30 flo-lef w-70pc'>    <h2 class='fs-30 flo-lef'>"+data.name+"</h2></div><div class='price_by_night flo-rig'>    <p class='mt-23pc'>$"+data.price_by_night+"</p></div></div><div class='information'><div class='max_guest'>    <div class='icon_group'></div> "+data.max_guest+" Guest    </div><div class='number_rooms'>    <div class='icon_bed'></div>"+data.number_rooms+" bedroom    </div><div class='number_bathrooms'>    <div class='icon_bath'></div>"+data.number_bathrooms+"bathroom</div></div><div class='description'><p>"+data.description+"</p></div></article>")
        })
    },
});

$('button').click(function (data){
    let dicObj = {};
    dicObj.amenities = Object.keys(amenities);
    console.log(dicObj);
    $.ajax({
        url: 'http://127.0.0.1:5001/api/v1/places_search',
        method: 'POST',
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(dicObj),
        success: function(data){
            let place;
            let template;
            for (place of data){
                template = `<article>
                <div class="title_box">
                   <h2>${place.name}</h2>
                   <div class="price_by_night">$${place.price_by_night}</div>
                </div>
                <div class="information">
                   <div class="max_guest">${place.max_guest} Guests</div>
                   <div class="number_rooms">${place.number_rooms} Bedrooms</div>
                   <div class="number_bathrooms">${place.number_bathrooms} Bathrooms</div>
                </div>
                <div class="description">${place.description}</div>
             </article>`;
             $('section..places').append(template);

            }
        }
    })
})