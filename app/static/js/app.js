const activeNavBar = () => {
  const curUrl = window.location.pathname;
  const $navBar = document.querySelectorAll("nav a");
  const navToArray = [...$navBar];
  navToArray.forEach((el) => {
    if (el.pathname == curUrl) el.classList.add("active-nav");
  });
};
document.addEvenetListener("load", activeNavBar());
