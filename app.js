const chapters = [
  {id:'motion', level:'Seconde', category:'Physique', title:'Mouvement et vitesse', context:'Transport et trajets', description:'Décrire un mouvement, calculer une vitesse moyenne et lire un graphique de position.', tip:'v = d / Δt. Pensez à convertir les unités avant de calculer : 1 m·s⁻¹ = 3,6 km·h⁻¹.'},
  {id:'mixtures', level:'Seconde', category:'Chimie', title:'Mélanges et solutions', context:'Eau et salinité', description:'Distinguer mélange homogène et hétérogène, puis utiliser concentration massique et molaire.', tip:'Une eau claire n’est pas forcément pure : des sels dissous peuvent être invisibles.'},
  {id:'electricity', level:'Première', category:'Physique', title:'Énergie électrique', context:'Lampe et panneau solaire', description:'Relier tension, intensité, puissance et énergie dans un circuit électrique.', tip:'P = U × I et E = P × Δt. Le watt mesure une puissance ; le wattheure mesure une énergie.'},
  {id:'acids', level:'Première', category:'Chimie', title:'Acides, bases et pH', context:'Solutions du quotidien', description:'Lire une valeur de pH, reconnaître une solution acide ou basique et raisonner sur une dilution.', tip:'À 25 °C, pH < 7 indique une solution acide, pH = 7 neutre et pH > 7 basique.'},
  {id:'rlc', level:'Terminale', category:'Physique', title:'Circuit RLC et résonance', context:'Radio et filtres', description:'Étudier le régime transitoire et la résonance en intensité d’un circuit RLC série.', tip:'Pour un circuit RLC série idéal, f₀ = 1 / (2π√(LC)). Augmenter la résistance élargit le pic.'},
  {id:'titration', level:'Terminale', category:'Chimie', title:'Dosage et titrage', context:'Contrôle d’une solution', description:'Comprendre l’équivalence d’un titrage et exploiter une relation stœchiométrique.', tip:'À l’équivalence, les réactifs ont été introduits dans les proportions de l’équation-bilan.'},
];

const quiz = [
  {q:'Quelle grandeur se mesure en wattheure (Wh) ?', options:['La puissance','L’énergie','La tension'], answer:1, why:'Le wattheure est une unité d’énergie.'},
  {q:'Quelle est l’unité SI de la vitesse ?', options:['m·s⁻¹','m·s⁻²','kg·m·s⁻¹'], answer:0, why:'La vitesse est une distance divisée par un temps : m·s⁻¹.'},
  {q:'Une solution de pH 3 est généralement…', options:['Acide','Neutre','Basique'], answer:0, why:'À 25 °C, une solution de pH inférieur à 7 est acide.'},
  {q:'Dans un circuit RLC série, la fréquence propre dépend de…', options:['L et C','R seulement','La tension seulement'], answer:0, why:'f₀ = 1 / (2π√(LC)).'},
  {q:'Lors d’une dilution, quelle relation est conservée ?', options:['C₁V₁ = C₂V₂','C₁ + V₁ = C₂ + V₂','C₁/V₁ = C₂/V₂'], answer:0, why:'La quantité de soluté prélevée reste la même avant et après dilution.'},
];

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];
const readStore = (key, fallback) => { try { return JSON.parse(localStorage.getItem(key)) ?? fallback; } catch { return fallback; } };
const writeStore = (key, value) => { try { localStorage.setItem(key, JSON.stringify(value)); } catch { /* Le contenu reste utilisable si le stockage est désactivé. */ } };

function renderChapters(filter='Tous') {
  const grid = $('#chapter-grid');
  const completed = readStore('sunu-completed', []);
  const visible = chapters.filter(ch => filter === 'Tous' || ch.level === filter);
  grid.innerHTML = visible.map((ch, i) => `
    <article class="chapter-card">
      <div class="chapter-meta"><span class="chapter-number">PARCOURS 0${chapters.indexOf(ch)+1} · ${ch.category.toUpperCase()}</span><span class="chapter-level">${ch.level}</span></div>
      <h3>${ch.title}</h3><p>${ch.description}</p>
      <div class="chapter-bottom"><span class="chapter-context">${ch.context}</span><button class="chapter-open ${completed.includes(ch.id)?'done':''}" data-chapter="${ch.id}">${completed.includes(ch.id)?'Révisé':'Découvrir'} <span aria-hidden="true">→</span></button></div>
    </article>`).join('');
  $$('.chapter-open').forEach(button => button.addEventListener('click', () => openChapter(button.dataset.chapter)));
}

function openChapter(id) {
  const ch = chapters.find(item => item.id === id); if (!ch) return;
  $('#dialog-level').textContent = `${ch.level} · ${ch.category}`;
  $('#dialog-title').textContent = ch.title;
  $('#dialog-description').textContent = `${ch.description} Exemple de contexte : ${ch.context.toLowerCase()}.`;
  $('#dialog-tip').textContent = ch.tip;
  $('#mark-complete').dataset.chapter = ch.id;
  $('#chapter-dialog').showModal();
}

