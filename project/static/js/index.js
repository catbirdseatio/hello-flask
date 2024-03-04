document.addEventListener("DOMContentLoaded", () => {
  const burger = document.querySelector(".navbar-burger");
  const navbarMenu = document.querySelector(".navbar-menu");
  const deleteButtons =
    document.querySelectorAll(".notification .delete") || [];
  const message = document.querySelector("blockquote.message-body");
  
  deleteButtons.forEach(($delete) => {
    const $notification = $delete.parentNode;

    $delete.addEventListener("click", () => {
      $notification.parentNode.removeChild($notification);
    });
  });
  // Check for click events on the navbar burger icon
  burger.addEventListener("click", () => {
    burger.classList.toggle("is-active");
    navbarMenu.classList.toggle("is-active");
  });

  if (message) {
    console.log(message)
    message.scrollIntoView({behavior: "smooth"});
  }
});
