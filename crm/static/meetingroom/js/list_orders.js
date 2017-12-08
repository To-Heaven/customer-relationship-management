$.each($("table tr"), function () {
    var num = 0;
   $.each($(this).children(), function () {
       num += 1;
       if (num>14){
           $(this).remove();
       }
   })
});