# Place all the behaviors and hooks related to the matching controller here.
# All this logic will automatically be available in application.js.
# You can use CoffeeScript in this file: http://coffeescript.org/
$ ->
  $(".thumbImg").click (e) ->
    $.ajax({
        url: "log",
        data: {method: "watched", name: $(this).data("name"), season: $(this).data("season"), episode: $(this).data("episode")}
      });
    $(this).removeClass("unseen");
#All objects with class "thumbImg"
#Have an onclick function
#That AJAX's home
#With data [Name, Se, Ep]
#And tells Vegarails to turn the "Watched" field false
