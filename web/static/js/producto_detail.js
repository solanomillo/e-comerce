// static/js/producto_detail.js
document.addEventListener('DOMContentLoaded', function() {
    const increment = document.getElementById('increment');
    const decrement = document.getElementById('decrement');
    const quantityInput = document.querySelector('input[name="cantidad"]');
  
    if (increment && decrement && quantityInput) {
      increment.addEventListener('click', function() {
        quantityInput.value = parseInt(quantityInput.value) + 1;
      });
  
      decrement.addEventListener('click', function() {
        if (parseInt(quantityInput.value) > 1) {
          quantityInput.value = parseInt(quantityInput.value) - 1;
        }
      });
    }
  });