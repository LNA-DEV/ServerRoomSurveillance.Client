window.setInterval(setTime, 1000);
window.setInterval(getData, 5000);

function setTime()
{
  let date = new Date();
  let clock = document.getElementById("clock");
  if(clock != null)
  {
    clock.innerHTML = date.toLocaleTimeString();
  }
}

async function getData()
{
    let data =  fetch('http://localhost:1111/data')
    .then(response => response.json())
    .then(data => writeToHTML(data));
}

async function writeToHTML(jsondata: string)
{
    let data = JSON.parse(jsondata);

    let room = document.getElementById("room");
    let temp = document.getElementById("temp");
    let humid = document.getElementById("humid");
    let tempLimit = document.getElementById("tempLimit");
    let humidLimit = document.getElementById("humidLimit");

    if(room != null)
    room.innerHTML = data.room;
    if(temp != null)
    temp.innerHTML = data.temp.toFixed(1);
    if(humid != null)
    humid.innerHTML = data.humid.toFixed(1);
    if(tempLimit != null)
    tempLimit.innerHTML = data.tlimit.toFixed(1);
    if(humidLimit != null)
    humidLimit.innerHTML = data.hlimit.toFixed(1);
}

window.onload = function() {
    getData();
  };