"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
window.setInterval(setTime, 1000);
window.setInterval(getData, 5000);
function setTime() {
    let date = new Date();
    let clock = document.getElementById("clock");
    if (clock != null) {
        clock.innerHTML = date.toLocaleTimeString();
    }
}
function getData() {
    return __awaiter(this, void 0, void 0, function* () {
        let data = fetch('http://localhost:1111/data')
            .then(response => response.json())
            .then(data => writeToHTML(data));
    });
}
function writeToHTML(jsondata) {
    return __awaiter(this, void 0, void 0, function* () {
        let data = JSON.parse(jsondata);
        let room = document.getElementById("room");
        let temp = document.getElementById("temp");
        let humid = document.getElementById("humid");
        let tempLimit = document.getElementById("tempLimit");
        let humidLimit = document.getElementById("humidLimit");
        if (room != null)
            room.innerHTML = data.room;
        if (temp != null)
            temp.innerHTML = data.temp.toFixed(1);
        if (humid != null)
            humid.innerHTML = data.humid.toFixed(1);
        if (tempLimit != null)
            tempLimit.innerHTML = data.tlimit.toFixed(1);
        if (humidLimit != null)
            humidLimit.innerHTML = data.hlimit.toFixed(1);
    });
}
window.onload = function () {
    getData();
};
