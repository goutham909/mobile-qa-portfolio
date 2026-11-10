const ARTIFACTS = [
  { title: "Test plan", path: "test_artifacts/test_plan.md", text: "Scope, approach, device matrix, entry/exit criteria, risks and traceability." },
  { title: "Sample bug reports", path: "test_artifacts/sample_bug_reports.md", text: "Severity, environment, numbered steps, expected vs actual, evidence." },
  { title: "Interrupt testing (BDD)", path: "test_artifacts/bdd_features/interrupt_testing.feature", text: "Calls, SMS, backgrounding, process death, rotation, low battery." },
  { title: "Network throttling (BDD)", path: "test_artifacts/bdd_features/network_throttling.feature", text: "Offline, 2G/3G, handoffs, latency, timeouts and double-submit protection." },
  { title: "Page objects", path: "pages", text: "Accessibility-first locators and fluent screen APIs." },
  { title: "CI pipeline", path: ".github/workflows/mobile_tests.yml", text: "Lint, emulator smoke, nightly regression and Sauce Labs runs." },
];

const FILTER_LABELS = {
  all: "All",
  client: "Client QA",
  clone: "App clones",
  build: "Builds",
};

const el = (tag, className, text) => {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
};

const fill = (id, items, render) => {
  const root = document.getElementById(id);
  if (!root) return;
  root.replaceChildren(...items.map(render));
};

const externalLink = (href, className, label) => {
  const a = el("a", className, label);
  a.href = href;
  if (href.startsWith("http")) {
    a.target = "_blank";
    a.rel = "noopener";
  }
  return a;
};

function renderWorkCard(project) {
  const card = el("article", `work-card${project.featured ? " is-featured" : ""}`);
  card.dataset.category = project.category;
  card.tabIndex = 0;

  const badge = el("span", "work-badge", project.badge || FILTER_LABELS[project.category] || project.category);
  const title = el("h3", "", project.title);
  const summary = el("p", "", project.summary || project.description || "");

  const tags = el("ul", "work-tags");
  (project.tags || []).forEach((tag) => tags.append(el("li", "", tag)));

  const actions = el("div", "work-actions");
  (project.links || []).forEach((link) => {
    actions.append(
      externalLink(link.url, `btn btn-sm${link.primary ? "" : " btn-ghost"}`, link.label)
    );
  });

  card.append(badge, title, summary, tags, actions);

  const primary = (project.links || []).find((link) => link.primary) || (project.links || [])[0];
  if (primary) {
    card.addEventListener("click", (event) => {
      if (event.target.closest("a")) return;
      if (primary.url.startsWith("#")) {
        location.hash = primary.url;
        return;
      }
      window.open(primary.url, "_blank", "noopener");
    });
    card.addEventListener("keydown", (event) => {
      if (event.key !== "Enter" && event.key !== " ") return;
      event.preventDefault();
      card.click();
    });
  }
  return card;
}

function setupWork(projects) {
  const grid = document.getElementById("work-grid");
  const empty = document.getElementById("work-empty");
  const filters = document.getElementById("work-filters");
  if (!grid || !filters) return;

  let active = "all";

  const paint = () => {
    const visible = projects.filter((p) => active === "all" || p.category === active);
    grid.replaceChildren(...visible.map(renderWorkCard));
    if (empty) empty.hidden = visible.length > 0;

    filters.querySelectorAll(".filter").forEach((btn) => {
      const on = btn.dataset.filter === active;
      btn.classList.toggle("is-active", on);
      btn.setAttribute("aria-selected", on ? "true" : "false");
    });
  };

  filters.addEventListener("click", (event) => {
    const btn = event.target.closest(".filter");
    if (!btn) return;
    active = btn.dataset.filter;
    paint();
  });

  paint();
}

