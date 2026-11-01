const TITLES = {
  meta: "这次是谁在做",
  task_start: "接到一件事",
  model_turn: "它开口",
  tool: "它动手了",
  check: "有没有做对",
  absorb: "写进去划不划算",
  ledger: "要不要写进脑子",
  write: "这次写了没有",
  sleep: "晚上整理",
  morning: "早上的记录",
  gate: "考试",
  confirm: "先问你",
  status: "正在准备",
  done: "这一轮结束",
  error: "出错了",
  share: "交给另一台",
  carry: "换了一具基座",
  relabel: "改了个标签",
};

const DEST = {
  fast: "先记住",
  retrieval: "先不写进脑子",
  slot: "写成一项技能",
  local: "只留给这家",
  core: "变成通用本事",
  drop: "丢掉",
};

const FAMILY_NAME = {
  table: "表格",
  file: "文件",
  report: "报告",
  shell: "命令",
  http: "本机接口",
  mixed: "连着做几步",
};

const TOOL_NAME = {
  python: "跑了一小段程序",
  shell: "跑了一条允许的命令",
  read_file: "读了一个文件",
  write_file: "写了一个文件",
  list_dir: "看了看文件夹",
  http: "访问了本机接口",
  finish: "停下，等着检查",
};

const GATE_LINE = {
  gate1: "连续学习和倒班对照还没拿出胜负。",
  gate2: "办公世界双节律已通过闸门：dual 赢过 agent，区间在 0 以上。",
  gate3: "封存行业包迁移已通过：transfer 增益区间在 0 以上。",
};

const WHY = {
  "still cheaper to reread": "再读提示更便宜，所以先不写",
  "one success stays in the fast state": "只做对一次，先记住就好",
  "sorter dropped the trace": "这条不该留下",
  "gates agree on slot": "可以写成一项技能",
  "gates agree on local": "只留给这家",
  "gates agree on core": "可以变成通用本事",
  "night batch": "这一段结束时一起写",
  shift_end: "一段工作结束了",
  budget: "白天的额度用完了",
  drift: "环境变了",
  idle: "空下来了",
  practice: "做对就写",
  human: "你撤回了这一条",
};

const TOUR = [
  {
    type: "tool",
    title: "它动手了",
    text: "它不是只聊天。它会读文件、写结果、跑允许的命令。能不能做，不由它自己说了算。",
  },
  {
    type: "check",
    title: "有没有做对",
    text: "做完要看文件夹最后变成什么样。做对和做错走同一条时间线，不会藏起来。",
  },
  {
    type: "ledger",
    title: "要不要写进脑子",
    text: "做对一次只是记住。反复做对，才考虑写进去。这家的字段名不会变成谁都能用的本事。",
  },
  {
    type: "absorb",
    title: "写进去划不划算",
    text: "如果下次再看提示更便宜，这次就不写。划算了，才写进脑子。",
  },
  {
    type: "sleep",
    title: "晚上整理",
    text: "一段工作结束，它会整理今天留下的东西。早上可以撤回某一条。",
  },
];

const state = {
  view: "cover",
  boot: null,
  events: [],
  organism: null,
  card: null,
  origin: null,
  runId: null,
  busy: false,
  tour: 0,
  openSeq: null,
  es: null,
  confirm: null,
};

const $ = (id) => document.getElementById(id);

