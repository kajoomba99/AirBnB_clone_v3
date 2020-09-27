$(function () {
  $(".popover input[type='checkbox']").click(function () {
    const amenities = checkInputs();
    $('.amenities h4').text(amenities);
    if (amenities.length === 0) { $('.amenities h4').html('&nbsp;'); }
  });
});
const checkInputs = () => {
  const checks = $('.popover input:checked');
  const checbox = [];
  $.each(checks, (item, data) => {
    const object = $(data);
    const name = object.attr('data-name');
    // const id = object.attr('data-id');
    checbox.push(name);
  });
  return checbox;
};
