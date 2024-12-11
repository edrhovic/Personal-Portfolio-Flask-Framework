function adjustResponsive() {
    let width = window.innerWidth;

    if (width <= 576) { 
        document.querySelector('.text').style.fontSize = '1.6em'; 
        document.querySelectorAll('.form-container input').forEach(input => {
            input.style.fontSize = '1em';
            input.style.padding = '0.6em 1em';
            input.style.width = '100%'; 
        });
        document.querySelector('button').style.fontSize = '1em';
        document.querySelector('button').style.padding = '0.6em 1em';
    }
    else if (width <= 768) { 
        document.querySelector('.text').style.fontSize = '2.0em'; 
        document.querySelectorAll('.form-container input').forEach(input => {
            input.style.fontSize = '1.1em';
            input.style.padding = '0.8em 1.5em';
            input.style.width = '100%';
        });
        document.querySelector('button').style.fontSize = '1.1em';
        document.querySelector('button').style.padding = '0.8em 1.5em';
    }
    else if (width <= 992) {
        document.querySelector('.text').style.fontSize = '2.2em'; 
        document.querySelectorAll('.form-container input').forEach(input => {
            input.style.fontSize = '1.1em';
            input.style.padding = '0.9em 2em';
            input.style.width = '90%'; 
        });
        document.querySelector('button').style.fontSize = '1.1em';
        document.querySelector('button').style.padding = '0.9em 2em';
    }
    else {
        document.querySelector('.text').style.fontSize = '2.5em'; 
        document.querySelectorAll('.form-container input').forEach(input => {
            input.style.fontSize = '1.2em';
            input.style.padding = '1em 2.5em';
            input.style.width = '80%'; 
        });
        document.querySelector('button').style.fontSize = '1.2em';
        document.querySelector('button').style.padding = '1em 2.5em';
    }
}

window.addEventListener('resize', adjustResponsive);
window.addEventListener('load', adjustResponsive);

document.addEventListener("DOMContentLoaded", function () {
    const deleteProfileModal = new bootstrap.Modal(document.getElementById('deleteProfileModal'));
});

function toggleMenu() {
    const navBar = document.getElementById('nav-bar');
    navBar.classList.toggle('open');
    const menu = document.getElementById('menu');
    menu.classList.toggle('show');
}

function adjustLayout() {
    const boxes = document.querySelectorAll('.box-container');
    
    let numColumns;
    const screenWidth = window.innerWidth;

    if (screenWidth >= 1024) {
        numColumns = 4;
    } else if (screenWidth >= 768) {
        numColumns = 3;
    } else if (screenWidth >= 480) {
        numColumns = 2;
    } else {
        numColumns = 1;
    }

    const boxWidth = (100 / numColumns) - (2 * (numColumns - 1) * 100 / (numColumns * 100));

    boxes.forEach(box => {
        box.style.width = `${boxWidth}%`;
    });
}

adjustLayout();
window.addEventListener('resize', adjustLayout);