function esc(value) {
  return String(value ?? "").replace(/[&<>"']/g, (ch) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  }[ch]));
}

function why(text) {
  return WHY[text] || text || "";
}

function sitePhrase(event) {
  const sites = event.sites || [];
  const mlp = sites.includes("gate_proj");
  const delta = sites.includes("in_proj_qkv");
  const attn = sites.includes("q_proj");
  if (event.phase === "day" && delta && !mlp) return "白天只小改一层。";
  if (event.phase === "night" && delta && mlp && !attn) return "晚上整理，多改了一层。";
  if (attn && mlp) return "连原来会注意的部分也一起改。";
  return "";
}

function dest(name) {
  return DEST[name] || name || "—";
}

function last(type, events = state.events) {
  for (let i = events.length - 1; i >= 0; i -= 1) {
    if (events[i].type === type) return events[i];
  }
  return null;
}

function sentence(event) {
  switch (event.type) {
    case "meta":
      if (event.actor === "reference") return "这是标准答案在演示该怎么做，不是模型自己会了";
      if (event.actor === "model") return "这是真模型在做，做对做错都留下";
      return event.actor_label || "一次过程";
    case "task_start":
      return `${FAMILY_NAME[event.family] || "一件事"} · ${event.split === "exam" ? "这题算考试" : "这题是练习"}`;
    case "model_turn":
      return event.parsed ? "它决定动手" : "它没有说清楚要做什么";
    case "tool":
      if (event.refused && event.refused.length) return `这一步被拒绝了：${TOOL_NAME[event.name] || "这个动作"}`;
      if (event.name === "finish") return "它停下来，等着检查结果";
      return event.applied ? `${TOOL_NAME[event.name] || "它做了一个动作"}，已经执行` : `${TOOL_NAME[event.name] || "它提议了一个动作"}，没有改文件`;
    case "check":
      if (event.mode === "shadow") return `只看不改。文件改动：${(event.changed || []).join("、") || "没有"}`;
      if (event.mode === "assist") return `可以改这个临时文件夹。改动：${(event.changed || []).join("、") || "没有"}`;
      if (event.mode === "auto") return event.ok ? "这件事验过，放行了" : "这件事还没验过，没有放行";
      if (event.mode === "confirm") return "问过你了";
      return event.ok ? "这题做对了" : "这题没做对";
    case "absorb":
      return event.absorb ? "写进脑子已经比反复看提示划算" : "再读提示更便宜，所以先不写";
    case "ledger":
      return `${FAMILY_NAME[event.family] || "这件事"}：${dest(event.destination)}。做对 ${event.verified || 0} 次`;
    case "relabel":
      return "这题没做对。数字碰巧是另一种合法合计，只改个标签，不算这题做对。";
    case "write": {
      const where = event.write ? sitePhrase(event) : "这次没有写进脑子。";
      return `${dest(event.dest)}。${why(event.why)} ${where}`.trim();
    }
    case "sleep":
      return event.pressure ? "这段工作结束了，该整理了" : "还不到整理的时候";
    case "morning":
      return event.rollback ? `撤回了 ${event.rollback}` : "早上的小结写好了";
    case "gate":
      return GATE_LINE[event.id] || `${event.title || "考试"} · ${event.passed === false ? "还没过" : event.passed ? "过了" : "还没有结论"}`;
    case "confirm":
      return event.why || "等人点头";
    case "status":
      return event.label || event.phase || "";
    case "done":
      return "过程已经记完";
    case "error":
      return event.message || "出错了";
    default:
      return event.type;
  }
}

function tone(event) {
  if (event.type === "check" && event.mode === "shadow") return "";
  if (event.type === "check" && event.mode === "auto" && !event.ok) return "";
  if (event.type === "check") return event.ok ? "ok" : "bad";
  if (event.type === "tool" && event.refused && event.refused.length) return "bad";
  if (event.type === "error") return "bad";
  if (event.type === "write" && event.write) return "ok";
  return "";
}

function detail(event) {
  if (event.type === "model_turn") return event.text || "";
  if (event.type === "tool") {
    const args = event.arguments ? JSON.stringify(event.arguments, null, 2) : "";
    return [args, event.observation || event.error || ""].filter(Boolean).join("\n\n");
  }
  if (event.type === "task_start") return event.prompt || "";
  if (event.type === "morning") return event.text || "";
  if (event.type === "check" && event.changed) return `改动：${event.changed.join("，") || "没有"}`;
  return "";
}

function visibleEvents(events, highlight) {
  const rows = events.filter((event) => event.type !== "model_turn" && event.type !== "gate");
  if (!highlight) return rows;
  const picked = rows.filter((event) => event.type === highlight);
  return picked.length ? picked.slice(0, 3) : rows.slice(0, 4);
}

function plainNote(card, meta) {
  const actor = card?.actor || meta?.actor;
  if (actor === "reference") return "标准答案在演示该怎么做，不是模型自己会了。";
  if (actor === "model") return "这是真模型做的。做对做错都留着。";
  return "";
}

function replayTitle(row) {
  if (row.id === "reference_body") return "标准演示：表格算对了";
  if (row.id === "model_live" || row.ok === false && row.actor === "model") return "真模型做了一题，没做对";
  if (row.actor === "model") return "真模型的一次记录";
  if (row.actor === "reference") return "标准答案的一次演示";
  return row.title || "一次记录";
}

function renderTimeline(target, events, highlight) {
  const node = $(target);
  if (!node) return;
  const shown = visibleEvents(events, highlight);
  if (!shown.length) {
    node.innerHTML = '<li class="node"><p>还没有过程。先看一段已经录好的标准演示。</p></li>';
    return;
  }
  node.innerHTML = shown.map((event) => {
    const dim = highlight && event.type !== highlight ? " dim" : "";
    const on = highlight && event.type === highlight ? " on" : "";
    const open = state.openSeq === event.seq;
    const extra = open ? `<pre class="detail">${esc(detail(event) || JSON.stringify(event, null, 2))}</pre>` : "";
    return `<li class="node ${tone(event)}${dim}${on}">
      <button type="button" class="plain" data-seq="${esc(event.seq)}">
        <div class="kicker">${esc(TITLES[event.type] || event.type)}</div>
        <div>${esc(sentence(event))}</div>
      </button>
      ${extra}
    </li>`;
  }).join("");
  node.querySelectorAll("button[data-seq]").forEach((button) => {
    button.addEventListener("click", () => {
      const seq = Number(button.dataset.seq);
      state.openSeq = state.openSeq === seq ? null : seq;
      paint();
    });
  });
  if (state.busy && state.view === "studio") node.lastElementChild?.scrollIntoView({ block: "nearest" });
  if (state.view === "tour") {
    node.querySelector(".node.on")?.scrollIntoView({ block: "center" });
  }
}

function badge() {
  const meta = last("meta");
  const origin = state.origin === "history" ? "已经录好的" : state.origin === "live" ? "正在发生" : "";
  const who = meta?.actor === "model" ? "真模型" : meta?.actor === "reference" ? "标准答案" : "";
  return [origin, who].filter(Boolean).join(" · ");
}

function show(view) {
  state.view = view;
  document.querySelectorAll(".view").forEach((section) => {
    section.hidden = section.id !== view;
  });
  document.querySelectorAll(".nav-btn").forEach((button) => {
    button.classList.toggle("active", button.dataset.view === view);
  });
  if (view === "tour") ensureTour();
  if (view === "books") paintBooks();
  if (view === "arena") paintArena();
  paint();
}

function paint() {
  const flag = badge();
  const note = plainNote(state.card, last("meta"));
  if ($("studio-flag")) $("studio-flag").textContent = [flag, note].filter(Boolean).join("。");
  if ($("tour-flag")) $("tour-flag").textContent = flag;
  if ($("pilot-flag")) $("pilot-flag").textContent = state.view === "pilot" ? [flag, note].filter(Boolean).join(" — ") : "";
  const highlight = state.view === "tour" ? TOUR[state.tour].type : null;
  if (state.view === "studio") renderTimeline("studio-timeline", state.events, null);
  if (state.view === "tour") renderTimeline("tour-timeline", state.events, highlight);
  if (state.view === "pilot") renderTimeline("pilot-timeline", state.events, null);
  paintSide();
  paintBar();
  paintTourCopy();
  const pending = pendingConfirm();
  $("modal").hidden = !pending;
  if (pending) {
    const args = pending.arguments ? JSON.stringify(pending.arguments) : "";
    $("modal-body").textContent = `${pending.why || ""} ${pending.name || ""} ${args}`.trim();
    state.confirm = pending;
  }
}

function pendingConfirm() {
  const event = last("confirm");
  if (!event || !state.runId || !state.busy) return null;
  const after = state.events.slice(state.events.indexOf(event) + 1);
  if (after.some((item) => item.type === "tool" || item.type === "done" || item.type === "error")) return null;
  return event;
}

function paintTourCopy() {
  const box = $("tour-copy");
  const list = $("tour-steps");
  if (!box || !list) return;
  list.innerHTML = TOUR.map((step, index) =>
    `<li><button type="button" class="${index === state.tour ? "on" : ""}" data-tour="${index}">0${index + 1} ${esc(step.title)}</button></li>`
  ).join("");
  list.querySelectorAll("button").forEach((button) => {
    button.addEventListener("click", () => {
      state.tour = Number(button.dataset.tour);
      paint();
    });
  });
  const step = TOUR[state.tour];
  const found = state.events.some((event) => event.type === step.type);
  box.innerHTML = `<h2>${esc(step.title)}</h2><p class="lede">${esc(step.text)}</p>${found ? "" : "<p class=\"hint\">这段记录里还没有这一格。规则先写在这里。</p>"}`;
}

function paintSide() {
  const side = $("studio-side");
  if (!side || state.view !== "studio") return;
  const check = last("check");
  const files = (check && check.files) || [];
  const license = state.organism?.license;
  const grants = license ? license.grants.join("、") : "python、shell、read、write、http";
  const fileHtml = files.length
    ? files.map((file) => `<div class="file"><strong>${esc(file.path)}</strong><pre class="detail">${esc(file.text || "")}</pre></div>`).join("")
    : "<p class=\"hint\">工作区还是空的。跑起来之后，文件会出现在这里。</p>";
  side.innerHTML = `
    <p class="eyebrow">这一题</p>
    <h2>${check ? (check.ok ? "做对了" : "没做对") : "还没检查"}</h2>
    <p class="hint">它只能做被允许的事。不能跑出这个文件夹。删东西、付款、发消息要先问你。</p>
    <p class="hint">允许的种类：${esc(grants)}。</p>
    ${fileHtml}`;
}

function paintBar() {
  const bar = $("studio-bar");
  if (!bar || state.view !== "studio") return;
  const ledger = last("ledger");
  const absorb = last("absorb");
  const sleep = last("sleep");
  const uses = absorb && absorb.breakeven_uses != null ? Number(absorb.breakeven_uses) : null;
  const seen = absorb ? Number(absorb.seen || 0) : 0;
  const width = uses ? Math.min(100, (seen / uses) * 100) : 0;
  const wrote = last("write");
  const memoryLine = wrote
    ? (wrote.write ? dest(wrote.dest) : "这次没有写进脑子")
    : (!ledger ? "还只是记住，没写进脑子" : dest(ledger.destination));
  const costLine = !absorb ? "还没比较划不划算" : absorb.absorb ? "写进脑子已经划算" : "再读提示更便宜，所以先不写";
  const nightLine = sleep?.pressure ? "这段工作结束了" : "还在白天";
  bar.innerHTML = `
    <div><strong>${esc(memoryLine)}</strong><span>${esc(ledger ? `这类事做对 ${ledger.verified || 0} 次` : "还没有记上一类事")}</span></div>
    <div><strong>${esc(costLine)}</strong><span>${esc(uses ? `见过 ${seen} 次，大约 ${uses.toFixed(0)} 次才划算` : "还没有一条做对的练习")}</span><div class="meter"><i style="width:${width}%"></i></div></div>
    <div><strong>${esc(nightLine)}</strong><span>${esc(sleep ? "到了该整理的时候" : "这段还没结束")}</span></div>`;
}

function paintBooks() {
  const body = $("books-body");
  const note = $("books-note");
  if (!body) return;
  const organism = state.organism;
  if (!organism) {
    note.textContent = "先看一段已经录好的演示。这里会告诉你，它有没有把这件事写进脑子。";
    body.innerHTML = "";
    return;
  }
  note.textContent = "下面是这一轮实际记住了什么。没写进脑子，就还只是记住。";
  const rule = `<p class="lede">白天只小改一层。晚上整理才动更多层。这家的字段名不外传。做错但数字碰巧是另一种合法合计，只改个标签，不算这题做对。</p>`;
  const families = organism.families || {};
  const names = Object.keys(families);
  const live = state.origin === "live" && state.runId;
  const cards = names.map((name) => {
    const row = families[name];
    const absorb = row.absorb;
    const uses = absorb && absorb.breakeven_uses != null ? Number(absorb.breakeven_uses) : null;
    const rungs = ["fast", "slot", "local", "core"].map((id) =>
      `<span class="rung ${row.ledger === id ? "on" : ""}">${esc(dest(id))}</span>`
    ).join("");
    return `<article class="book">
      <p class="eyebrow">${esc(FAMILY_NAME[name] || name)}</p>
      <div class="rungs">${rungs}</div>
      <p class="hint">亮着的是现在走到的那一格。真正写没写，看下面的小结。</p>
      <p class="hint">${esc(uses ? `见过 ${absorb.seen} 次。大约 ${uses.toFixed(0)} 次再写才划算。` : "还没数过写进去划不划算。")}</p>
    </article>`;
  }).join("");
  const commits = (organism.morning && organism.morning.commits) || organism.writes || [];
  const commitHtml = commits.map((row) => {
    const button = live ? `<button type="button" class="ghost" data-rollback="${esc(row.name)}">撤回 ${esc(row.name)}</button>` : "";
    return `<li class="node"><div>${esc(row.name)} → ${esc(dest(row.dest))}。${esc(why(row.why))}</div>${button}</li>`;
  }).join("");
  const morning = organism.morning && organism.morning.text
    ? `<details class="fold"><summary>看原来的英文记录</summary><pre class="morning">${esc(organism.morning.text)}</pre></details>`
    : "";
  const history = live ? "" : "<p class=\"hint\">这是已经录好的。当时的小结不能改。正在发生的这一轮，可以撤回某一条。</p>";
  body.innerHTML = `${rule}<div class="arm-grid">${cards || "<p class=\"hint\">这次还没有记上一类事。</p>"}</div>
    <h2>早上的小结</h2>
    ${history}
    <ol class="rail">${commitHtml || "<li class=\"node\">这次没有写进脑子。</li>"}</ol>
    ${morning}
    <h2>交给另一台</h2>
    <p class="lede">点下去如果还不是通用本事，另一台什么都收不到。旁边的演练只是演示清理私有名字，不是这次考试的分数。</p>
    <div class="stack row">
      ${names.map((name) => `<button type="button" class="ghost" data-share="${esc(name)}">把 ${esc(name)} 交出去</button>`).join("")}
      <button type="button" class="ghost" id="fleet-drill">看一次去私有化演练</button>
    </div>
    <div id="desk-result"></div>
    <h2>换成新的底子</h2>
    <p class="lede">带走练过的题。不带走旧的权重。考题不在里面。</p>
    <button type="button" class="ghost" id="carry-base">换成一具新基座</button>
    <div id="carry-result"></div>`;
  body.querySelectorAll("[data-rollback]").forEach((button) => {
    button.addEventListener("click", () => rollback(button.dataset.rollback));
  });
  body.querySelectorAll("[data-share]").forEach((button) => {
    button.addEventListener("click", () => shareFamily(button.dataset.share));
  });
  $("fleet-drill")?.addEventListener("click", showDrill);
  $("carry-base")?.addEventListener("click", carryBase);
}

async function shareFamily(name) {
  const target = state.runId
    ? `/api/live/${state.runId}/share`
    : state.card?.id
      ? `/api/replays/${state.card.id}/share`
      : "";
  const box = $("desk-result");
  if (!target || !box) return;
  const response = await fetch(target, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name }),
  });
  const result = await response.json();
  if (!response.ok) {
    box.textContent = result.detail || "没有交出去。";
    return;
  }
  if (result.ok) {
    box.innerHTML = `<p>另一台收到的是占位符，不是这一家的原文字。</p><pre class="morning">${esc(result.text)}</pre>`;
    return;
  }
  if (result.why === "leak") {
    box.textContent = "私有字符串还在，另一台什么都没收到。";
    return;
  }
  box.textContent = "这一轮还不是通用核。另一台什么都没收到。";
}

