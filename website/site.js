(function () {
  const root = document.documentElement;
  const themeKey = "python-tutorial-theme";
  const savedTheme = localStorage.getItem(themeKey);
  if (savedTheme === "dark") root.dataset.theme = "dark";

  const body = document.body;
  const navToggle = document.querySelector("[data-nav-toggle]");
  const navBackdrop = document.querySelector("[data-nav-backdrop]");

  const closeNav = () => {
    body.classList.remove("nav-open");
    if (navToggle) navToggle.setAttribute("aria-expanded", "false");
  };

  const openNav = () => {
    body.classList.add("nav-open");
    if (navToggle) navToggle.setAttribute("aria-expanded", "true");
  };

  if (navToggle) {
    navToggle.addEventListener("click", () => {
      if (body.classList.contains("nav-open")) closeNav();
      else openNav();
    });
  }

  if (navBackdrop) navBackdrop.addEventListener("click", closeNav);
  document.querySelectorAll(".chapter-nav a").forEach((link) => {
    link.addEventListener("click", closeNav);
  });

  const themeButton = document.querySelector("[data-theme-toggle]");
  if (themeButton) {
    themeButton.addEventListener("click", () => {
      const next = root.dataset.theme === "dark" ? "light" : "dark";
      if (next === "dark") root.dataset.theme = "dark";
      else delete root.dataset.theme;
      localStorage.setItem(themeKey, next);
    });
  }

  const search = document.querySelector("[data-search]");
  if (search) {
    const cards = Array.from(document.querySelectorAll("[data-search-card]"));
    const status = document.createElement("span");
    status.className = "meta-pill strong";
    status.setAttribute("aria-live", "polite");
    search.insertAdjacentElement("afterend", status);

    const updateStatus = () => {
      const visible = cards.filter((card) => !card.hidden).length;
      status.textContent = `${visible} / ${cards.length}`;
    };

    search.addEventListener("input", () => {
      const query = search.value.trim().toLowerCase();
      for (const card of cards) {
        const text = card.textContent.toLowerCase();
        card.hidden = Boolean(query && !text.includes(query));
      }
      updateStatus();
    });

    updateStatus();
  }

  const progress = document.querySelector("[data-read-progress]");
  const backTop = document.querySelector("[data-back-top]");
  const updateProgress = () => {
    const max = document.documentElement.scrollHeight - window.innerHeight;
    const value = max > 0 ? Math.min(1, Math.max(0, window.scrollY / max)) : 0;
    if (progress) progress.style.width = `${Math.round(value * 100)}%`;
    if (backTop) backTop.classList.toggle("visible", window.scrollY > 480);
  };

  updateProgress();
  window.addEventListener("scroll", updateProgress, { passive: true });
  window.addEventListener("resize", updateProgress);
  if (backTop) {
    backTop.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));
  }

  document.querySelectorAll(".chapter-content pre").forEach((pre) => {
    if (pre.parentElement && pre.parentElement.classList.contains("code-wrap")) return;

    const wrap = document.createElement("div");
    wrap.className = "code-wrap";
    pre.parentNode.insertBefore(wrap, pre);
    wrap.appendChild(pre);

    const copy = document.createElement("button");
    copy.className = "copy-code";
    copy.type = "button";
    copy.textContent = "复制";
    wrap.appendChild(copy);

    copy.addEventListener("click", async () => {
      const text = pre.textContent || "";
      try {
        await navigator.clipboard.writeText(text);
        copy.textContent = "已复制";
        copy.classList.add("copied");
        window.setTimeout(() => {
          copy.textContent = "复制";
          copy.classList.remove("copied");
        }, 1300);
      } catch {
        copy.textContent = "复制失败";
        window.setTimeout(() => {
          copy.textContent = "复制";
        }, 1300);
      }
    });
  });

  const lightbox = document.querySelector("[data-lightbox]");
  const lightboxImg = document.querySelector("[data-lightbox-img]");
  const lightboxCaption = document.querySelector("[data-lightbox-caption]");
  const lightboxClose = document.querySelector("[data-lightbox-close]");

  const closeLightbox = () => {
    if (!lightbox) return;
    lightbox.hidden = true;
    body.classList.remove("lightbox-open");
    if (lightboxImg) lightboxImg.removeAttribute("src");
  };

  document.querySelectorAll(".chapter-content figure img, .chapter-content > p img").forEach((img) => {
    img.addEventListener("click", () => {
      if (!lightbox || !lightboxImg) return;
      lightboxImg.src = img.currentSrc || img.src;
      lightboxImg.alt = img.alt || "";
      const caption = img.closest("figure")?.querySelector("figcaption")?.textContent || img.alt || "";
      if (lightboxCaption) lightboxCaption.textContent = caption;
      lightbox.hidden = false;
      body.classList.add("lightbox-open");
    });
  });

  if (lightboxClose) lightboxClose.addEventListener("click", closeLightbox);
  if (lightbox) {
    lightbox.addEventListener("click", (event) => {
      if (event.target === lightbox) closeLightbox();
    });
  }

  window.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeLightbox();
      closeNav();
    }
  });

  const links = Array.from(document.querySelectorAll(".toc-panel a"));
  const headings = links
    .map((link) => {
      const href = link.getAttribute("href") || "";
      if (!href.startsWith("#")) return null;
      return document.getElementById(decodeURIComponent(href.slice(1)));
    })
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
