const flashMessage = document.querySelector('.alert');
const messageCloseButton = document.querySelector('.alert__close');
messageCloseButton.addEventListener('click', function () {
  flashMessage.style.display = 'none';
})