function render(p) {
  document.querySelectorAll("[data-bind]").forEach((node) => {
    const value = p[node.dataset.bind];
    if (value) node.textContent = value;
  });
  document.querySelectorAll("[data-link]").forEach((node) => {
    const url = p.links?.[node.dataset.link];
    if (url) node.href = url;
  });

  fill("stats", p.stats || [], (s) => {
    const li = el("li", "stat");
    li.append(el("strong", "", s.value), el("span", "", s.label));
    return li;
  });

  fill("about-text", p.about || [], (para) => el("p", "", para));

  fill("capability-list", p.capabilities || [], (c, i) => {
    const item = el("li", "deliver-item");
    item.append(
      el("span", "idx", String(i + 1).padStart(2, "0")),
      (() => {
        const body = el("div");
        body.append(el("h3", "", c.title), el("p", "", c.description));
        return body;
      })()
    );
    return item;
  });

  fill("experience-list", p.experience || [], (job) => {
    const li = el("li", "job");
    const head = el("div", "job-head");
    const company = job.companyUrl ? el("a", "company", job.company) : el("span", "company", job.company);
    if (job.companyUrl) {
      company.href = job.companyUrl;
      company.target = "_blank";
      company.rel = "noopener";
    }
    head.append(el("h3", "", job.role), el("span", "period", job.period));
    li.append(head, company);
    if (job.bullets?.length) {
      const ul = el("ul", "checks");
      job.bullets.forEach((b) => ul.append(el("li", "", b)));
      li.append(ul);
    }
    return li;
  });

  const edu = document.getElementById("education");
  if (edu && p.education) {
    edu.replaceChildren(
      el("span", "label", "Education"),
      el("strong", "", p.education.degree),
      el("span", "period", p.education.period)
    );
  }

  fill("testimonial-list", p.testimonials || [], (t) => {
    const fig = el("figure", "quote");
    const cap = el("figcaption");
    cap.append(el("strong", "", t.author), el("span", "", t.context));
    fig.append(el("div", "stars", "★★★★★"), el("blockquote", "", `“${t.quote}”`), cap);
    return fig;
  });

  setupWork(p.projects || []);

  fill("blog-list", p.blogs || [], (post) => {
    const card = el("a", "blog-card");
    card.href = post.url;
    card.target = "_blank";
    card.rel = "noopener";
    card.append(
      el("span", "blog-outlet", post.outlet || "Article"),
      el("h3", "", post.title),
      el("p", "", post.summary || ""),
      el("span", "blog-cta", "Read article →")
    );
    return card;
  });

  fill("tool-list", p.tools || [], (t) => el("li", "", t));

  const repo = (p.repoUrl || "").replace(/\/$/, "");
  fill("artifact-list", ARTIFACTS, (a) => {
    const card = el(repo ? "a" : "article", "artifact");
    if (repo) {
      card.href = `${repo}/${a.path.includes(".") ? "blob" : "tree"}/main/${a.path}`;
      card.target = "_blank";
      card.rel = "noopener";
    }
    card.append(el("h3", "", a.title), el("p", "", a.text), el("code", "path", a.path));
    return card;
  });

  const badge = document.getElementById("ci-badge");
  if (badge && repo) {
    const link = el("a");
    link.href = `${repo}/actions/workflows/mobile_tests.yml`;
    link.target = "_blank";
    link.rel = "noopener";
    const img = el("img");
    img.src = `${repo}/actions/workflows/mobile_tests.yml/badge.svg`;
    img.alt = "Mobile Tests CI status";
    const source = el("a", "btn btn-ghost btn-sm", "View source on GitHub");
    source.href = repo;
    source.target = "_blank";
    source.rel = "noopener";
    link.append(img);
    badge.replaceChildren(link, source);
  }
}

document.getElementById("year").textContent = new Date().getFullYear();

fetch("profile.json", { cache: "no-cache" })
  .then((res) => (res.ok ? res.json() : Promise.reject(res.status)))
  .then(render)
  .catch((err) => console.error("Could not load profile.json", err));
