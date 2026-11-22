let resizeTimer;
window.addEventListener("resize", () => {
    document.body.classList.add("resize_animation_stopper");
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout( () => {
        document.body.classList.remove("resize_animation_stopper");
    }, 400);
});