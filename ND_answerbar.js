//No Distractions Full Screen v4.0

function ansConf(ease, remaining){
  var pressed = '.button[data-ease='+ ease +']';
  if ($(pressed)[0] != null) {
    $(pressed).parent().siblings('div').css({'opacity':'0', 'transition': '0.3s'})
    $(pressed).addClass('ansConf')
    $(pressed).on("animationend", function(){
      $('.button_container').remove();
      insertQuesBut(remaining);
    });
  }
  else {
      $('.button_container').remove();
      insertQuesBut(remaining);
  }
}

function insertAnsBut(due, extra, i, label) {
  $('.ques').remove();
  $('#container').append(`
  <div id='`+ label +`' class='ans button_container'>
    <div `+ extra +` class='button' data-ease='`+ i +`' onclick='pycmd("ease`+ i +`")'>`+ due +`</div>
  </div>
  `)
  positionBar()
}

function insertQuesBut(remaining) {
  if ($('.ans')[0] == null) {
    $('.ques').remove();
    $('#container').append(`
    <div class='ques button_container'>
      <div class='button' onclick='pycmd("ans");'>`+ remaining +`</div>
    </div>
    `)
    positionBar()
  }
}

function clearButs() {
  $('.button_container').remove();
}

window.barPos = 'bottom';
function positionBar() {
  if (window.barPos == 'top'){
    $('#container,.ans,.ques,.button').addClass('top');
  }
  else if (window.barPos == 'left'){
    $('#container,.ans,.ques,.button').addClass('left');
  }
  else if (window.barPos == 'right'){
    $('#container,.ans,.ques,.button').addClass('right');
  }
  else {
    $('#container,.ans,.ques,.button').addClass('bottom');
  }
}


if (showQuestion.wrapped == null){
  var og_showQuestion = showQuestion
  window.showQuestion = function(txt, maxTime_) {
    og_showQuestion.call(this, txt, maxTime_);
    $("#middle")[0].innerHTML = '';
    pycmd("NDFS_showQues");
  }
  showQuestion.wrapped = true
}
if (showAnswer.wrapped == null){
  var og_showAnswer = showAnswer
  window.showAnswer = function(txt) {
    og_showAnswer.call(this, txt);
    $("#middle")[0].innerHTML = '';
    pycmd("NDFS_showAns"); 
  }
  showAnswer.wrapped = true
}