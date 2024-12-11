


document.querySelector('form').addEventListener('submit', function(event) {
    const inputs = this.querySelectorAll('input');
    inputs.forEach(function(input) {
        input.value = input.value.trim();
    });
});

document.querySelectorAll('input').forEach(function(input) {
    input.addEventListener('blur', function() {
        input.value = input.value.trim();
    });
});
