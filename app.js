const reports = [
  { id: 1, title: "AI note-taking tools: market outlook 2026", topic: "AI note-taking tools", date: "Aug 30, 2026", sources: 47, status: "Completed", summary: "Category growth, competitive positioning and whitespace in the fast-moving AI meeting assistant market.", region: "Global" },
  { id: 2, title: "Vertical farming opportunity in India", topic: "Vertical farming India", date: "Aug 29, 2026", sources: 31, status: "Draft", summary: "Demand drivers, unit economics and go-to-market options for controlled-environment agriculture.", region: "India" },
  { id: 3, title: "European HR software landscape", topic: "European HR software", date: "Aug 27, 2026", sources: 56, status: "Completed", summary: "A market map of mid-market HRIS vendors, buyer priorities and regional growth pockets.", region: "Europe" },
  { id: 4, title: "Embedded finance for B2B marketplaces", topic: "Embedded finance", date: "Aug 25, 2026", sources: 42, status: "Completed", summary: "Adoption patterns and strategic opportunities at the intersection of vertical SaaS and payments.", region: "North America" },
  { id: 5, title: "Climate accounting software signals", topic: "Climate software", date: "Aug 21, 2026", sources: 38, status: "Completed", summary: "Regulatory tailwinds, buyer behavior and competitor differentiation in carbon accounting.", region: "Europe" },
  { id: 6, title: "Conversational commerce in Southeast Asia", topic: "Conversational commerce", date: "Aug 18, 2026", sources: 61, status: "Completed", summary: "Platform dynamics and emerging opportunities across social and messaging-led commerce.", region: "Asia Pacific" }
];

const agents = [
  { code:"MM", name:"Market Mapper", role:"Market intelligence", desc:"Sizes the opportunity, segments demand and maps the structural forces shaping the category.", color:"rose", tasks:"Market sizing · Segmentation · Growth drivers" },
  { code:"SS", name:"Signal Scout", role:"Trend intelligence", desc:"Surfaces emerging themes, behavioral shifts and weak signals before they become consensus.", color:"blue", tasks:"Trends · Customer signals · Horizon scan" },
  { code:"CA", name:"Competitor Analyst", role:"Competitive intelligence", desc:"Compares products, positioning and business models to reveal strategic whitespace.", color:"purple", tasks:"Landscape · Benchmarking · Positioning" },
  { code:"IE", name:"Insight Editor", role:"Research synthesis", desc:"Connects every finding into a clear narrative with practical recommendations and next steps.", color:"amber", tasks:"Synthesis · Implications · Recommendations" },
  { code:"CP", name:"Customer Pulse", role:"Voice of customer", desc:"Synthesizes customer language, pain points and buying criteria from qualitative signals.", color:"blue", tasks:"Pain points · Jobs-to-be-done · Buying criteria" },
  { code:"RE", name:"Risk Examiner", role:"Strategic risk", desc:"Stress-tests assumptions and identifies regulatory, adoption and execution risks.", color:"rose", tasks:"Risk analysis · Scenarios · Assumptions" }
];

const icons = {
  report: '<svg viewBox="0 0 24 24"><path d="M6 3h9l4 4v14H6zM14 3v5h5M9 13h7M9 17h5"/></svg>'
};

const views = {
  dashboard: document.querySelector('#dashboardView'), reports: document.querySelector('#reportsView'),
  agents: document.querySelector('#agentsView'), run: document.querySelector('#runView'), detail: document.querySelector('#reportDetailView')
};

let currentReport = reports[0];
let runTimer = null;

function showView(name) {
  Object.values(views).forEach(view => view.classList.add('hidden'));
  views[name].classList.remove('hidden');
  document.querySelectorAll('.nav-item').forEach(item => item.classList.toggle('active', item.dataset.view === name));
  const crumbs = {dashboard:'Overview', reports:'Research reports', agents:'Agent library', run:'Live research', detail:'Report'};
  document.querySelector('.breadcrumb strong').textContent = crumbs[name] || 'Overview';
  window.scrollTo({top:0, behavior:'smooth'});
  closeMobileNav();
}

