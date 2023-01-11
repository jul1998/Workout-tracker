let timerElement = document.querySelector("#timer")

let timerBar = document.querySelector("#timer-bar")

let timerCounter = timerBar.max


let timerInterval = setInterval(()=>{
if(timerCounter<=1){
    clearInterval(timerInterval)
    window.location.href = "/timer_exercise"
}else{
    console.log(timerCounter)
    timerCounter --
   timerElement.textContent = timerCounter + "s"
   timerBar.value = timerCounter
}
},1000)







