const state = {
  snapshot: null,
  depthMode: null,
  density: localStorage.getItem("nexus-density") || "comfortable",
  auth: {
    apiToken: null,
  },
};

const nodes = {
  log: document.getElementById("conversation-log"),
  quickActions: document.getElementById("quick-actions"),
  composerForm: document.getElementById("composer-form"),
  composerInput: document.getElementById("composer-input"),
  focusComposer: document.getElementById("focus-composer"),
  launchMission: document.getElementById("launch-mission"),
  approveNext: document.getElementById("approve-next"),
  runStatePill: document.getElementById("run-state-pill"),
  activeMissionPill: document.getElementById("active-mission-pill"),
  pendingPill: document.getElementById("pending-pill"),
  routeSignal: document.getElementById("route-signal"),
  modelSignal: document.getElementById("model-signal"),
  workspaceLabel: document.getElementById("workspace-label"),
  depthLayer: document.getElementById("depth-layer"),
  depthTitle: document.getElementById("depth-title"),
  depthIntro: document.getElementById("depth-intro"),
  depthBody: document.getElementById("depth-body"),
  closeDepth: document.getElementById("close-depth"),
  summonModels: document.getElementById("summon-models"),
  summonGovernance: document.getElementById("summon-governance"),
  summonProof: document.getElementById("summon-proof"),
  openTextual: document.getElementById("open-textual"),
  densityToggle: document.getElementById("density-toggle"),
};

function applyDensity() {
  const compact = state.density === "compact";
  document.body.classList.toggle("density-compact", compact);
  nodes.densityToggle.textContent = compact ? "Density: Compact" : "Density: Comfortable";
}

function toggleDensity() {
  state.density = state.density === "compact" ? "comfortable" : "compact";
  localStorage.setItem("nexus-density", state.density);
  applyDensity();
}

function bubble(role, text) {
  const div = document.createElement("div");
  div.className = `bubble ${role}`;
  div.textContent = text;
  return div;
}

function api(path, init = {}) {
  const headers = {
    "Content-Type": "application/json",
    ...(init.headers || {}),
  };
  if (state.auth.apiToken) {
    headers.Authorization = `Bearer ${state.auth.apiToken}`;
  }
  return fetch(path, {
    headers,
    ...init,
  }).then(async (res) => {
    const data = await res.json().catch(() => ({}));
    if (!res.ok || data.ok === false) {
      const reason = data.error || `http_${res.status}`;
      throw new Error(reason);
    }
    return data.data;
  });
}

function formatTurn(turn) {
  const route = turn.route || "conversation";
  const reason = turn.route_reason || "";
  const model = turn.model_trace || {};
  const routeSummary = `route=${route} reason=${reason}`;
  const modelSummary = model.invoked
    ? `model=${model.provider || "unknown"}/${model.model_id || ""} tier=${model.tier || ""} fallback=${Boolean(model.fallback)}`
    : `model=not-invoked`;
  return `${routeSummary}\n${modelSummary}`;
}

function extractSignals(snapshot) {
  const turns = (snapshot.conversation && snapshot.conversation.turns) || [];
  const latest = turns.length ? turns[turns.length - 1] : null;
  const trace = latest && latest.model_trace ? latest.model_trace : {};
  const route = latest ? `${latest.route || "chat"}:${latest.route_reason || ""}` : "waiting";
  const model = trace.invoked
    ? `${trace.provider || "unknown"}/${trace.tier || ""} fallback=${Boolean(trace.fallback)}`
    : "not_invoked";
  return { route, model, latest, trace };
}

function resumeSnapshot(snapshot) {
  return snapshot.resume_snapshot || {};
}

function resetQuickActions() {
  nodes.quickActions.innerHTML = "";
}

function quickAction(label, action) {
  const button = document.createElement("button");
  button.type = "button";
  button.className = "quick-action";
  button.textContent = label;
  button.addEventListener("click", action);
  nodes.quickActions.appendChild(button);
}

