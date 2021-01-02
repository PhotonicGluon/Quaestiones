function updateTime(k) {
    if (k < 10) {
        return "0" + k;
    } else {
        return k;
    }
}

function getTimeLeft(timeInSeconds) {
    // Express the seconds in terms of days, hours, minutes and seconds
    let days = Math.floor(timeInSeconds / 60 / 60 / 24);
    let hours = Math.floor((timeInSeconds - days * 60 * 60 * 24) / 60 / 60);
    let minutes = Math.floor((timeInSeconds - days * 60 * 60 * 24 - hours * 60 * 60) / 60);
    let seconds = timeInSeconds - days * 60 * 60 * 24 - hours * 60 * 60 - minutes * 60;

    // Update the hours, minutes and seconds
    days = updateTime(days);
    hours = updateTime(hours);
    minutes = updateTime(minutes);
    seconds = updateTime(seconds);

    // Return the string representation
    return days + ":" + hours + ":" + minutes + ":" + seconds;
}

function startClock(clockStartingTimes) {
    // Get all the clock elements
    let clocks = document.getElementsByClassName("clock");

    // Iterate through every clock and set their starting time
    for (let i = 0; i < clocks.length; i++) {
        // Get the ID of the clock
        let id = "clock-" + i;

        // Find the number of seconds left on the clock
        let secondsLeft = clockStartingTimes[i];

        // Set the initial value onto the clock
        if (secondsLeft > 0) {
            document.getElementById(id).innerText = getTimeLeft(secondsLeft);
        }

        // Update the clock every second
        let interval = setInterval(() => {
            if (secondsLeft === 0) {
                clearInterval(interval);
                document.getElementById(id).innerText = "";
            } else {
                secondsLeft -= 1;
                document.getElementById(id).innerText = getTimeLeft(secondsLeft);
            }
        }, 1000);
    }
}

window.onload = function () {
    startClock(releaseDatetimes)
};