async function carryBase() {
  const box = $("carry-result");
  const target = state.runId
    ? `/api/live/${state.runId}/carry`
    : state.card?.id
      ? `/api/replays/${state.card.id}/carry`
      : "";
  if (!box || !target) return;
  const response = await fetch(target, { method: "POST" });
  const result = await response.json();
  if (!response.ok) {
    box.textContent = result.detail || "没有换成新基座。";
    return;
  }
  box.textContent = `${result.note} 带走 ${result.practice} 条练习，丢下 ${result.exams_dropped} 道考题。`;
}

async function showDrill() {
  const box = $("desk-result");
  if (!box) return;
  const drill = await fetch("/api/fleet").then((response) => response.json());
  box.innerHTML = `
    <p>${drill.leak_blocked ? "私有字符串还在，导出被拒绝。" : ""}</p>
    <p>${drill.export_ok ? "换成占位符之后，文本里已经没有那家的客户名。" : ""}</p>
    <p>${drill.helped ? "另一台填上自己的字段，就能做同类的事。" : ""}</p>
    <p class="hint">${esc(drill.note || "")}</p>`;
}

function paintArena() {
  if (!state.boot || state.view !== "arena") return;
  $("arena-arms").innerHTML = `<details class="fold"><summary>七种对照是什么</summary><div class="arm-grid">${state.boot.arms.map((arm) =>
    `<article><h3>${esc(arm.title)}</h3><p>${esc(arm.text)}</p></article>`
  ).join("")}</div></details>`;
  $("arena-gates").innerHTML = state.boot.gates.map((gate, index) => {
    const failed = gate.passed === false;
    const label = failed ? "还没过" : gate.passed ? "过了" : "还没有结论";
    const klass = failed ? "bad" : gate.passed ? "ok" : "";
    const line = GATE_LINE[gate.id] || gate.about;
    return `<article class="gate"><span class="chip ${klass}">第 ${index + 1} 次考试 · ${label}</span><p class="lede">${esc(line)}</p><details class="fold"><summary>看原来的考试原文</summary><pre>${esc(gate.body)}</pre></details></article>`;
  }).join("");
}

