(function () {
  var fine = window.matchMedia("(hover: hover) and (pointer: fine)");
  var drops = document.querySelectorAll(".drop");

  drops.forEach(function (drop) {
    var summary = drop.querySelector("summary");
    if (!summary) return;
    drop.addEventListener("toggle", function () {
      if (!drop.open) return;
      drops.forEach(function (other) {
        if (other !== drop) other.open = false;
      });
    });
    if (fine.matches) {
      var timer;
      drop.addEventListener("mouseenter", function () {
        clearTimeout(timer);
        drop.open = true;
      });
      drop.addEventListener("mouseleave", function () {
        timer = setTimeout(function () { drop.open = false; }, 160);
      });
    }
  });

  document.addEventListener("click", function (e) {
    if (!e.target.closest(".drop")) {
      drops.forEach(function (drop) { drop.open = false; });
    }
  });

  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    drops.forEach(function (drop) { drop.open = false; });
    var box = document.getElementById("nav-check");
    if (box) box.checked = false;
  });

  document.querySelectorAll(".nav-links a").forEach(function (link) {
    link.addEventListener("click", function () {
      var box = document.getElementById("nav-check");
      if (box) box.checked = false;
    });
  });

  var legacy = {
    art: "art.html",
    music: "music.html",
    videos: "music-videos.html",
    akari: "akari/",
    about: "about.html",
    contact: "index.html#connect",
    "coming-soon": "akari/",
    "akari-stories": "akari/stories/"
  };
  var hash = location.hash.replace(/^#/, "");
  var root = document.body.getAttribute("data-root") || "";
  if (hash && legacy[hash] && !document.getElementById(hash)) {
    var dest = legacy[hash];
    if (dest.charAt(0) !== "#" && dest.indexOf("index.html") !== 0) dest = root + dest;
    else if (dest.indexOf("index.html") === 0) dest = root + dest;
    location.replace(dest);
  }

  var hero = document.getElementById("hero-video");
  if (hero) {
    var motion = window.matchMedia("(prefers-reduced-motion: reduce)");
    var sync = function () {
      if (motion.matches) {
        hero.pause();
        hero.removeAttribute("autoplay");
      } else {
        hero.muted = true;
        hero.setAttribute("autoplay", "");
        var play = hero.play();
        if (play && play.catch) play.catch(function () {});
      }
    };
    sync();
    if (motion.addEventListener) motion.addEventListener("change", sync);
  }

  var layout = document.querySelector(".hero-layout");
  if (layout) {
    var svg = layout.querySelector(".leaders");
    var portrait = layout.querySelector(".portrait");
    var narrow = window.matchMedia("(max-width: 860px)");
    var draw = function () {
      if (!svg || !portrait) return;
      while (svg.firstChild) svg.removeChild(svg.firstChild);
      if (narrow.matches) return;
      var lb = layout.getBoundingClientRect();
      if (!lb.width || !lb.height) return;
      svg.setAttribute("viewBox", "0 0 " + lb.width + " " + lb.height);
      var p = portrait.getBoundingClientRect();
      var cx = (p.left - lb.left) + p.width * parseFloat(portrait.getAttribute("data-face-cx") || "0.52");
      var cy = (p.top - lb.top) + p.height * parseFloat(portrait.getAttribute("data-face-cy") || "0.33");
      var rx = p.width * parseFloat(portrait.getAttribute("data-face-rx") || "0.28");
      var ry = p.height * parseFloat(portrait.getAttribute("data-face-ry") || "0.15");
      var ns = "http://www.w3.org/2000/svg";
      layout.querySelectorAll(".callout-dot").forEach(function (dot) {
        var d = dot.getBoundingClientRect();
        var x = d.left - lb.left + d.width / 2;
        var y = d.top - lb.top + d.height / 2;
        var ang = Math.atan2(y - cy, x - cx);
        var ex = cx + rx * Math.cos(ang);
        var ey = cy + ry * Math.sin(ang);
        var line = document.createElementNS(ns, "line");
        line.setAttribute("x1", x);
        line.setAttribute("y1", y);
        line.setAttribute("x2", ex);
        line.setAttribute("y2", ey);
        line.setAttribute("stroke", "rgba(215,246,255,0.9)");
        line.setAttribute("stroke-width", "1");
        svg.appendChild(line);
        var c = document.createElementNS(ns, "circle");
        c.setAttribute("cx", ex);
        c.setAttribute("cy", ey);
        c.setAttribute("r", "2.4");
        c.setAttribute("fill", "#d7f6ff");
        svg.appendChild(c);
      });
    };
    draw();
    window.addEventListener("resize", draw);
    if (narrow.addEventListener) narrow.addEventListener("change", draw);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(draw);
    if (window.ResizeObserver) new ResizeObserver(draw).observe(layout);
  }

  var videos = document.querySelectorAll("video[data-poster]");
  if (videos.length && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var v = entry.target;
        if (!v.getAttribute("poster")) v.poster = v.getAttribute("data-poster");
        io.unobserve(v);
      });
    }, { rootMargin: "400px 0px" });
    videos.forEach(function (v) { io.observe(v); });
  } else {
    videos.forEach(function (v) { v.poster = v.getAttribute("data-poster"); });
  }

  document.addEventListener("play", function (e) {
    if (!e.target || e.target.tagName !== "VIDEO") return;
    document.querySelectorAll("video").forEach(function (v) {
      if (v !== e.target) v.pause();
    });
  }, true);

  var dlg = document.getElementById("lightbox");
  if (dlg) {
    var img = dlg.querySelector("img");
    var cap = dlg.querySelector("figcaption");
    document.querySelectorAll("[data-lightbox]").forEach(function (a) {
      a.addEventListener("click", function (e) {
        e.preventDefault();
        img.src = a.href;
        img.alt = a.getAttribute("data-alt") || "";
        cap.textContent = a.getAttribute("data-caption") || "";
        dlg.showModal();
      });
    });
    dlg.addEventListener("click", function (e) {
      if (e.target === dlg) dlg.close();
    });
  }
})();