function reportRow(report) {
  return `<article class="report-row" data-report="${report.id}"><span class="report-type">${icons.report}</span><span class="report-info"><strong>${report.title}</strong><small>${report.summary}</small></span><span class="report-meta"><small>Sources</small><strong>${report.sources} verified</strong></span><span class="report-meta"><small>Updated</small><strong>${report.date}</strong></span><span class="report-status ${report.status === 'Draft' ? 'draft' : ''}">${report.status}</span></article>`;
}

function reportCard(report) {
  return `<article class="report-card" data-report="${report.id}"><span class="report-type">${icons.report}</span><span class="report-status ${report.status === 'Draft' ? 'draft' : ''}">${report.status}</span><h3>${report.title}</h3><p>${report.summary}</p><div class="report-card-footer"><span>${report.region} · ${report.sources} sources</span><span>${report.date}</span></div></article>`;
}

function renderReports(items = reports) {
  document.querySelector('#recentReports').innerHTML = reports.slice(0,3).map(reportRow).join('');
  document.querySelector('#fullReportGrid').innerHTML = items.map(reportCard).join('') || '<p>No reports match your search.</p>';
  document.querySelectorAll('[data-report]').forEach(el => el.addEventListener('click', () => openReport(Number(el.dataset.report))));
}

function renderAgents() {
  document.querySelector('#agentLibrary').innerHTML = agents.map((a,i) => `<article class="library-agent-card"><span class="agent-icon ${a.color}">${a.code}</span><div><small class="eyebrow">${a.role}</small><h3>${a.name}</h3><p>${a.desc}</p><div class="agent-meta"><span>${a.tasks}</span></div></div><button class="toggle ${i < 4 ? 'on' : ''}" aria-label="Toggle ${a.name}"><span></span></button></article>`).join('');
  document.querySelectorAll('.toggle').forEach(toggle => toggle.addEventListener('click', () => { toggle.classList.toggle('on'); toast(toggle.classList.contains('on') ? 'Agent activated' : 'Agent paused'); }));
}

function buildReport(report) {
  return `<span class="doc-kicker">Market intelligence brief</span><h1>${report.title}</h1><div class="doc-meta">Prepared by AI Market Research Crew · ${report.date} · ${report.region} · ${report.sources} sources reviewed</div><h2>Executive summary</h2><p>The market is moving from broad experimentation toward workflow-specific products with clear, measurable value. Buyers increasingly favor solutions that reduce coordination costs, integrate into existing systems and demonstrate trust through transparent controls.</p><div class="metric-grid"><div class="metric"><strong>$4.8B</strong><span>Illustrative market size</span></div><div class="metric"><strong>21.4%</strong><span>Projected annual growth</span></div><div class="metric"><strong>7 / 10</strong><span>Market momentum score</span></div></div><div class="insight-callout"><strong>Core strategic insight</strong><p>The strongest opportunity is not a feature race. It is owning a high-frequency workflow for a clearly defined customer segment, then expanding through trusted distribution.</p></div><h2>Market dynamics</h2><p>Demand is supported by growing pressure to improve productivity, the falling cost of intelligent automation and greater willingness to adopt specialized software. At the same time, switching friction and product convergence make durable differentiation difficult.</p><ul><li><strong>Demand:</strong> Teams are consolidating point tools around products that fit existing workflows.</li><li><strong>Supply:</strong> Technical barriers are falling, increasing competition and compressing feature advantages.</li><li><strong>Distribution:</strong> Partnerships and embedded routes to market are becoming strategic moats.</li></ul><h2>Competitive landscape</h2><p>Established platforms benefit from distribution and data access, while specialists win with sharper user experiences and category expertise. The market remains fragmented enough for focused entrants, particularly in regulated or underserved verticals.</p><h2>Recommended moves</h2><ol><li>Choose a narrow initial segment with urgent, repeated pain and a visible budget owner.</li><li>Build differentiation around workflow data and integration depth, not generic AI capability.</li><li>Validate willingness to pay through a design-partner cohort before broad market entry.</li><li>Track activation, retained weekly usage and time-to-value as early leading indicators.</li></ol><p class="source-note">Demo note: This report contains illustrative, synthetic findings to demonstrate the product workflow. It is not a substitute for live market research.</p>`;
}

