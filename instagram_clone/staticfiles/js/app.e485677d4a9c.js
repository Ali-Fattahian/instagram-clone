const searchIcon = document.querySelector('.fa-search');
const searchModal = document.querySelector('.modal-search');
const overlay = document.querySelector('.overlay');


const showModal = function () {
  overlay.classList.remove('hidden');
  searchModal.classList.remove('hidden');
}

searchIcon.addEventListener('click', showModal);

const hideModal = function () {
  if (!searchModal.classList.contains('hidden') || !overlay.classList.contains('hidden')) {
    overlay.classList.add('hidden');
    searchModal.classList.add('hidden');
  }
}

overlay.addEventListener('click', hideModal); 

document.addEventListener('keydown', function (e) {
  if (e.key === 'Escape')
    hideModal();
});