function autosizeComposer() {
  const node = nodes.composerInput;
  node.style.height = "auto";
  node.style.height = `${Math.min(node.scrollHeight, 240)}px`;
}

function renderConversation(snapshot) {
  nodes.log.innerHTML = "";
  const turns = (snapshot.conversation && snapshot.conversation.turns) || [];
  const resume = resumeSnapshot(snapshot);

  if (!turns.length) {
    const objective = resume.objective || "none";
    const nextStep = resume.next_step || "No active next step yet.";
    nodes.log.appendChild(
      bubble(
        "system",
        `Nexus is ready. Objective=${objective} | Runtime=${resume.runtime_status || "idle"} | Next=${nextStep}`
      )
    );
    return;
  }

  const truthLines = [
    `objective=${resume.objective || "none"}`,
    `runtime=${resume.runtime_status || "idle"}`,
    `next=${resume.next_step || "none"}`,
    `open_loops=${(resume.open_loops || []).length}`,
    `pending_approvals=${(resume.pending_approvals || []).length}`,
  ];
  nodes.log.appendChild(bubble("system", truthLines.join(" | ")));

  for (const turn of turns) {
    if (turn.user_text) {
      nodes.log.appendChild(bubble("user", turn.user_text));
    }
    nodes.log.appendChild(bubble("nexus", turn.goal || ""));
    nodes.log.appendChild(bubble("system", formatTurn(turn)));
  }
  nodes.log.scrollTop = nodes.log.scrollHeight;
}

function addDepthCard(title, lines) {
  const card = document.createElement("section");
  card.className = "depth-card";
  const h3 = document.createElement("h3");
  h3.textContent = title;
  card.appendChild(h3);

  for (const line of lines) {
    const p = document.createElement("p");
    p.textContent = line;
    card.appendChild(p);
  }
  nodes.depthBody.appendChild(card);
}

function renderDepth(mode, snapshot) {
  nodes.depthBody.innerHTML = "";
  nodes.depthIntro.textContent = "";
  const resume = resumeSnapshot(snapshot);

  if (mode === "models") {
    nodes.depthTitle.textContent = "Models Depth";
    nodes.depthIntro.textContent = "Live provider and fallback truth from the current runtime.";
    const telemetry = snapshot.models && snapshot.models.telemetry ? snapshot.models.telemetry : {};
    const recent = telemetry.recent_activity || [];
    addDepthCard("Runtime Truth", [
      `gateway_online=${Boolean(snapshot.models && snapshot.models.stack && snapshot.models.stack.gateway_online)}`,
      `model_invocations=${telemetry.model_invocations || 0}`,
      `fallbacks=${telemetry.fallbacks || 0}`,
      `success_rate=${telemetry.success_rate || 0}`,
    ]);
    recent.slice(-8).reverse().forEach((activity, idx) => {
      addDepthCard(`Activity ${idx + 1}`, [
        `provider=${activity.provider}`,
        `model=${activity.model_id}`,
        `tier=${activity.tier} routed=${activity.routed_tier}`,
        `fallback=${Boolean(activity.fallback)} reason=${activity.fallback_reason || ""}`,
        `latency_ms=${activity.latency_ms}`,
      ]);
    });
    return;
  }

  if (mode === "governance") {
    nodes.depthTitle.textContent = "Governance Depth";
    nodes.depthIntro.textContent = "Authority and safeguards appear only when needed.";
    const cards = (snapshot.operator_surface && snapshot.operator_surface.governance_cards) || [];
    addDepthCard("Pending Authority", [
      `pending=${(resume.pending_approvals || []).length}`,
      `runtime_status=${resume.runtime_status || "idle"}`,
      `open_loops=${(resume.open_loops || []).length}`,
    ]);
    (resume.pending_approvals || []).slice(0, 10).forEach((item, idx) => {
      addDepthCard(`Approval ${idx + 1}`, [
        `approval_id=${item.approval_id}`,
        `mission_id=${item.mission_id}`,
        `objective=${item.objective}`,
        `status=${item.status}`,
      ]);
    });
    cards.slice(0, 20).forEach((line, idx) => {
      addDepthCard(`Governance ${idx + 1}`, [line]);
    });
    return;
  }

  nodes.depthTitle.textContent = "Proof Depth";
  nodes.depthIntro.textContent = "Execution receipts, memory influence, and artifacts for the current runtime.";
  const proofs = (snapshot.operator_surface && snapshot.operator_surface.proof_ids) || [];
  const artifacts = snapshot.artifacts_recent || [];
  const execution = resume.execution_summary || {};
  const influence = resume.memory_influence || { matches: [] };
  addDepthCard("Execution Truth", [
    `run_id=${execution.run_id || "none"}`,
    `status=${execution.status || resume.runtime_status || "idle"}`,
    `step_count=${execution.step_count || 0}`,
    `attempt_count=${execution.attempt_count || 0}`,
    `latest_phase=${execution.latest_step ? execution.latest_step.phase : "none"}`,
  ]);
  addDepthCard("Memory Influence", [
    `query=${influence.query || ""}`,
    `match_count=${(influence.matches || []).length}`,
  ]);
  (influence.matches || []).slice(0, 5).forEach((item, idx) => {
    addDepthCard(`Memory Match ${idx + 1}`, [
      `key=${item.key}`,
      `stratum=${item.stratum}`,
      `score=${item.score}`,
      `reasons=${(item.reasons || []).join(",")}`,
    ]);
  });
  addDepthCard("Proof Inventory", [`proof_ids=${proofs.length}`, `recent_artifacts=${artifacts.length}`]);
  artifacts.slice(-10).reverse().forEach((artifact, idx) => {
    addDepthCard(`Artifact ${idx + 1}`, [
      `id=${artifact.id}`,
      `mission_id=${artifact.mission_id}`,
      `type=${artifact.type || ""}`,
    ]);
  });
}

