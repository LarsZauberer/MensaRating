function starRate(index, rating){
    console.log(index, rating)

    let star = document.getElementById("stars-" + index);

    rating = +(rating.replace(",", "."))
    rating = String(rating/5*100) + "%"

    star.style.width = rating
}