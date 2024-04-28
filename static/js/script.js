document.addEventListener('DOMContentLoaded', function () {
    const title = document.querySelector('.title');
    title.style.transition = 'transform 0.5s ease';
    title.style.transform = 'scale(1.1)';
    title.addEventListener('mouseover', function () {
        this.style.transform = 'scale(1.2)';
    });
    title.addEventListener('mouseout', function () {
        this.style.transform = 'scale(1.1)';
    });
});