function fillForm() {
  const boot = state.boot;
  if (!boot) return;
  $("family").innerHTML = boot.families.map((item) => `<option value="${esc(item.id)}">${esc(FAMILY_NAME[item.id] || item.id)}</option>`).join("");
  $("arm").innerHTML = boot.arms.map((item) => `<option value="${esc(item.id)}" ${item.id === "dual" ? "selected" : ""}>${esc(item.title)}</option>`).join("");
  $("model").innerHTML = boot.models.map((item) =>
    `<option value="${esc(item.id)}" ${item.ready ? "" : "disabled"}>${esc(item.id)}${item.ready ? "" : "（这台机器上还没有）"}</option>`
  ).join("");
  const ready = boot.models.find((item) => item.ready);
  if (ready) $("model").value = ready.id;
  fillReplays();
  blurbs();
  const chips = boot.gates.map((gate, index) => {
    const label = gate.passed === false ? `第 ${index + 1} 次考试还没过` : gate.passed ? `第 ${index + 1} 次考试过了` : `第 ${index + 1} 次考试还没有结论`;
    const klass = gate.passed === false ? "bad" : gate.passed ? "ok" : "";
    return `<button type="button" class="chip ${klass}" data-gate="${esc(gate.id)}">${esc(label)}</button>`;
  }).join("");
  $("cover-gates").innerHTML = chips;
  $("cover-gates").querySelectorAll("[data-gate]").forEach((button) => {
    button.addEventListener("click", () => {
      const gate = boot.gates.find((item) => item.id === button.dataset.gate);
      const box = $("cover-gate-detail");
      if (!gate || !box) return;
      const open = box.dataset.open === gate.id;
      box.dataset.open = open ? "" : gate.id;
      box.innerHTML = open ? "" : `<details class="fold" open><summary>看原来的考试原文</summary><pre class="morning">${esc(gate.body)}</pre></details>`;
    });
  });
}

