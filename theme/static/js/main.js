

    const sidebar = document.querySelector('.fixed.inset-0');
    const toggleButton = document.getElementById('sidebar-toggle');
    const menuButton = document.getElementById('menuButton');
    const logo = document.getElementById('logo');
    const themeBtn = document.querySelectorAll('.theme');

    menuButton.addEventListener('click', () => {
        sidebar.classList.toggle('-translate-x-full');  // Toggle sidebar visibility
        
    });

    document.addEventListener('click', (e) => {
        if (!sidebar.contains(e.target) && e.target !== toggleButton && e.target !== menuButton) {
            sidebar.classList.add('-translate-x-full');  // Close sidebar when clicked outside
            logo.classList.remove('hidden')
        }
    });

    
    

// reload page for popstate
window.onpopstate = function(event) {
    location.reload();
};
 

