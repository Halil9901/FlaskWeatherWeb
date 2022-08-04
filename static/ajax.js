//Calls the update_data_frame function every 10,000 milliseconds = 10 sec
//60,000 = 1min
var myVar = setInterval(update_data_frame, 10000);

//This function makes a POST request to the flask route "/update"
//The value of return response.json() is the return value of the "/update"
//In your case this is going to be the dataframe
//".then(function(myjson))..." captures the return value to be used as required
function update_data_frame () {
    url = '/update_api';
    fetch(url,{method:'POST'})
    .then(function(response) {
      return response.json();
    })
    .then(function(myJson)
    {
      store = myJson;
      //This line prints out "{somedata":"somedatavalue","somedata1":"somedatavalue1"}" every 2000 milliseconds
      console.log(store);
    });
  }