function setDepth(mode) {
  state.depthMode = mode;
  if (!mode) {
    nodes.depthLayer.classList.add("hidden");
    return;
  }
  if (state.snapshot) {
    renderDepth(mode, state.snapshot);
  }
  nodes.depthLayer.classList.remove("hidden");
}

async function refresh() {
  const snapshot = await api("/api/state");
  state.snapshot = snapshot;
  const ws = snapshot.workspace || {};
  const resume = resumeSnapshot(snapshot);
  const pending = resume.pending_approvals || [];
  const signals = extractSignals(snapshot);

  nodes.workspaceLabel.textContent = ws.workspace_id || "workspace:main";
  nodes.runStatePill.textContent = resume.runtime_status || ws.run_state || "idle";
  nodes.pendingPill.textContent = `pending approvals: ${pending.length}`;
  nodes.activeMissionPill.textContent = resume.active
    ? `mission: ${resume.mission_id} (${resume.status || resume.runtime_status || "active"})`
    : "mission: none";
  nodes.routeSignal.textContent = `route signal: ${signals.route || "waiting"}`;
  nodes.modelSignal.textContent = `next step: ${resume.next_step || "waiting"}`;
  nodes.approveNext.classList.toggle("hidden", pending.length === 0);

  renderConversation(snapshot);
  resetQuickActions();

  if (pending.length > 0) {
    quickAction("Resolve Pending Approval", approveNext);
  }

  if (resume.active && resume.status === "paused") {
    quickAction("Resume Active Mission", () => sendConversation("resume mission"));
  }

  if (!resume.active && signals.latest && signals.latest.route === "chat") {
    quickAction("Launch Last Intent As Mission", () => {
      const draft = (signals.latest.user_text || "").trim();
      if (!draft) {
        return;
      }
      nodes.composerInput.value = draft;
      autosizeComposer();
      launchMissionFromComposer();
    });
  }

  if ((resume.relevant_memory || []).length > 0) {
    quickAction("Inspect Memory Influence", () => setDepth("proof"));
  }

  if (resume.execution_summary && (resume.execution_summary.step_count || 0) > 0) {
    quickAction("Inspect Execution Truth", () => setDepth("proof"));
  }

  if (signals.trace && signals.trace.fallback) {
    quickAction("Inspect Model Fallback", () => setDepth("models"));
  }

  if (pending.length > 0 || ((snapshot.operator_surface && snapshot.operator_surface.governance_cards) || []).length > 0) {
    quickAction("Inspect Governance", () => setDepth("governance"));
  }

  if (state.depthMode) {
    renderDepth(state.depthMode, snapshot);
  }
}

