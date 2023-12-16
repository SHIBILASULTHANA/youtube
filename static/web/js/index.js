const menu = document.querySelector('#menu');
const sidebar = document.querySelector('.sidebar');
menu.addEventListener('click', function () {
  sidebar.classList.toggle('show-sidebar');
  const isSidebarVisible = sidebar.classList.contains('show-sidebar');
  sidebar.style.cssText = isSidebarVisible
    ? `
        overflow-y: scroll;
        height: 80vh;
        z-index : 2;
        ::-webkit-scrollbar-thumb {
          background: transparent;
          height: 50vh;
        }
        
      `
    : '';
});
