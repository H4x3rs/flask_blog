(function($){
  $(function(){
      // 下拉菜单的设置
      $('.dropdown-trigger').dropdown({
          constrainWidth: false, // Does not change width of dropdown to that of the activator
          hover: true, // Activate on hover
          coverTrigger: false, // Displays dropdown below the button
          alignment: 'left' // Displays dropdown with edge aligned to the left of button
      });

      $('.button-collapse').sidenav();
      $('.parallax').parallax();
      $('.sidenav').sidenav()
      $('#comment').characterCounter();


  }); // end of document ready
})(jQuery); // end of jQuery name space
