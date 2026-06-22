(function () {
  const root = document.documentElement;
  const key = "python-tutorial-theme";
  const saved = localStorage.getItem(key);
  if (saved === "dark") root.dataset.theme = "dark";

  const button = document.querySelector("[data-theme-toggle]");
  if (button) {
    button.addEventListener("click", () => {
      const next = root.dataset.theme === "dark" ? "light" : "dark";
      if (next === "dark") root.dataset.theme = "dark";
      else delete root.dataset.theme;
      localStorage.setItem(key, next);
    });
  }

  const search = document.querySelector("[data-search]");
  if (search) {
    const cards = Array.from(document.querySelectorAll("[data-search-card]"));
    search.addEventListener("input", () => {
      const query = search.value.trim().toLowerCase();
      for (const card of cards) {
        const text = card.textContent.toLowerCase();
        card.hidden = query && !text.includes(query);
      }
    });
  }

  const links = Array.from(document.querySelectorAll(".toc-panel a"));
  const headings = links
    .map((link) => document.getElementById(decodeURIComponent(link.getAttribute("href").slice(1))))
    .filter(Boolean);
  if ("IntersectionObserver" in window && headings.length) {
    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((entry) => entry.isIntersecting)
          .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top)[0];
        if (!visible) return;
        for (const link of links) link.classList.remove("active");
        const active = document.querySelector(`.toc-panel a[href="#${CSS.escape(visible.target.id)}"]`);
        if (active) active.classList.add("active");
      },
      { rootMargin: "-15% 0px -70% 0px", threshold: [0, 1] }
    );
    headings.forEach((heading) => observer.observe(heading));
  }
})();
