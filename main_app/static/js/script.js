var itemCard = document.querySelectorAll('.item-card-inner');
var quantityButton = document.querySelectorAll('.flip-forward');
var detailsButton = document.querySelectorAll('.flip-backward');

for (let i = 0; i < quantityButton.length; i++) {
  quantityButton[i].addEventListener('click', function (e) {
    e.preventDefault();
    itemCard[i].classList.toggle('flipped');
  });
}

for (let i = 0; i < detailsButton.length; i++) {
  detailsButton[i].addEventListener('click', function (e) {
    e.preventDefault();
    itemCard[i].classList.toggle('flipped');
  });
}
