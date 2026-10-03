(() => {
  const body = document.querySelector("[data-admin-body]");
  const toggle = document.querySelector("[data-admin-menu]");
  const overlay = document.querySelector("[data-admin-overlay]");

  const setOpen = (open) => {
    if (!body || !toggle) return;
    body.classList.toggle("admin-nav-open", open);
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Fermer le menu" : "Ouvrir le menu");
    if (overlay) overlay.hidden = !open;
  };

  if (toggle) toggle.addEventListener("click", () => setOpen(!body.classList.contains("admin-nav-open")));
  if (overlay) overlay.addEventListener("click", () => setOpen(false));
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") setOpen(false);
  });
  document.querySelectorAll(".admin-sidebar a").forEach((link) => link.addEventListener("click", () => setOpen(false)));

  document.querySelectorAll("form").forEach((form) => {
    form.addEventListener("submit", () => {
      const button = form.querySelector('button[type="submit"]:not([data-no-loading]), input[type="submit"]');
      if (!button) return;
      button.disabled = true;
      button.classList.add("is-loading");
      if (button.tagName === "BUTTON") {
        button.dataset.originalText = button.textContent;
        button.textContent = "Traitement…";
      }
    });
  });

  document.querySelectorAll("[data-confirm]").forEach((control) => {
    control.addEventListener("click", (event) => {
      if (!window.confirm(control.dataset.confirm)) event.preventDefault();
    });
  });
})();