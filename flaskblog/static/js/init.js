(function($){
  $(function(){
      // 下拉菜单的设置
      $('.dropdown-button').dropdown({
          inDuration: 300,
          outDuration: 225,
          constrainWidth: 240, // Does not change width of dropdown to that of the activator
          hover: true, // Activate on hover
          gutter: 0, // Spacing from edge
          belowOrigin: true, // Displays dropdown below the button
          alignment: 'left', // Displays dropdown with edge aligned to the left of button
          stopPropagation: false
      });

      $('.button-collapse').sideNav();
      $('.parallax').parallax();

      $('#comment').characterCounter();


  }); // end of document ready
})(jQuery); // end of jQuery name space