function calculateSolar() {
  const power = Number($('#solar-power').value), hours = Number($('#solar-hours').value), efficiency = Number($('#solar-efficiency').value);
  $('#solar-efficiency-value').textContent = `${efficiency} %`;
  const energy = Math.max(0, power * hours * efficiency / 100);
  $('#solar-result').textContent = `${new Intl.NumberFormat('fr-FR',{maximumFractionDigits:0}).format(energy)} Wh`;
}

function calculateRLC() {
  const L = Number($('#rlc-l').value) * 1e-3, C = Number($('#rlc-c').value) * 1e-9, R = Number($('#rlc-r').value);
  const f0 = L > 0 && C > 0 ? 1 / (2 * Math.PI * Math.sqrt(L*C)) : 0;
  const q = L > 0 && C > 0 && R > 0 ? Math.sqrt(L/C) / R : 0;
  $('#rlc-result').textContent = `${new Intl.NumberFormat('fr-FR',{maximumFractionDigits:0}).format(f0)} Hz`;
  $('#rlc-q-result').textContent = new Intl.NumberFormat('fr-FR',{maximumFractionDigits:2}).format(q);
}

function calculateDilution() {
  const c1 = Number($('#dilution-c1').value), v1 = Number($('#dilution-v1').value), v2 = Number($('#dilution-v2').value);
  const c2 = v2 > 0 ? c1*v1/v2 : 0;
  $('#dilution-result').textContent = `${new Intl.NumberFormat('fr-FR',{maximumSignificantDigits:4}).format(c2)} mol·L⁻¹`;
}

function renderQuiz() {
  $('#quiz-questions').innerHTML = quiz.map((item,i) => `<fieldset class="quiz-question"><legend>${i+1}. ${item.q}</legend><div class="quiz-options">${item.options.map((option,j)=>`<label class="quiz-option"><input type="radio" name="q${i}" value="${j}" ${j===0?'required':''}> ${option}</label>`).join('')}</div></fieldset>`).join('');
  const best = readStore('sunu-best-score', null); $('#best-score').textContent = best === null ? '—' : `${best}/5`;
}

$('#level-filter').addEventListener('change', event => renderChapters(event.target.value));
$('#solar-power').addEventListener('input', calculateSolar); $('#solar-hours').addEventListener('input', calculateSolar); $('#solar-efficiency').addEventListener('input', calculateSolar);
['#rlc-l','#rlc-c','#rlc-r'].forEach(selector => $(selector).addEventListener('input', calculateRLC));
['#dilution-c1','#dilution-v1','#dilution-v2'].forEach(selector => $(selector).addEventListener('input', calculateDilution));
$('#dialog-close').addEventListener('click', () => $('#chapter-dialog').close());
$('#chapter-dialog').addEventListener('click', event => { if (event.target === $('#chapter-dialog')) $('#chapter-dialog').close(); });
$('#mark-complete').addEventListener('click', event => {
  const done = readStore('sunu-completed', []); if (!done.includes(event.currentTarget.dataset.chapter)) done.push(event.currentTarget.dataset.chapter);
  writeStore('sunu-completed', done); renderChapters($('#level-filter').value); $('#chapter-dialog').close();
});
$('#quiz-form').addEventListener('submit', event => {
  event.preventDefault(); const data = new FormData(event.currentTarget);
  if (quiz.some((_,i)=>data.get(`q${i}`)===null)) { $('#quiz-result').textContent='Répondez aux cinq questions pour voir le corrigé.'; return; }
  let score=0; const feedback=[];
  quiz.forEach((item,i)=>{ const correct=Number(data.get(`q${i}`))===item.answer; if(correct) score++; feedback.push(`${correct?'✓':'✗'} ${item.why}`); });
  const best=readStore('sunu-best-score',0); if(score>best) writeStore('sunu-best-score',score);
  $('#best-score').textContent=`${Math.max(score,best)}/5`; $('#quiz-result').textContent=`Score : ${score}/5 — ${feedback.join(' ')}`;
});

let installPrompt;
window.addEventListener('beforeinstallprompt', event => { event.preventDefault(); installPrompt=event; $('#install-button').hidden=false; });
$('#install-button').addEventListener('click', async () => { if(!installPrompt)return; installPrompt.prompt(); await installPrompt.userChoice; installPrompt=null; $('#install-button').hidden=true; });
function updateConnection() {
  const badge=$('#connection-state'); badge.classList.toggle('online',navigator.onLine); badge.classList.toggle('offline',!navigator.onLine);
  badge.lastChild.textContent=navigator.onLine?' En ligne':' Hors ligne';
}
window.addEventListener('online',updateConnection); window.addEventListener('offline',updateConnection);
renderChapters(); renderQuiz(); calculateSolar(); calculateRLC(); calculateDilution(); updateConnection();

if ('serviceWorker' in navigator) {
  window.addEventListener('load', async () => {
    try { await navigator.serviceWorker.register('./sw.js'); $('#offline-ready').textContent='Prêt hors ligne'; $('#offline-ready').classList.add('ready'); }
    catch { $('#offline-ready').textContent='Mode hors ligne indisponible'; }
  });
} else { $('#offline-ready').textContent='Navigateur sans mode hors ligne'; }