function fillReplays() {
  const rows = state.boot?.replays || [];
  const keep = state.origin === "history" ? ($("replay").value || "") : "";
  const options = ['<option value="">屏幕上的这一轮</option>'].concat(
    rows.map((row) => `<option value="${esc(row.id)}">${esc(replayTitle(row))}</option>`)
  );
  $("replay").innerHTML = options.join("");
  if (state.origin === "history" && keep && rows.some((row) => row.id === keep)) $("replay").value = keep;
  else if (state.origin !== "history") $("replay").value = "";
}

function blurbs() {
  const hints = {
    table: "读一张表，按条件加总，把结果写出来。",
    file: "按规则搬动文件。",
    report: "把算出来的数字写进说明。",
    shell: "只允许很少几条命令。",
    http: "访问这台电脑上的接口。",
    mixed: "几步连着做。",
  };
  const arm = state.boot.arms.find((item) => item.id === $("arm").value);
  $("family-blurb").textContent = hints[$("family").value] || "";
  $("arm-blurb").textContent = arm ? arm.text : "";
}

function stopStream() {
  if (state.es) {
    state.es.close();
    state.es = null;
  }
}

async function loadReplay(id) {
  if (!id) return;
  stopStream();
  state.busy = false;
  const response = await fetch(`/api/replays/${encodeURIComponent(id)}`);
  if (!response.ok) {
    $("studio-status").textContent = "没有读到这段记录。";
    return;
  }
  const body = await response.json();
  state.events = body.events || [];
  state.organism = body.organism;
  state.card = body.card;
  state.origin = "history";
  state.runId = null;
  state.openSeq = null;
  $("studio-status").textContent = plainNote(body.card, null);
  if ($("replay") && body.card?.id) {
    const option = [...$("replay").options].some((item) => item.value === body.card.id);
    if (option) $("replay").value = body.card.id;
  }
  paint();
  if (state.view === "books") paintBooks();
}

