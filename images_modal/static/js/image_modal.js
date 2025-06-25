const SELECTORS = {
  modal: "carouselModal",
  image: ".carousel-item.active img",
  modalBody: ".modal-body",
  rotation: "current-rotation",
  scale: "scale-percentage",
  carousel: "imageCarousel",
  slideEvent: "slid.bs.carousel",
  zoomInput: "zoom-input",
  counter: "image-counter",
  item: ".carousel-item",
  tooltip: '[data-bs-toggle="tooltip"]',
};

let isDragging = false;
let startX, startY;
let scale = 1,
  rotation = 0,
  translateX = 0,
  translateY = 0;

const zoomInput = document.getElementById(SELECTORS.zoomInput);
const counter = document.getElementById(SELECTORS.counter);
const carousel = document.getElementById(SELECTORS.carousel);

/* Utils */
function openImageModal(index) {
  const modal = new bootstrap.Modal(document.getElementById(SELECTORS.modal));
  modal.show();

  const bsCarousel =
    bootstrap.Carousel.getInstance(carousel) ||
    new bootstrap.Carousel(carousel, {
      interval: false /* Setting the interval to false, otherwise the carousel will automatically change to next image */,
    });
  bsCarousel.to(index);

  resetTransformState();
  updateTransform();

  /* Updating the image count value */
  if (counter) {
    counter.textContent = `Imagem ${index + 1} de ${
      carousel.querySelectorAll(".carousel-item").length
    }`;
  }
}

function normalizeRotation(angle) {
  return ((angle % 360) + 360) % 360;
}

function resetTransformState() {
  scale = 1;
  rotation = 0;
  translateX = 0;
  translateY = 0;
}

function updateZoomDisplay() {
  const zoomDisplay = document.getElementById(SELECTORS.scale);
  if (zoomDisplay) zoomDisplay.textContent = `${Math.round(scale * 100)}%`;
  if (zoomInput) zoomInput.value = Math.round(scale * 100);
}

function updateRotationDisplay() {
  const rotationDisplay = document.getElementById(SELECTORS.rotation);
  if (rotationDisplay) rotationDisplay.textContent = `${rotation}°`;
}

function updateTransform() {
  const activeImage = document.querySelector(SELECTORS.image);
  const modalBody = document.querySelector(SELECTORS.modalBody);
  if (!activeImage || !modalBody) return;

  /* Rotation Logic */
  const rotationDisplay = document.getElementById(SELECTORS.rotation);
  if (rotationDisplay) rotationDisplay.textContent = `${rotation}°`;

  /* Zoom Logic */
  const zoomDisplay = document.getElementById(SELECTORS.scale);
  if (zoomDisplay) zoomDisplay.textContent = `${Math.round(scale * 100)}%`;
  if (zoomInput) zoomInput.value = Math.round(scale * 100);

  activeImage.classList.remove("rotated-90", "rotated-270");
  const normalizedRotation = normalizeRotation(rotation);
  if (normalizedRotation === 90) activeImage.classList.add("rotated-90");
  else if (normalizedRotation === 270) activeImage.classList.add("rotated-270");

  /* Getting the new border limit with the new zoom value */
  const modalRect = modalBody.getBoundingClientRect();
  const imageWidth = activeImage.offsetWidth * scale;
  const imageHeight = activeImage.offsetHeight * scale;

  const maxX = Math.max(0, (imageWidth - modalRect.width) / 2);
  const maxY = Math.max(0, (imageHeight - modalRect.height) / 2);

  /* Fixing the translateX/Y outside of the limit */
  translateX = Math.max(-maxX, Math.min(maxX, translateX));
  translateY = Math.max(-maxY, Math.min(maxY, translateY));

  /* Applying the new style that handles rotation, zoom and position draggable */
  activeImage.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scale}) rotate(${rotation}deg)`;
}

/* Transform Controls */
function zoomIn() {
  scale = Math.min(5, scale + 0.1);
  updateTransform();
}

function zoomOut() {
  scale = Math.max(0.1, scale - 0.1);
  updateTransform();
}

function rotateLeft() {
  rotation -= 90;
  updateTransform();
}

function rotateRight() {
  rotation += 90;
  updateTransform();
}

/* Drag logic */
function onMouseDown(e) {
  isDragging = true;
  startX = e.clientX;
  startY = e.clientY;
  e.preventDefault();
}

function onMouseMove(e) {
  if (!isDragging) return;

  const dx = e.clientX - startX;
  const dy = e.clientY - startY;
  startX = e.clientX;
  startY = e.clientY;

  const image = document.querySelector(SELECTORS.image);
  const modalBody = document.querySelector(SELECTORS.modalBody);
  if (!image || !modalBody) return;

  const modalRect = modalBody.getBoundingClientRect();
  const imageWidth = image.offsetWidth * scale;
  const imageHeight = image.offsetHeight * scale;

  const maxX = Math.max(0, (imageWidth - modalRect.width) / 2);
  const maxY = Math.max(0, (imageHeight - modalRect.height) / 2);

  translateX = Math.max(-maxX, Math.min(maxX, translateX + dx));
  translateY = Math.max(-maxY, Math.min(maxY, translateY + dy));

  updateTransform();
}

function onMouseUp() {
  isDragging = false;
}

/* Event Binds */
if (zoomInput) {
  zoomInput.addEventListener("change", () => {
    let value = parseInt(zoomInput.value, 10);
    if (isNaN(value)) return;

    value = Math.max(10, Math.min(500, value));
    scale = value / 100;
    updateTransform();
  });
}

document.addEventListener("mousedown", (e) => {
  const image = document.querySelector(SELECTORS.image);
  if (image?.contains(e.target)) onMouseDown(e);
});
document.addEventListener("mousemove", onMouseMove);
document.addEventListener("mouseup", onMouseUp);

/* Carousel Slide Event */
if (carousel) {
  const totalImages = carousel.querySelectorAll(SELECTORS.item).length;

  carousel.addEventListener(SELECTORS.slideEvent, (event) => {
    resetTransformState();
    updateTransform();

    const currentIndex = event.to + 1;
    if (counter)
      counter.textContent = `Imagem ${currentIndex} de ${totalImages}`;
  });
}

/* Initializing the tooltip */
function initTooltips() {
  const tooltipElements = document.querySelectorAll(SELECTORS.tooltip);
  tooltipElements.forEach((el) => new bootstrap.Tooltip(el));
}

if (document.readyState !== "loading") initTooltips();
else document.addEventListener("DOMContentLoaded", initTooltips);