function openReport(id) {
  currentReport = reports.find(r => r.id === id) || reports[0];
  document.querySelector('#reportDocument').innerHTML = buildReport(currentReport);
  showView('detail');
}

function toast(message) {
  const el = document.querySelector('#toast'); el.textContent = message; el.classList.add('show');
  clearTimeout(el._timer); el._timer = setTimeout(() => el.classList.remove('show'), 2200);
}

function startResearch(event) {
  event?.preventDefault();
  const query = document.querySelector('#researchQuery').value.trim();
  if (!query) { document.querySelector('#researchQuery').focus(); toast('Add a research question first'); return; }
  clearInterval(runTimer);
  const region = document.querySelector('#regionLabel').textContent;
  const depth = document.querySelector('#depthLabel').textContent;
  document.querySelector('#runTopic').textContent = query;
  document.querySelector('#runRegion').textContent = region; document.querySelector('#sideRegion').textContent = region;
  document.querySelector('#runDepth').textContent = depth; document.querySelector('#sideDepth').textContent = depth.replace(' depth','');
  const steps = [
    ['MM','Market Mapper','Sizing the market and identifying demand segments'],
    ['SS','Signal Scout','Scanning trends and emerging customer signals'],
    ['CA','Competitor Analyst','Mapping competitors and strategic whitespace'],
    ['IE','Insight Editor','Synthesizing findings into the final narrative']
  ];
  document.querySelector('#activityTimeline').innerHTML = steps.map((s,i) => `<div class="timeline-item ${i===0?'working':''}" data-step="${i}"><span class="timeline-avatar">${s[0]}</span><span class="timeline-copy"><strong>${s[1]}</strong><p>${s[2]}</p></span><span class="timeline-state">${i===0?'Working':'Queued'}</span></div>`).join('');
  document.querySelector('#progressBar').style.width = '3%'; document.querySelector('#progressPercent').textContent = '3%'; document.querySelector('#sourceCount').textContent = '0'; document.querySelector('#eta').textContent = '~24 sec';
  document.querySelector('#progressTitle').textContent = 'Market Mapper is analyzing the category...'; document.querySelector('#runStatusText').textContent = 'Crew is working';
  showView('run');
  let tick = 0;
  runTimer = setInterval(() => {
    tick++;
    const pct = Math.min(100, 3 + tick * 4);
    const active = Math.min(3, Math.floor(pct / 25));
    document.querySelector('#progressBar').style.width = `${pct}%`; document.querySelector('#progressPercent').textContent = `${pct}%`;
    document.querySelector('#sourceCount').textContent = Math.min(48, Math.floor(pct * .48)); document.querySelector('#eta').textContent = pct < 96 ? `~${Math.max(1,Math.ceil((100-pct)/4))} sec` : 'Finishing';
    document.querySelectorAll('.timeline-item').forEach((item,i) => { item.classList.toggle('done', i < active); item.classList.toggle('working', i === active && pct < 100); item.querySelector('.timeline-state').textContent = i < active ? 'Complete' : (i === active && pct < 100 ? 'Working' : 'Queued'); });
    const names = ['Market Mapper is analyzing the category...','Signal Scout is finding emerging signals...','Competitor Analyst is mapping the landscape...','Insight Editor is synthesizing the report...'];
    document.querySelector('#progressTitle').textContent = names[active];
    if (pct >= 100) finishResearch(query, region);
  }, 600);
}

