function emptyDiv(){
  $("#filtered_tweets ol").html("");
}

//create submit function for drop down menu
function submit(){
  emptyDiv();
  var selected_value = $("#filters").children("option:selected").val();
  var data_to_send = JSON.stringify({ "value": selected_value });
  $.ajax({
    url: "/api/filter",
    method: "post",
    data: data_to_send
  });
}

function send_word(){
  emptyDiv();
  var selected_value = $("#word").val();
  var data_to_send = JSON.stringify({ "value": selected_value });
  $.ajax({
    url: "/api/filter",
    method: "post",
    data: data_to_send
  });
}

// create a tweets block
block('#unfiltered_tweets').tweets({
  memory: 20
});

block('#filtered_tweets').tweets({
  memory: 20
});

block('#organiser_tweets').tweets({
  memory: 20
});

block('#word_cloud').wordcloud({
    filter_function: function(cat, val, max) {
        return val >= 0; // do not display words seen less than 3 times
    }
});

events.connect('goodword', '#word_cloud');
events.connect('badword', '#word_cloud');
events.connect('unfiltered_tweet', '#unfiltered_tweets');
events.connect('filtered_tweet', '#filtered_tweets');
events.connect('organiser_tweet', '#organiser_tweets');
