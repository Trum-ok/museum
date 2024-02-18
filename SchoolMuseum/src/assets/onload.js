// Функция, которая запускается при загрузке страницы
window.onload = function() {
    // Находим элемент с классом "text-animation"
    var textElement = document.querySelector('.text-animation');
    // Получаем текст из элемента
    var text = textElement.innerText;
    // Очищаем текст в элементе
    textElement.innerText = '';
    // Проходимся по каждому символу текста
    for (var i = 0; i < text.length; i++) {
        // Создаем новый элемент <span> для символа
        var span = document.createElement('span');
        // Устанавливаем текст в <span> элемент
        span.innerText = text[i];
        // Добавляем <span> элемент внутрь "text-animation" элемента
        textElement.appendChild(span);
    }
    // Устанавливаем анимацию набора текста
    textElement.style.animation = 'typing 2s steps(80, end)';
    // Устанавливаем анимацию только один раз, без повторений
    textElement.style.animationFillMode = 'forwards';
};