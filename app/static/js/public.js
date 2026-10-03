(() => {
  const toggle = document.querySelector("[data-nav-toggle]");
  const nav = document.querySelector("[data-nav]");
  const backdrop = document.querySelector("[data-nav-backdrop]");
  const header = document.querySelector("[data-header]");
  const mobileNav = window.matchMedia("(max-width: 980px)");

  const navIsOpen = () => Boolean(nav && nav.classList.contains("is-open"));

  const closeNav = ({ restoreFocus = false } = {}) => {
    if (!toggle || !nav) return;
    nav.classList.remove("is-open");
    document.body.classList.remove("nav-open");
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-label", "Ouvrir la navigation");
    if (backdrop) backdrop.hidden = true;
    if (restoreFocus) toggle.focus();
  };

  const openNav = () => {
    if (!toggle || !nav || !mobileNav.matches) return;
    nav.classList.add("is-open");
    document.body.classList.add("nav-open");
    toggle.setAttribute("aria-expanded", "true");
    toggle.setAttribute("aria-label", "Fermer la navigation");
    if (backdrop) backdrop.hidden = false;

    const firstLink = nav.querySelector("a[href]");
    if (firstLink) firstLink.focus();
  };

  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      if (navIsOpen()) closeNav();
      else openNav();
    });

    nav.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => closeNav());
    });

    if (backdrop) {
      backdrop.addEventListener("click", () => closeNav({ restoreFocus: true }));
    }

    document.addEventListener("keydown", (event) => {
      if (!navIsOpen() || !mobileNav.matches) return;

      if (event.key === "Escape") {
        event.preventDefault();
        closeNav({ restoreFocus: true });
        return;
      }

      if (event.key !== "Tab") return;

      const focusables = [
        toggle,
        ...nav.querySelectorAll('a[href], button:not([disabled])'),
      ].filter((element) => element.offsetParent !== null);

      if (!focusables.length) return;

      const first = focusables[0];
      const last = focusables[focusables.length - 1];

      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    });

    const handleBreakpointChange = (event) => {
      if (!event.matches) closeNav();
    };

    if (typeof mobileNav.addEventListener === "function") {
      mobileNav.addEventListener("change", handleBreakpointChange);
    } else if (typeof mobileNav.addListener === "function") {
      mobileNav.addListener(handleBreakpointChange);
    }
  }

  const updateHeader = () => {
    if (header) header.classList.toggle("is-scrolled", window.scrollY > 8);
  };
  updateHeader();
  window.addEventListener("scroll", updateHeader, { passive: true });

  document.querySelectorAll("form").forEach((form) => {
    form.addEventListener("submit", () => {
      const button = form.querySelector('button[type="submit"], input[type="submit"]');
      if (!button || button.dataset.noLoading !== undefined) return;
      button.disabled = true;
      button.classList.add("is-loading");
      if (button.tagName === "BUTTON") {
        button.dataset.originalText = button.textContent;
        button.textContent = "Traitement…";
      }
    });
  });

  if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches && "IntersectionObserver" in window) {
    const items = document.querySelectorAll("[data-reveal]");
    items.forEach((item) => item.classList.add("reveal-ready"));
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    items.forEach((item) => observer.observe(item));
  }
})();