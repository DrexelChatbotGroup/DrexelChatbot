var $messages = $('.messages-content'),
    d, h, m,
    i = 0;

$(window).load(function() {
  $messages.mCustomScrollbar();
  setTimeout(function() {
    welcomeMessage();
  }, 100);
});

function updateScrollbar() {
  $messages.mCustomScrollbar("update").mCustomScrollbar('scrollTo', 'bottom', {
    scrollInertia: 10,
    timeout: 0
  });
}

function setDate(){
  d = new Date()
  if (m != d.getMinutes()) {
    m = d.getMinutes();
    $('<div class="timestamp">' + d.getHours() + ':' + (m < 10 ? "0"+m : m) + '</div>').appendTo($('.message:last'));
  }
  $('<div class="timestamp">' + d.getHours() + ':' + (m < 10 ? "0"+m : m) + '</div>').appendTo($('.message:last'));
}

function insertMessage() {
  msg = $('.message-input').val();
  if ($.trim(msg) == '') {
    return false;
  }
  disableInput();
  
  $('<div class="message message-personal">' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
  setDate();
  $('.message-input').val(null);
  updateScrollbar();
  setTimeout(function() {
    sendMessage();
  }, 500);
}

$('.message-submit').click(function() {
  insertMessage();
});

$(window).on('keydown', function(e) {
  if (e.which == 13) {
    insertMessage();
    return false;
  }
});

var Fake = [
  'zzz...'
]

function welcomeMessage(){
	$('<div class="message loading new"><figure class="avatar"><img src="../drexel.png" /></figure><span></span></div>').appendTo($('.mCSB_container'));
	updateScrollbar();

	setTimeout(function() {
		$('.message.loading').remove();
		$('<div class="message new"><figure class="avatar"><img src="../drexel.png" /></figure>' + 'Welcome to DrexelChatbot!' + '</div>').appendTo($('.mCSB_container')).addClass('new');
		setDate();
		updateScrollbar();
		
		$('<div class="message loading new"><figure class="avatar"><img src="../drexel.png" /></figure><span></span></div>').appendTo($('.mCSB_container'));
		updateScrollbar();

		setTimeout(function() {
			$('.message.loading').remove();
			$('<div class="message new"><figure class="avatar"><img src="../drexel.png" /></figure>' + 'Enter a question you would like to ask me!' + '</div>').appendTo($('.mCSB_container')).addClass('new');
			setDate();
			updateScrollbar();
		}, 750);
	}, 500);
	
	
}

function sendMessage() {
  if ($('.message-input').val() != '') {
    return false;
  }
  $('<div class="message loading new"><figure class="avatar"><img src="../drexel.png" /></figure><span></span></div>').appendTo($('.mCSB_container'));
  updateScrollbar();

  setTimeout(function() {
	  
	$.ajax({
		url: "/chatbot/api?query="+msg,
		method: 'GET',
		success:function(a){
			console.log(a);
			$('.message.loading').remove();
   			$('<div class="message new"><figure class="avatar"><img src="../drexel.png" /></figure>' + a.content + '</div>').appendTo($('.mCSB_container')).addClass('new');
    		setDate();
    		updateScrollbar();
    		enableInput();
    		focusTextBox();
    	},
    	error:function(a){
    		$('.message.loading').remove();
   			$('<div class="message new"><figure class="avatar"><img src="../drexel.png" /></figure>' + Fake[0] + '</div>').appendTo($('.mCSB_container')).addClass('new');
    		setDate();
    		updateScrollbar();
    		enableInput();
    		focusTextBox();
    	}
	});
    
  }, 0);

}

function disableInput(){
  $(".message-input").attr("disabled", true); 
  $(".message-submit").attr("disabled", true); 
}

function enableInput(){
  $(".message-input").attr("disabled", false); 
  $(".message-submit").attr("disabled", false); 
}

function focusTextBox(){
	$(".message-input").focus(function(){
		setTimeout(function(){
			updateScrollbar();
		}, 200);
	});
}

function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
}