$(document).ready(function(){


$.ajax({
	url:"/ajax_call/",
      })
	.done(function( data ) {
		alert( data );
	}); // end .done()


}); //end document




	function follow(id){
		alert(id);
	}
