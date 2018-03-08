
//CKeditor init
document.addEventListener("DOMContentLoaded", function(event) { 
  //dom ready...
  setTimeout(function(){ 
       ClassicEditor
        .create( document.querySelector('.ckeditor') )
        .then( editor => {
            console.log( editor );
        } )
        .catch( error => {
            console.error( error );
        } );
      
    },400);
 
});

