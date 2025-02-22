// Select DOM elements
const body = document.querySelector("body");
const darkLight = document.querySelector("#darkLight");
const sidebar = document.querySelector(".sidebar");
const submenuItems = document.querySelectorAll(".submenu_item");
const sidebarOpen = document.querySelector("#sidebarOpen");
const sidebarClose = document.querySelector(".collapse_sidebar");
const sidebarExpand = document.querySelector(".expand_sidebar");

// Toggle sidebar visibility when sidebar open button is clicked
sidebarOpen.addEventListener("click", () => {
    sidebar.classList.toggle("close");
});

// Collapse the sidebar and make it hoverable
sidebarClose.addEventListener("click", () => {
    sidebar.classList.add("close", "hoverable");
});

// Expand the sidebar and remove hoverable behavior
sidebarExpand.addEventListener("click", () => {
    sidebar.classList.remove("close", "hoverable");
});

// Open sidebar when hovered if it is in hoverable state
sidebar.addEventListener("mouseenter", () => {
    if (sidebar.classList.contains("hoverable")) {
        sidebar.classList.remove("close");
    }
});

// Close sidebar when mouse leaves if it is in hoverable state
sidebar.addEventListener("mouseleave", () => {
    if (sidebar.classList.contains("hoverable")) {
        sidebar.classList.add("close");
    }
});

// Toggle dark mode and change icon accordingly
darkLight.addEventListener("click", () => {
    body.classList.toggle("dark");
    if (body.classList.contains("dark")) {
        darkLight.classList.replace("bx-sun", "bx-moon");
    } else {
        darkLight.classList.replace("bx-moon", "bx-sun");
    }
});

// Toggle submenu visibility and close other open submenus
submenuItems.forEach((item, index) => {
    item.addEventListener("click", () => {
        item.classList.toggle("show_submenu");
        submenuItems.forEach((item2, index2) => {
            if (index !== index2) {
                item2.classList.remove("show_submenu");
            }
        });
    });
});

// Automatically close sidebar on small screens
if (window.innerWidth < 768) {
    sidebar.classList.add("close");
} else {
    sidebar.classList.remove("close");
}
