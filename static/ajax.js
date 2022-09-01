const main = document.getElementById('update');
const temp = document.getElementById('temp');
const date = document.getElementById('date');

function noDelaySetInterval(func, interval) {
    func();
    return setInterval(func, interval);
}


function startSetInterval() {
    noDelaySetInterval(update_data_frame, 0);
}

//Calls the update_data_frame function every 10,000 milliseconds = 10 sec
//60,000 = 1min
var myVar = setInterval(update_data_frame, 120000);


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

      $('#temp').text(store[0]);
      $('#time').text(store[6]);
      $('#date').text(store[10]);

      $('#lastUpdateTime').text(store[7]);


      $('#condition').text(store[1]);
      $('#windSpeed').text(store[2]);
      $('#humidity').text(store[3]);
      $('#cloudCover').text(store[4]);
      $('#uv').text(store[8]);
      

      
      
     
      console.log(store);
      
    });
  }