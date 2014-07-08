
var star = document.getElementById('star');
var width = window.innerWidth;
var height = window.innerHeight;

var direction='left';
var vertical_direction='up';

var vertical_num = Math.random();

if (vertical_num > 0.5){
	vertical_direction='up';
	} else {
	vertical_direction='down';
}


var p_width = star.clientWidth;
var p_height = star.clientHeight;

var position_marginLeft = Math.floor((Math.random()*width)+1);

var position_marginTop = Math.floor((Math.random()*height)+1);

var num = Math.random();

	if (num > 0.5){
		direction = 'left';
	} else {
		direction = 'right';
	}




setInterval(function(){
  
  if (position_marginLeft == 0) {
	direction='right';
  }

  if (position_marginTop == 0) {
	vertical_direction='down';
}


  if (position_marginLeft == (width-p_width)) {
        direction = 'left';
  }

  if (position_marginTop == (height-p_height)) {
	vertical_direction = 'up';
}



  if (position_marginLeft < (width-p_width) && direction=='right'){
       	  position_marginLeft = position_marginLeft + 1;
	  star.style.marginLeft=(position_marginLeft)+'px';
      }

  if (position_marginTop < (height-p_height) && vertical_direction == 'down'){
	  position_marginTop = position_marginTop + 1;
	  star.style.marginTop=(position_marginTop)+'px';
	}



  if (position_marginLeft > 0 && direction=='left'){
		
	  position_marginLeft = position_marginLeft - 1;
	  star.style.marginLeft=(position_marginLeft)+'px';
}

  if (position_marginTop > 0 && vertical_direction =='up'){
          position_marginTop = position_marginTop - 1;
	  star.style.marginTop=(position_marginTop)+'px';
}


},1);