async function sendConversation(text) {
  const trimmed = text.trim();
  if (!trimmed) {
    return;
  }
  await api("/api/conversation", {
    method: "POST",
    body: JSON.stringify({ text: trimmed }),
  });
  nodes.composerInput.value = "";
  await refresh();
}

async function approveNext() {
  await api("/api/approve", {
    method: "POST",
    body: JSON.stringify({}),
  });
  await refresh();
}

async function launchMissionFromComposer() {
  const objective = nodes.composerInput.value.trim();
  if (!objective) {
    return;
  }
  await api("/api/mission", {
    method: "POST",
    body: JSON.stringify({ objective }),
  });
  nodes.composerInput.value = "";
  await refresh();
}

nodes.composerForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    await sendConversation(nodes.composerInput.value);
  } catch (error) {
    nodes.log.appendChild(bubble("system", `send failed: ${String(error.message || error)}`));
  }
});

nodes.composerInput.addEventListener("input", () => {
  autosizeComposer();
});

nodes.composerInput.addEventListener("keydown", async (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    try {
      await sendConversation(nodes.composerInput.value);
    } catch (error) {
      nodes.log.appendChild(bubble("system", `send failed: ${String(error.message || error)}`));
    }
  }
});

nodes.launchMission.addEventListener("click", async () => {
  try {
    await launchMissionFromComposer();
  } catch (error) {
    nodes.log.appendChild(bubble("system", `mission launch failed: ${String(error.message || error)}`));
  }
});

nodes.approveNext.addEventListener("click", async () => {
  try {
    await approveNext();
  } catch (error) {
    nodes.log.appendChild(bubble("system", `approval failed: ${String(error.message || error)}`));
  }
});

nodes.summonModels.addEventListener("click", () => setDepth("models"));
nodes.summonGovernance.addEventListener("click", () => setDepth("governance"));
nodes.summonProof.addEventListener("click", () => setDepth("proof"));
nodes.closeDepth.addEventListener("click", () => setDepth(null));
nodes.focusComposer.addEventListener("click", () => {
  nodes.composerInput.focus();
});
nodes.densityToggle.addEventListener("click", toggleDensity);

nodes.openTextual.addEventListener("click", async () => {
  if (window.nexusDesktop && window.nexusDesktop.openTextualFallback) {
    await window.nexusDesktop.openTextualFallback();
  }
});

window.addEventListener("keydown", (event) => {
  if (event.key === "/" && document.activeElement !== nodes.composerInput) {
    event.preventDefault();
    nodes.composerInput.focus();
  }
  if (event.key === "Escape" && !nodes.depthLayer.classList.contains("hidden")) {
    setDepth(null);
  }
});

applyDensity();
autosizeComposer();

async function boot() {
  try {
    const info = await Promise.resolve(window.nexusDesktop && window.nexusDesktop.appInfo ? window.nexusDesktop.appInfo() : null);
    if (info && info.apiToken) {
      state.auth.apiToken = info.apiToken;
    }
    await refresh();
  } catch (error) {
    nodes.log.appendChild(bubble("system", `boot failed: ${String(error.message || error)}`));
  }
}

boot();

setInterval(() => {
  refresh().catch(() => {});
}, 2500);