function finishResearch(query, region) {
  clearInterval(runTimer);
  document.querySelectorAll('.timeline-item').forEach(item => { item.classList.add('done'); item.classList.remove('working'); item.querySelector('.timeline-state').textContent = 'Complete'; });
  document.querySelector('#progressTitle').textContent = 'Research report complete'; document.querySelector('#runStatusText').textContent = 'Research complete'; document.querySelector('#eta').textContent = 'Complete';
  currentReport = { id: Date.now(), title: query, topic: query, date: new Date().toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'}), sources:48, status:'Completed', summary:'A freshly synthesized market intelligence brief from your specialist research crew.', region };
  reports.unshift(currentReport); renderReports();
  setTimeout(() => { document.querySelector('#reportDocument').innerHTML = buildReport(currentReport); showView('detail'); toast('Your research report is ready'); }, 850);
}

function closeMobileNav() { document.querySelector('#sidebar').classList.remove('open'); document.querySelector('#mobileOverlay').classList.remove('show'); }

document.querySelectorAll('.nav-item').forEach(btn => btn.addEventListener('click', () => showView(btn.dataset.view)));
document.querySelectorAll('[data-view-jump]').forEach(btn => btn.addEventListener('click', () => showView(btn.dataset.viewJump)));
document.querySelectorAll('[data-new-research], #topNewResearch').forEach(btn => btn.addEventListener('click', () => { showView('dashboard'); setTimeout(()=>document.querySelector('#researchQuery').focus(),300); }));
document.querySelectorAll('.recent-item').forEach(btn => btn.addEventListener('click', () => { const r=reports.find(x=>x.topic===btn.dataset.topic); if(r) openReport(r.id); }));
document.querySelector('#researchForm').addEventListener('submit', startResearch);
document.querySelector('#researchQuery').addEventListener('keydown', e => { if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') startResearch(e); });
document.querySelector('#regionButton').addEventListener('click', () => { document.querySelector('#regionMenu').classList.toggle('show'); document.querySelector('#depthMenu').classList.remove('show'); });
document.querySelector('#depthButton').addEventListener('click', () => { document.querySelector('#depthMenu').classList.toggle('show'); document.querySelector('#regionMenu').classList.remove('show'); });
document.querySelectorAll('#regionMenu button').forEach(btn => btn.addEventListener('click',()=>{document.querySelector('#regionLabel').textContent=btn.dataset.value;btn.parentElement.classList.remove('show');}));
document.querySelectorAll('#depthMenu button').forEach(btn => btn.addEventListener('click',()=>{document.querySelector('#depthLabel').textContent=btn.dataset.value;btn.parentElement.classList.remove('show');}));
document.addEventListener('click', e => { if(!e.target.closest('.option-button')&&!e.target.closest('.select-menu')) document.querySelectorAll('.select-menu').forEach(m=>m.classList.remove('show')); });
document.querySelector('#reportSearch').addEventListener('input', e => { const q=e.target.value.toLowerCase(); renderReports(reports.filter(r=>(r.title+r.summary+r.region).toLowerCase().includes(q))); });
document.querySelector('#backToDashboard').addEventListener('click',()=>showView('dashboard')); document.querySelector('#backToReports').addEventListener('click',()=>showView('reports'));
document.querySelector('#copyReport').addEventListener('click', async()=>{ try { await navigator.clipboard.writeText(document.querySelector('#reportDocument').innerText); toast('Report copied to clipboard'); } catch { toast('Copy is unavailable in this browser'); } });
document.querySelector('#downloadReport').addEventListener('click',()=>{ const blob=new Blob([document.querySelector('#reportDocument').innerText],{type:'text/plain'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=`${currentReport.topic.replace(/[^a-z0-9]+/gi,'-').toLowerCase()}-report.txt`;a.click();URL.revokeObjectURL(a.href);toast('Report exported'); });
document.querySelector('#themeToggle').addEventListener('click',()=>{document.body.classList.toggle('dark');localStorage.setItem('research-theme',document.body.classList.contains('dark')?'dark':'light');});
document.querySelector('#mobileMenu').addEventListener('click',()=>{document.querySelector('#sidebar').classList.add('open');document.querySelector('#mobileOverlay').classList.add('show');});document.querySelector('#mobileOverlay').addEventListener('click',closeMobileNav);
if(localStorage.getItem('research-theme')==='dark') document.body.classList.add('dark');
renderReports(); renderAgents();