async function ensureTour() {
  if (state.events.length) return;
  const replay = (state.boot?.replays || []).find((item) => item.id === "reference_body") || state.boot?.replays?.[0];
  if (!replay) {
    $("tour-flag").textContent = "还没有记录。先到「看它干活」，让标准答案做一小段。";
    return;
  }
  await loadReplay(replay.id);
}

async function startLive(spec) {
  stopStream();
  state.events = [];
  state.organism = null;
  state.card = {
    source: "live",
    actor: spec.actor,
    note: spec.actor === "model" ? "现场模型，做对做错都留下。" : "标准答案在演示身体该怎么动。",
  };
  state.origin = "live";
  state.busy = true;
  state.runId = null;
  $("studio-status").textContent = spec.actor === "model" ? "正在装模型，然后做一题。" : "正在跑一小段白天。";
  setBusy(true);
  paint();
  const response = await fetch("/api/live", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(spec),
  });
  const body = await response.json();
  if (!response.ok) {
    state.busy = false;
    setBusy(false);
    $("studio-status").textContent = body.detail || "没有跑起来。";
    return;
  }
  state.runId = body.id;
  const stream = new EventSource(`/api/live/${body.id}/events`);
  state.es = stream;
  stream.onmessage = async (message) => {
    const event = JSON.parse(message.data);
    state.events.push(event);
    if (event.type === "done" || event.type === "error") {
      stream.close();
      state.es = null;
      state.busy = false;
      setBusy(false);
      const snap = await fetch(`/api/live/${body.id}`).then((res) => res.json());
      state.organism = snap.organism;
      if (event.type === "error") $("studio-status").textContent = event.message || "出错了。";
      else $("studio-status").textContent = "这一轮记完了。到「它记得什么」看这次有没有写进脑子。";
      const boot = await fetch("/api/bootstrap").then((res) => res.json());
      state.boot.replays = boot.replays;
      fillReplays();
      document.querySelector("#studio .stage")?.scrollTo(0, 0);
    }
    paint();
  };
  stream.onerror = () => {
    if (!state.busy) return;
    $("studio-status").textContent = "和本机服务的连接断了。";
  };
}

async function startPilot(mode) {
  stopStream();
  show("pilot");
  state.events = [];
  state.organism = null;
  state.card = { source: "live", note: "临时文件夹里的一次放权。" };
  state.origin = "live";
  state.busy = true;
  state.runId = null;
  paint();
  const response = await fetch("/api/pilot", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ mode }),
  });
  const body = await response.json();
  state.runId = body.id;
  const stream = new EventSource(`/api/live/${body.id}/events`);
  state.es = stream;
  stream.onmessage = (message) => {
    const event = JSON.parse(message.data);
    state.events.push(event);
    if (event.type === "done" || event.type === "error") {
      stream.close();
      state.es = null;
      state.busy = false;
    }
    paint();
  };
}

async function answerConfirm(yes) {
  const pending = state.confirm;
  if (!pending || !state.runId) return;
  await fetch(`/api/pilot/${state.runId}/confirm`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ token: pending.token, yes }),
  });
}

async function rollback(name) {
  if (!state.runId) return;
  const response = await fetch(`/api/live/${state.runId}/rollback`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name }),
  });
  const body = await response.json();
  if (!response.ok) {
    $("books-note").textContent = body.detail || "撤回没有做成。";
    return;
  }
  state.organism = body.organism;
  const snap = await fetch(`/api/live/${state.runId}`).then((res) => res.json());
  state.events = snap.events || state.events;
  paintBooks();
}

