function ansConf(ease, remaining){
  var pressed = '.platform[data-ease='+ ease +']';
  $(pressed).parent().siblings('div').css({'opacity':'0'})
  $(pressed).addClass('ansConf')
  $(pressed).on("animationend", function(){
    $('.ans').remove();
    insertQuesBut(remaining);
  });
}

function insertAnsBut(due, extra, i, label) {
  $('#ques').remove();
  $('#container').append(`
  <div id='`+ label +`' class='ans'>
    <div `+ extra +` class='platform' data-ease='`+ i +`' onclick='pycmd("ease`+ i +`")'>`+ due +`</div>
  </div>
  `)
}

function insertQuesBut(remaining) {
  if ($('.ans')[0] == null) {
    $('#container').append(`
    <div id='ques' class='ans'>
      <div class='platform' onclick='pycmd("ans");'>`+ remaining +`</div>
    </div>
    `)
  }
}

function clearButs() {
  $('.ans').remove();
}