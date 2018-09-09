$(function () {

  /* Functions */

  var loadPostLike = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
//$(".show_like").html(data.like).hide()

      },
      success: function (data) {
        //alert(data.like);
          //document.write(data.like)
          $(".show_like").html(data.like).toggle()

      },
      error: function(e) {
          alert("failure");
      }
    });
  };
  
  var loadCommentLike=function () {

    var btn=$(this)
      $.ajax({
          url:btn.attr("data-url"),
          type:'get',
          dataType:'json',
          beforeSend:function () {

          },
          success:function (data) {
             //$(".show_comment_like").html(data.like).toggle()
              $("#myModal .modal-content").html(data.like)
          },
          error:function (e) {
              alert(failure)

          }
      });
      
  };

/*
  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#book-table tbody").html(data.html_book_list);
          $("#modal-book").modal("hide");
        }
        else {
          $("#modal-book .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };
*/

  /* Binding */

  // Create book
  $(".load-post-like").mouseenter(loadPostLike);
  $(".load-comment-like").click(loadCommentLike)




  $("#modal-book").on("submit", ".js-book-create-form", saveForm);


  // Update book
  $("#book-table").on("click", ".js-update-book", loadForm);
  $("#modal-book").on("submit", ".js-book-update-form", saveForm);

  // Delete book
$("#book-table").on("click", ".js-delete-book", loadForm);
$("#modal-book").on("submit", ".js-book-delete-form", saveForm);

});