const LESSON = [
  {
    title: "要解决什么",
    view: "cover",
    ask: "为什么不能只做一个会聊天、每次把说明书再读一遍的助手？",
    look: "先读这一页。它会在电脑上干活，但三次考试都还没通过，所以它还不会办公。",
    conclusion: "要证明的是边干活边把反复的做法写进自己，下一次少看说明书。",
    cannot: "不能说成：它已经会办公。",
    learns: 0,
  },
  {
    title: "标准答案怎样把一件事做完",
    view: "studio",
    replay: "reference_body",
    ask: "一件「把已付款的行加总」的事，做完之后凭什么说它做对了？",
    look: "看中间时间线上的「这题做对了」，以及右边写出来的合计。",
    conclusion: "检查看的是文件夹里的结果，不听它自己说。",
    cannot: "不能说成：这是模型做对的。这是标准答案在演示。",
    spot: "这题做对了",
    spotAlso: "#studio-side",
    learns: 1,
  },
  {
    title: "做对了为什么还没写进脑子",
    view: "studio",
    replay: "reference_body",
    ask: "表格算对了，为什么还不算学会？",
    look: "看最下面一行。它应该写着这次没有写进脑子。",
    conclusion: "做对一次只记住。写进权重要更划算才发生，这次还没写。做对和学会不是一回事。",
    cannot: "不能说成：演示做对了等于学会了。",
    spotBar: true,
    learns: 1,
  },
  {
    title: "真模型做同一件事会怎样",
    view: "studio",
    replay: "model_live",
    ask: "换上当时真的跑过的小模型，同一类表格题怎么样？",
    look: "看时间线上的「这题没做对」。",
    conclusion: "真模型那一题没做对。界面没有把它换成标准答案。",
    cannot: "不能说成：模型已经和标准答案一样会做表。",
    spot: "这题没做对",
    learns: 2,
  },
  {
    title: "它打算怎样记住",
    view: "books",
    replay: "reference_body",
    ask: "记住、写进脑子、只留给这家、变成谁都能用，这四格有什么差别？",
    look: "看四格梯子，再看「另一台什么都没收到」。",
    conclusion: "这家的表头不外传。还不是通用本事时，另一台什么都收不到。",
    cannot: "不能说成：已经可以分发给别的公司。",
    spotSelector: ".rungs",
    share: "table",
    learns: 4,
  },
  {
    title: "三次考试各在考什么",
    view: "arena",
    ask: "这三次考试分别在问什么，结果是什么？",
    look: "三张卡都在说还没过。第 2 张写着样本不够，不是赢了。",
    conclusion: "三次考试都还没过。办公题上还没赢过只看说明书的做法，样本也不够，不能说赢了。",
    cannot: "不能说成：界面把考试改判了。原文仍收在每张卡片里。",
    spotSelector: "#arena-gates",
    learns: 3,
  },
  {
    title: "你自己接着可以点什么",
    view: "studio",
    ask: "课结束之后，三个按钮分别会发生什么？",
    look: "左边三个按钮：看录像、再让标准答案做一小段、让真模型做一题。这一课不会替你去跑模型。",
    conclusion: "看录像马上能看。再让标准答案做一小段是重放手脚。让真模型做一题要等，而且可能做错。",
    cannot: "不能说成：点了真模型就会通过考试。",
    spotSelector: "#studio-actions",
    cycle: ["play-replay", "run-reference", "run-model"],
    learns: 4,
  },
];

const LESSON_NOTES = [
  "它是一个会在电脑上干活的小模型，要研究的是反复做的事能不能写进它自己，让下一次少看说明书。",
  "标准演示里表格做对了，但这次没有写进脑子。做对和学会不是一回事。",
  "真模型那一题没做对。界面没有把它换成标准答案。",
  "三次考试都还没过。办公题上还没赢过只看说明书的做法，样本也不够，不能说赢了。",
  "左边五页分别回答：它怎么干活、记住了什么、考试怎样、能不能改你的文件。数据不出这台电脑。",
];

function startLesson() {
  state.lesson = { on: true, step: 0 };
  localStorage.removeItem("evo-lesson-done");
  document.body.classList.add("lesson");
  $("lesson").hidden = false;
  if ($("lesson-again")) $("lesson-again").hidden = true;
  return renderLesson();
}

function endLesson(done) {
  state.lesson = { on: false, step: 0 };
  document.body.classList.remove("lesson");
  $("lesson").hidden = true;
  clearSpots();
  if (state.lessonTimer) clearInterval(state.lessonTimer);
  if (done) {
    localStorage.setItem("evo-lesson-done", "1");
    const learned = $("learned");
    if (learned) {
      learned.hidden = false;
      learned.innerHTML = LESSON_NOTES.map((line) => `<li>${esc(line)}</li>`).join("");
    }
    if ($("lesson-again")) $("lesson-again").hidden = false;
    show("cover");
  }
}

function clearSpots() {
  document.querySelectorAll(".lesson-spot").forEach((el) => el.classList.remove("lesson-spot"));
}

function mark(el) {
  if (!el) return;
  el.classList.add("lesson-spot");
  el.scrollIntoView({ block: "nearest", inline: "nearest" });
}

function spot(el) {
  clearSpots();
  mark(el);
}

function renderNotes(upto) {
  const list = $("lesson-notes");
  if (!list) return;
  list.innerHTML = LESSON_NOTES.map((line, index) =>
    `<li class="${index <= upto ? "" : "soon"}">${esc(line)}</li>`
  ).join("");
  const map = $("lesson-map");
  if (!map) return;
  map.innerHTML = LESSON.map((lesson, index) => {
    const mark = index < state.lesson.step ? "done" : index === state.lesson.step ? "now" : "";
    return `<li class="${mark}" title="${esc(lesson.title)}">${index + 1}</li>`;
  }).join("");
}

