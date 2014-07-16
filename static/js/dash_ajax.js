	


	function favorite(number){
	  var identifier=number.toString();
	  var hash="favorited"+identifier;
	  var tag=document.getElementById(hash);
	  if (tag.value == "favorited"){
	   tag.style.color="#9599a6";
	   tag.style.textDecoration="none";
	   tag.value = "not_favorited";
	  } else {
	   tag.style.color="#ffac33";
	   tag.style.textDecoration="underline";
	   tag.value = "favorited";
//put Jquery here

$(document).ready(function(){

$.ajax({
	url:"/ajax_call/",
	data:{identifier:identifier}
      })
	.done(function( data ) {
		alert( data );
	}); // end ajax statement

}); //end document

//end Jquery
	         }
	   }


