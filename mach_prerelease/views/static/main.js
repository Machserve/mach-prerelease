(function() {
    var burger = document.querySelector('.burger');
    var menu = document.querySelector('#'+burger.dataset.target);
    burger.addEventListener('click', function() {
        burger.classList.toggle('is-active');
        menu.classList.toggle('is-active');
    });

    particlesJS.load(
        'particles-js', 
        '/static/assets', 
        function() {
            console.log('callback - particles.js config loaded');
      },
    );
})();