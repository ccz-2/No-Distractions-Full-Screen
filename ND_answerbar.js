//No Distractions Full Screen v4.0

function ansConf(ease, remaining){
  var pressed = '.platform[data-ease='+ ease +']';
  if ($(pressed)[0] != null) {
    $(pressed).parent().siblings('div').css({'opacity':'0', 'transition': '0.3s'})
    $(pressed).addClass('ansConf')
    $(pressed).on("animationend", function(){
      $('.button').remove();
      insertQuesBut(remaining);
    });
  }
  else {
      $('.button').remove();
      insertQuesBut(remaining);
  }
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