async function renderLesson() {
  const lesson = LESSON[state.lesson.step];
  $("lesson-progress").textContent = `第 ${state.lesson.step + 1} 课 / 共 ${LESSON.length} 课`;
  $("lesson-title").textContent = lesson.title;
  $("lesson-ask").textContent = lesson.ask;
  $("lesson-look").textContent = lesson.look;
  $("lesson-conclusion").textContent = lesson.conclusion;
  $("lesson-cannot").textContent = lesson.cannot;
  $("lesson-latest").textContent = LESSON_NOTES[lesson.learns] ? "记下了：" + LESSON_NOTES[lesson.learns] : "";
  $("lesson-next").textContent = state.lesson.step === LESSON.length - 1 ? "我看完了" : "下一步";
  $("lesson-prev").disabled = state.lesson.step === 0;
  $("lesson-missing").hidden = true;
  renderNotes(lesson.learns);
  show(lesson.view);
  if (lesson.replay) {
    const ok = await ensureReplay(lesson.replay);
    if (!ok) $("lesson-missing").hidden = false;
    if (lesson.view === "books") show("books");
  }
  if (state.lessonTimer) clearInterval(state.lessonTimer);
  state.lessonTimer = null;
  if (lesson.share && state.card?.id) {
    await shareFamily(lesson.share);
    clearSpots();
    mark(document.querySelector(".rungs"));
    mark($("desk-result"));
    return;
  }
  clearSpots();
  if (lesson.spot) {
    const root = document.querySelector("#studio-timeline") || document.body;
    const hit = [...root.querySelectorAll(".node")].find((node) => node.innerText.includes(lesson.spot));
    spot(hit);
  } else if (lesson.spotBar) {
    const strong = [...document.querySelectorAll("#studio-bar strong")].find((node) => node.textContent.includes("没有写进脑子"));
    spot(strong || $("studio-bar"));
  } else if (lesson.spotSelector) {
    spot(document.querySelector(lesson.spotSelector));
  }
  if (lesson.spotAlso) mark(document.querySelector(lesson.spotAlso));
  if (lesson.cycle) {
    let index = 0;
    const tick = () => {
      spot($(lesson.cycle[index % lesson.cycle.length]));
      index += 1;
    };
    tick();
    state.lessonTimer = setInterval(tick, 900);
  }
}

async function ensureReplay(id) {
  if (state.card?.id === id && state.events.length) return true;
  await loadReplay(id);
  return state.card?.id === id;
}

function setBusy(busy) {
  ["play-replay", "run-reference", "run-model"].forEach((id) => {
    $(id).disabled = busy;
  });
}

function bind() {
  document.querySelectorAll(".nav-btn").forEach((button) => {
    button.addEventListener("click", () => show(button.dataset.view));
  });
  $("goto-tour").addEventListener("click", () => {
    localStorage.setItem("evo-studio-seen", "1");
    show("tour");
  });
  $("goto-books").addEventListener("click", async () => {
    localStorage.setItem("evo-studio-seen", "1");
    if (!state.organism) await ensureTour();
    show("books");
  });
  $("goto-arena").addEventListener("click", () => {
    localStorage.setItem("evo-studio-seen", "1");
    show("arena");
  });
  $("tour-next").addEventListener("click", () => {
    if (state.tour < TOUR.length - 1) state.tour += 1;
    else {
      localStorage.setItem("evo-studio-seen", "1");
      show("studio");
      return;
    }
    paint();
  });
  $("tour-prev").addEventListener("click", () => {
    state.tour = Math.max(0, state.tour - 1);
    paint();
  });
  $("family").addEventListener("change", blurbs);
  $("arm").addEventListener("change", blurbs);
  $("play-replay").addEventListener("click", () => {
    const id = $("replay").value || "reference_body";
    show("studio");
    loadReplay(id);
  });
  $("run-reference").addEventListener("click", () => {
    show("studio");
    startLive({
      family: $("family").value,
      arm: $("arm").value,
      actor: "reference",
      span: "day",
      model: $("model").value,
      seed: 0,
    });
  });
  $("run-model").addEventListener("click", () => {
    show("studio");
    startLive({
      family: $("family").value,
      arm: $("arm").value,
      actor: "model",
      span: "task",
      model: $("model").value,
      seed: 0,
    });
  });
  document.querySelectorAll("[data-pilot]").forEach((button) => {
    button.addEventListener("click", () => startPilot(button.dataset.pilot));
  });
  $("modal-yes").addEventListener("click", () => answerConfirm(true));
  $("modal-no").addEventListener("click", () => answerConfirm(false));
  $("lesson-next").addEventListener("click", async () => {
    if (!state.lesson?.on) return;
    if (state.lesson.step >= LESSON.length - 1) {
      endLesson(true);
      return;
    }
    state.lesson.step += 1;
    await renderLesson();
  });
  $("lesson-prev").addEventListener("click", async () => {
    if (!state.lesson?.on || state.lesson.step === 0) return;
    state.lesson.step -= 1;
    await renderLesson();
  });
  $("lesson-leave").addEventListener("click", () => endLesson(true));
  const restart = async () => {
    await startLesson();
  };
  $("lesson-restart").addEventListener("click", restart);
  $("lesson-again").addEventListener("click", restart);
  $("lesson-notes-toggle").addEventListener("click", () => {
    $("lesson-notes").hidden = !$("lesson-notes").hidden;
  });
}

async function main() {
  bind();
  const response = await fetch("/api/bootstrap");
  state.boot = await response.json();
  fillForm();
  if (!localStorage.getItem("evo-lesson-done")) await startLesson();
  else {
    show("cover");
    $("lesson-again").hidden = false;
  }
}

main();
