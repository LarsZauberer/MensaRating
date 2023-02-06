function starRate(index, rating){
    console.log(index, rating)

    let star = document.getElementById(String(index));

    rating = +(rating.replace(",", "."))
    rating = String(rating/5*100).split(".")[0] + "%"

    star.style.width = rating
}