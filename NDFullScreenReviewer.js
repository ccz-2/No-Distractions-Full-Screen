//var op = .5; //Defined in python

if (!$("#NDFullScreenInjected").length) {
  $('head').append(`
  <style>
  * {
    cursor: none;
  }
  </style>
  `);
}