function main() {
    var abwesendItems = document.querySelectorAll('#abwesend li');
    var abwesendCounter = 0;
    setInterval(news_switcher(abwesendCounter, abwesendItems), 5000);
    var ausfallItems = document.querySelectorAll('#ausfall li');
    var ausfallCounter = 0;
    setInterval(news_switcher(ausfallCounter, ausfallItems), 5000);
    var exkursionItems = document.querySelectorAll('#exkursionen li');
    var exkursionCounter = 0;
    setInterval(news_switcher(exkursionCounter, exkursionItems), 5000);
    var uItems = document.querySelectorAll('#u li');
    var uCounter = 0;
    setInterval(news_switcher(uCounter, uItems), 5000);

    let posts = document.querySelectorAll('.posts article');
    let postCounter = 0;
    news_switcher(postCounter, posts)
    setInterval(news_switcher(postCounter, posts), 10000);

    set_time();
    setInterval(set_time, 60000);

    // Autoreload after 10min
    setTimeout(function() {
        location.reload();
    }, 600000);
}

function set_time() {
    var time = document.querySelector('#clock');
    var date = document.querySelector('#date');
    time.innerHTML = randomTime();
    date.innerHTML = randomDate();
}

function randomTime() {
    hrs = Math.round(Math.random() * 24);
    mins = Math.round(Math.random() * 60);
    return hrs + ":" + mins;
}

function randomDate() {
    day = Math.round(Math.random() * 31);
    month = Math.round(Math.random() * 12);
    year = Math.round(Math.random() * 2199);
    return day + "." + month + "." + year + " n.Chr.";
}

function news_switcher(counter, tickerItems) {
    function inner() {
        tickerItems[counter].style.opacity = 0;
        setTimeout(function() {
            tickerItems[counter].style.opacity = 1;
        }, 500);
        counter++;
        if (counter >= tickerItems.length) {
            counter = 0;
        }
    }
    return inner;
}

addEventListener("DOMContentLoaded", main, false);