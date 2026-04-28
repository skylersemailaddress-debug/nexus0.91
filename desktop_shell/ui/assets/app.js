const nodes = {
  heroTitle: document.getElementById("hero-title"),
  heroSubtitle: document.getElementById("hero-subtitle"),
  heroMeta: document.getElementById("hero-meta"),
  summaryText: document.getElementById("summary-text"),
  changesList: document.getElementById("changes-list"),
  qualityGates: document.getElementById("quality-gates"),
  commitsList: document.getElementById("commits-list"),
  filesHeading: document.getElementById("files-heading"),
  filesTotals: document.getElementById("files-totals"),
  filesList: document.getElementById("files-list"),
  testResults: document.getElementById("test-results"),
  validatorResults: document.getElementById("validator-results"),
  nextSteps: document.getElementById("next-steps"),
  repoDetails: document.getElementById("repo-details"),
  commitsHeading: document.getElementById("commits-heading"),
};

function api(path) {
  return fetch(path)
    .then((res) => res.json())
    .then((payload) => {
      if (!payload.ok) {
        throw new Error(payload.error || `request_failed:${path}`);
      }
      return payload.data;
    });
}

function metaChip(label, value) {
  const div = document.createElement("div");
  div.className = "meta-chip";
  div.innerHTML = `<label>${label}</label><span>${value || "n/a"}</span>`;
  return div;
}

function setText(el, text) {
  el.textContent = text;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function renderRepo(data) {
  const success = data.clean_worktree && !data.behind_remote;
  setText(nodes.heroTitle, success ? "Repository updated successfully" : "Repository requires attention");
  setText(
    nodes.heroSubtitle,
    data.clean_worktree
      ? "All changes committed, tested, and validated"
      : "Uncommitted or unsynced changes detected in working tree."
  );

  nodes.heroMeta.innerHTML = "";
  nodes.heroMeta.append(
    metaChip("Branch", data.branch),
    metaChip("Commit", (data.head_commit || "").slice(0, 7)),
    metaChip("Author", data.head_author),
    metaChip("Date", data.head_date)
  );

  setText(nodes.summaryText, data.head_summary || "No commit summary available.");

  nodes.changesList.innerHTML = "";
  const changes = data.change_highlights.length ? data.change_highlights : ["No changed files found."];
  changes.forEach((line) => {
    const li = document.createElement("li");
    li.textContent = line;
    nodes.changesList.appendChild(li);
  });

  nodes.qualityGates.innerHTML = "";
  data.quality_gates.forEach((gate) => {
    const div = document.createElement("div");
    div.className = "gate";
    div.innerHTML = `<div>${gate.name}</div><strong>${gate.status}</strong>`;
    nodes.qualityGates.appendChild(div);
  });

  nodes.commitsList.innerHTML = "";
  nodes.commitsHeading.textContent = `Commits (${data.commits.length})`;
  data.commits.forEach((commit) => {
    const row = document.createElement("div");
    row.className = "commit-row";
    row.innerHTML = `
      <span class="commit-hash">${commit.sha.slice(0, 7)}</span>
      <span>${commit.subject}</span>
      <span>${commit.author}</span>
      <span>${commit.time_short}</span>
    `;
    nodes.commitsList.appendChild(row);
  });

  nodes.filesHeading.textContent = `Files changed (${data.files_changed.length})`;
  nodes.filesTotals.innerHTML = `<span class="add">+${data.total_additions}</span> <span class="del">−${data.total_deletions}</span>`;
  nodes.filesList.innerHTML = "";
  data.files_changed.forEach((file) => {
    const row = document.createElement("div");
    row.className = "file-row";
    row.innerHTML = `
      <span>${file.path}</span>
      <span class="add">+${file.additions}</span>
      <span class="del">−${file.deletions}</span>
    `;
    nodes.filesList.appendChild(row);
  });

  nodes.repoDetails.innerHTML = "";
  const details = [
    `Remote: ${data.remote_url || "(not configured)"}`,
    `Branch: ${data.branch}`,
    `Commit: ${(data.head_commit || "").slice(0, 7)}`,
    `Pushed ${data.head_date}`,
  ];
  details.forEach((line) => {
    const p = document.createElement("p");
    p.textContent = line;
    nodes.repoDetails.appendChild(p);
  });
  const status = document.createElement("span");
  status.className = "repo-status";
  status.textContent = data.clean_worktree ? "Up to date" : "Changes pending";
  nodes.repoDetails.appendChild(status);
}

function renderCI(data) {
  const testPassCount = data.tests.filter((item) => item.pass).length;
  nodes.testResults.innerHTML = `
    <div class="result-summary">
      <div class="result-check">✓</div>
      <div>
        <p class="result-title">${testPassCount === data.tests.length ? "All tests passed" : "Some tests failed"}</p>
        <p class="result-subtitle">${testPassCount} passed, ${data.tests.length - testPassCount} failed</p>
      </div>
    </div>
  `;
  data.tests.forEach((test) => {
    const row = document.createElement("div");
    row.className = "status-line";
    row.innerHTML = `<span>${escapeHtml(test.name)}</span><span class="${test.pass ? "add" : "del"}">${test.pass ? "passed" : "failed"}</span>`;
    nodes.testResults.appendChild(row);
  });

  const validatorPassCount = data.validators.filter((item) => item.pass).length;
  nodes.validatorResults.innerHTML = `
    <div class="result-summary">
      <div class="result-check">✓</div>
      <div>
        <p class="result-title">${validatorPassCount === data.validators.length ? "validate:all passed" : "validator errors detected"}</p>
        <p class="result-subtitle">${validatorPassCount} validators passed</p>
      </div>
    </div>
  `;
  data.validators.forEach((item) => {
    const row = document.createElement("div");
    row.className = "status-line";
    row.innerHTML = `<span>${escapeHtml(item.name)}</span><span class="${item.pass ? "add" : "del"}">${item.pass ? "passed" : "failed"}</span>`;
    nodes.validatorResults.appendChild(row);
  });
}

function renderNextSteps(stateData) {
  const steps = [
    { title: "Plan", body: stateData.resume_snapshot?.objective || "Define objective" },
    { title: "Approve", body: `${(stateData.resume_snapshot?.pending_approvals || []).length} pending approvals` },
    { title: "Execute", body: stateData.resume_snapshot?.runtime_status || "idle" },
    { title: "Validate", body: stateData.resume_snapshot?.next_step || "Run quality gates" },
    { title: "Deploy", body: stateData.signal || "Awaiting signal" },
  ];

  nodes.nextSteps.innerHTML = "";
  steps.forEach((step, index) => {
    const div = document.createElement("div");
    div.className = "step";
    div.innerHTML = `<h4>${step.title}</h4><p>${step.body}</p>`;
    nodes.nextSteps.appendChild(div);
    if (index < steps.length - 1) {
      const arrow = document.createElement("div");
      arrow.className = "step-arrow";
      arrow.textContent = "→";
      nodes.nextSteps.appendChild(arrow);
    }
  });
}

Promise.all([api("/api/local-repo-dashboard"), api("/api/hybrid-ci"), api("/api/state")])
  .then(([repoData, ciData, stateData]) => {
    renderRepo(repoData);
    renderCI(ciData);
    renderNextSteps(stateData);
  })
  .catch((error) => {
    setText(nodes.heroTitle, "Dashboard failed to load");
    setText(nodes.heroSubtitle, error.message);
  });
