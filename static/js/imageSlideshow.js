// Maintained by: Ian, Robin
// https://www.w3schools.com/howto/howto_js_slideshow.asp

// Which images is currently being shown
let slideIndex = 1;

// Next/previous controls
function plusSlides(n) {
  showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
  showSlides(slideIndex = n);
}

// Check the orientation of the images and set the object-fit property accordingly
function checkOrientation() {
  let images = document.getElementsByClassName("imageImage");

  for (let index = 0; index < images.length; index++) {
      const element = images[index];
      if (element.naturalHeight > element.naturalWidth && !element.className.includes("portrait")) {
          // The image is a portrait and needs to be resized
          element.style.objectFit = "contain";
      }
  }

  images = document.getElementsByClassName("coverimage")
  for (let index = 0; index < images.length; index++) {
      const element = images[index];
      if (element.naturalHeight > element.naturalWidth && !element.className.includes("portrait")) {
          // The image is a portrait and needs to be resized
          element.style.objectFit = "contain";
      }
  }
}

function showSlides(n) {
  let i;
  let slides = document.getElementsByClassName("imageSlide");

  // Check if there are any images
  if (slides.length == 0) {
    console.warn("No images found");
    let container = document.getElementsByClassName("imageContainer")[0];
    let prev = document.getElementsByClassName("prev")[0];
    let next = document.getElementsByClassName("next")[0];
    container.innerHTML = "No images available";
    prev.style.display = "none";
    next.style.display = "none";
  }

  if (n > slides.length) {slideIndex = 1}  // If the index is too high, reset it
  if (n < 1) {slideIndex = slides.length}  // If the index is too low, reset it
  for (i = 0; i < slides.length; i++) {  // Hide all images
    slides[i].style.display = "none";
  }
  slides[slideIndex-1].style.display = "block";  // Only show the current image
}