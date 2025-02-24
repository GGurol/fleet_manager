// Select DOM elements
const body = document.querySelector("body");
const darkLight = document.querySelector("#darkLight");
const sidebar = document.querySelector(".sidebar");
const submenuItems = document.querySelectorAll(".submenu_item");
const sidebarOpen = document.querySelector("#sidebarOpen");
const sidebarClose = document.querySelector(".collapse_sidebar");
const sidebarExpand = document.querySelector(".expand_sidebar");

// Function to apply dark mode based on stored preference
function applyDarkMode(isDark) {
    if (isDark) {
        body.classList.add("dark");
        darkLight.classList.replace("bx-sun", "bx-moon");
    } else {
        body.classList.remove("dark");
        darkLight.classList.replace("bx-moon", "bx-sun");
    }
}

// Check for stored dark mode preference on page load
document.addEventListener("DOMContentLoaded", () => {
    const darkModeEnabled = localStorage.getItem("darkMode") === "enabled";
    applyDarkMode(darkModeEnabled);
});

// Toggle dark mode and store preference
darkLight.addEventListener("click", () => {
    const darkModeEnabled = body.classList.toggle("dark");
    localStorage.setItem("darkMode", darkModeEnabled ? "enabled" : "disabled");
    applyDarkMode(darkModeEnabled);
});

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
