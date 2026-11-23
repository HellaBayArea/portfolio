(function () {
  var nav = document.querySelector(".nav");
  if (nav) {
    var items = Array.prototype.slice.call(nav.querySelectorAll("details.nav-item"));
    var box = document.getElementById("nav-check");
    var fine = window.matchMedia("(hover: hover) and (pointer: fine)");
    var wide = window.matchMedia("(min-width: 861px)");

    function closeItems(except) {
      items.forEach(function (item) {
        if (item !== except) item.open = false;
      });
    }

    items.forEach(function (item) {
      var summary = item.querySelector("summary");
      item.addEventListener("toggle", function () {
        if (item.open) closeItems(item);
      });
      if (summary) {
        summary.addEventListener("click", function (e) {
          if (fine.matches && wide.matches && e.pointerType === "mouse" && item.open) e.preventDefault();
        });
      }
      item.addEventListener("mouseenter", function () {
        if (!fine.matches || !wide.matches) return;
        item.open = true;
      });
      item.addEventListener("mouseleave", function () {
        if (!fine.matches || !wide.matches) return;
        if (item.contains(document.activeElement)) return;
        item.open = false;
      });
    });

    document.addEventListener("click", function (e) {
      if (!nav.contains(e.target)) closeItems(null);
    });

    document.addEventListener("keydown", function (e) {
      if (e.key !== "Escape") return;
      closeItems(null);
      if (box && box.checked) {
        box.checked = false;
        box.dispatchEvent(new Event("change"));
      }
    });

    if (box) {
      box.addEventListener("change", function () {
        document.body.classList.toggle("nav-open", box.checked);
        if (!box.checked) closeItems(null);
      });
    }

    wide.addEventListener("change", function (e) {
      if (!e.matches && box) return;
      if (e.matches && box) {
        box.checked = false;
        document.body.classList.remove("nav-open");
      }
    });
  }

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)");
  var hero = document.getElementById("hero-video");
  if (hero) {
    function syncHero() {
      if (reduce.matches) {
        hero.pause();
        hero.autoplay = false;
        hero.removeAttribute("autoplay");
        hero.classList.remove("is-playing");
      } else {
        var pending = hero.play();
        if (pending && pending.then) {
          pending.then(function () { hero.classList.add("is-playing"); }).catch(function () {});
        }
      }
    }
    hero.addEventListener("playing", function () { hero.classList.add("is-playing"); });
    reduce.addEventListener("change", syncHero);
    syncHero();
  }

  document.addEventListener("play", function (e) {
    if (!e.target || e.target.id === "hero-video") return;
    document.querySelectorAll("video").forEach(function (v) {
      if (v !== e.target && v.id !== "hero-video") v.pause();
    });
  }, true);

  var posterObserver = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (!en.isIntersecting) return;
      var v = en.target;
      if (v.dataset.poster) v.poster = v.dataset.poster;
      posterObserver.unobserve(v);
    });
  }, { rootMargin: "400px 0px" });

  var revealObserver = null;
  if (!reduce.matches && "IntersectionObserver" in window) {
    revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add("in");
        revealObserver.unobserve(en.target);
      });
    }, { threshold: 0.12 });
  }

  window.studioRefresh = function (root) {
    var scope = root || document;
    scope.querySelectorAll("video[data-poster]").forEach(function (v) { posterObserver.observe(v); });
    scope.querySelectorAll(".reveal").forEach(function (el) {
      if (reduce.matches || !revealObserver) el.classList.add("in");
      else revealObserver.observe(el);
    });
  };

  window.studioRefresh(document);

  var mvCount = document.getElementById("mv-count");
  if (mvCount) {
    mvCount.textContent = document.querySelectorAll(".mv:not([data-pending])").length + " videos";
  }
})();
