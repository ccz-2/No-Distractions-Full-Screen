function ansConf(ease, remaining){
  var pressed = '.platform[data-ease='+ ease +']';
  $(pressed).parent().siblings('div').css({'opacity':'0', 'transition': '0.3s'})
  $(pressed).addClass('ansConf')
  $(pressed).on("animationend", function(){
    $('.button').remove();
    insertQuesBut(remaining);
  });
}

function insertAnsBut(due, extra, i, label) {
  $('.ques').remove();
  $('#container').append(`
  <div id='`+ label +`' class='ans button'>
    <div `+ extra +` class='platform' data-ease='`+ i +`' onclick='pycmd("ease`+ i +`")'>`+ due +`</div>
  </div>
  `)
}

function insertQuesBut(remaining) {
  if ($('.ans')[0] == null) {
    $('.ques').remove();
    $('#container').append(`
    <div class='ques button'>
      <div class='platform' onclick='pycmd("ans");'>`+ remaining +`</div>
    </div>
    `)
  }
}

function clearButs() {
  $('.button').remove();
}