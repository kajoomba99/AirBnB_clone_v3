$(function () {
  $(".popover input[type='checkbox']").click(function () {
    const amenities = checkInputs();

    const names = amenities.reduce((f, s) => {
      f.push(s.name);
      return f;
    }, []);
    $('.amenities h4').text(names);
    if (names.length === 0) { $('.amenities h4').html('&nbsp;'); }
  });

  const checkInputs = () => {
    const checks = $('.popover input:checked');
    const checbox = [];
    $.each(checks, (item, data) => {
      const object = $(data);
      const name = object.attr('data-name');
      const id = object.attr('data-id');
      checbox.push({
        name,
        id
      });
    });
    return checbox;
  };

  var data = {};

  $.ajax({
    url: 'http://127.0.0.1:5001/api/v1/places_search',
    method: 'POST',
    dataType: 'json',
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify(data),
    success: function (result) {
      $.each(result, (i, data) => {
        $('.place-cards').append("<article class='dip-inl-blo'><div class='cle-bot'><div class='fs-30 flo-lef w-70pc'>    <h2 class='fs-30 flo-lef'>" + data.name + "</h2></div><div class='price_by_night flo-rig'>    <p class='mt-23pc'>$" + data.price_by_night + "</p></div></div><div class='information'><div class='max_guest'>    <div class='icon_group'></div> " + data.max_guest + " Guest    </div><div class='number_rooms'>    <div class='icon_bed'></div>" + data.number_rooms + " bedroom    </div><div class='number_bathrooms'>    <div class='icon_bath'></div>" + data.number_bathrooms + "bathroom</div></div><div class='description'><p>" + data.description + '</p></div></article>');
      });
    }
  });

  $('button').click(() => {
    const amenities = checkInputs();
    const amenitiesId = amenities.reduce((f, s) => {
      f.push(s.id);
      return f;
    }, []);
    $.ajax({
      url: 'http://0.0.0.0:5001/api/v1/places_search',
      method: 'POST',
      dataType: 'json',
      contentType: 'application/json; charset=utf-8',
      data: JSON.stringify({ amenities: amenitiesId }),
      success: function (data) {
        let place;
        $('.place-cards').empty();
        for (place of data) {
          $('.place-cards').append(`<article class='dip-inl-blo'>
          <div class='cle-bot'>
            <div class='fs-30 flo-lef w-70pc'>
              <h2 class='fs-30 flo-lef'>${place.name}</h2>
            </div>
            <div class='price_by_night flo-rig'>
              <p class='mt-23pc'>$${place.price_by_night}</p>
            </div>
          </div>
          <div class='information'>
            <div class='max_guest'>
              <div class='icon_group'></div>${place.max_guest} Guest
            </div>
            <div class='number_rooms'>
              <div class='icon_bed'></div>${place.number_rooms} bedroom
            </div>
            <div class='number_bathrooms'>
              <div class='icon_bath'></div>${place.number_bathrooms}bathroom
            </div>
          </div>
          <div class='description'>
            <p>${place.description}</p>
          </div>
        </article>`);
        }
      }
    });
  });

  $.get('http://127.0.0.1:5001/api/v1/status/', function (data) {
    if (data.status === 'OK') {
      $('#api_status').addClass('available');
    }
  });
});
