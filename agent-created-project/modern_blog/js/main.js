document.addEventListener('DOMContentLoaded', function() {
    const nav = document.querySelector('nav ul');
    const toggle = document.createElement('div');
    toggle.className = 'nav-toggle';
    toggle.innerHTML = 'Menu';
    document.querySelector('header').insertBefore(toggle, nav);

    toggle.addEventListener('click', function() {
        nav.classList.toggle('active');
    });
});