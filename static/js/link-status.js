(function () {
  var script = document.getElementById("link-status-data");
  if (!script) return;
  var data;
  try { data = JSON.parse(script.textContent); } catch (e) { return; }

  var broken = data.broken || {};
  var replacement = data.replacement || {};

  var dialog = document.getElementById("broken-link-dialog");
  var urlEl = dialog ? document.getElementById("broken-link-url") : null;
  var archiveEl = dialog ? document.getElementById("broken-link-archive") : null;
  var closeBtn = dialog ? dialog.querySelector("[data-dialog-close]") : null;

  function variants(href) {
    var list = [href];
    var www = href.replace(/^https?:\/\/www\./i, "https://");
    if (www !== href) list.push(www);
    var noScheme = href.replace(/^https?:\/\//i, "");
    if (noScheme !== href) list.push(noScheme);
    return list;
  }

  function lookup(href) {
    var vs = variants(href);
    for (var i = 0; i < vs.length; i++) {
      if (Object.prototype.hasOwnProperty.call(broken, vs[i])) return { status: "broken", key: vs[i] };
      if (Object.prototype.hasOwnProperty.call(replacement, vs[i])) return { status: "replacement", key: vs[i] };
    }
    return null;
  }

  var containers = document.querySelectorAll(".post-content, .about-intro, .excerpt");
  if (!containers.length) return;

  Array.prototype.forEach.call(containers, function (content) {
  var links = content.querySelectorAll("a[href^='http']");
  Array.prototype.forEach.call(links, function (a) {
    var href = a.getAttribute("href");
    var hit = lookup(href);
    if (!hit) return;

    if (hit.status === "broken") {
      a.classList.add("is-broken");
      a.setAttribute("aria-label", (a.textContent || "Link") + " (die URL scheint nicht mehr verfügbar zu sein)");
      a.addEventListener("click", function (ev) {
        ev.preventDefault();
        if (!dialog) return;
        var target = a.getAttribute("href");
        urlEl.textContent = target;
        archiveEl.href = "https://web.archive.org/web/*/" + target;
        dialog.showModal();
      });
    } else if (hit.status === "replacement") {
      var rep = replacement[hit.key];
      if (rep) a.setAttribute("href", rep);
    }
  });
  });

  if (dialog) {
    dialog.addEventListener("click", function (ev) {
      if (ev.target === dialog) dialog.close();
    });
    if (closeBtn) closeBtn.addEventListener("click", function () { dialog.close(); });
  }
})();
