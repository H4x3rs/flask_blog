$(document).ready(function(){
    $('.carousel').carousel();
    $('.collapsible').collapsible();
    $('.sidenav').sidenav();
    $('.chips').chips({
        placeholder: 'Enter a tag',
    });
     $('.chips-placeholder').chips({
         placeholder: 'Enter a tag',
         secondaryPlaceholder: '+Tag',
      });
})
