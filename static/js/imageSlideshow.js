// https://www.w3schools.com/howto/howto_js_slideshow.asp

let slideIndex = 1;

// Next/previous controls
function plusSlides(n) {
  showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
  showSlides(slideIndex = n);
}

function checkOrientation() {
    let images = document.getElementsByClassName("imageImage");

    for (let index = 0; index < images.length; index++) {
        const element = images[index];
        if (element.naturalHeight > element.naturalWidth) {
            element.className += " portrait"
        }
    }
}

function showSlides(n) {
  let i;
  let slides = document.getElementsByClassName("imageSlide");

  if (slides.length == 0) {
    console.warn("No images found");
    let container = document.getElementsByClassName("imageContainer")[0];
    let prev = document.getElementsByClassName("prev")[0];
    let next = document.getElementsByClassName("next")[0];
    container.innerHTML = "No images available";
    prev.style.display = "none";
    next.style.display = "none";
  }

  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  slides[slideIndex-1].style.display = "block";
}