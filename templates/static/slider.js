// Скрипт для прокрутки слайдера

const slider = document.querySelector('.slider');
const cards = document.querySelectorAll('.card');
const cardWidth = cards[0].offsetWidth + 15; // Ширина карточки + отступ между карточками
let translateX = 0;

document.querySelector('.slider-container').addEventListener('click', function(event) {
    if (event.target.classList.contains('next')) {
        translateX -= cardWidth;
        if (translateX < -(cardWidth * (cards.length - 3))) {
            translateX = 0;
        }
    } else if (event.target.classList.contains('prev')) {
        translateX += cardWidth;
        if (translateX > 0) {
            translateX = -(cardWidth * (cards.length - 3));
        }
    }
    slider.style.transform = `translateX(${translateX}px)`;
});
