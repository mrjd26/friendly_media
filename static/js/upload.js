
$(document).ready(function(){


$(function(){
   var twitter = document.getElementById("twitter_checkbox");
   var char_count = document.getElementById("char_count");

   if (twitter.checked) {
	
//         char_count.style.visibility="visible";
//   } else {

//         char_count.style.visibility="hidden";
//   }
//}); //end state check function
var count=0;
var output ='0';
$("#id_text").keyup(function(){
   
   var text_count=document.getElementById("id_text").value.length;
   var link_count=document.getElementById("id_link").value.length;
   if (link_count >0) {
      count = text_count + 22;
   } else {
      count = text_count;
   }
      output = count.toString();

   if (count > 140) {
	document.getElementById("id_text").style.color="red";
   } else {
        document.getElementById("id_text").style.color="black";
   }

   $("#id_text").tooltip({    items: 'textarea',
				content: output }).tooltip("open");

}); //end id_text function

$("#id_link").keyup(function(){
  
  var text_count=document.getElementById("id_text").value.length;
  var link_count=document.getElementById("id_link").value.length;
  if (link_count >0){
     count = text_count + 22;
  } else {
     count = text_count;
  }
     output = count.toString();

  if (count > 140) {
	document.getElementById('id_link').style.color="red";
  } else {
	document.getElementById('id_link').style.color="black";
  }

  $("#id_link").tooltip({	items:'input',
				content: output }).tooltip("open");

}); //end id_link function


$('#id_link').mouseover(function(){
  $(this).tooltip({items:'input',content:output}).tooltip("open");
});

$('#id_text').mouseover(function(){
  $(this).tooltip({items:'textarea',content:output}).tooltip("open");
});

} //end if statement

}); //end state check function

}); //end document.ready
