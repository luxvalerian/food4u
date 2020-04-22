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

var modal = document.getElementById('cartModal');

var btn = document.getElementById('openModal');

var span = document.getElementsByClassName('close')[0];

btn.onclick = function () {
  modal.style.display = 'block';
};

span.onclick = function () {
  modal.style.display = 'none';
};

window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = 'none';
  }
};

document.addEventListener('DOMContentLoaded', function () {
  var elems = document.querySelectorAll('.dropdown-trigger');
  var instances = M.Dropdown.init(elems);
});