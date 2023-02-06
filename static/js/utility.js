function starRate(index, rating){
    console.log(index, rating)

    let star = document.getElementById("stars-" + index);

    rating = +(rating.replace(",", "."))
    rating = String(rating/5*100) + "%"

    star.style.width = rating
}

function starHover(stars, i){

    for(let j = 0; j <= i; j++){
        stars[j].style.backgroundImage = "url('../../static/images/yellowstar.png')"


    }


}

function stopStarHover(){
    for(let j = 0; j < 5; j++){
        stars[j].style.backgroundImage = "url('../../static/images/emptystar.png')"
    }
}
