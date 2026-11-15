// Ejecuta el motor de InformAMPA en Node (sin navegador) y guarda los informes
// HTML de los casos simulados. Uso: node informes_node.js <informampa.html> <casos.json> <dir_salida>
const fs = require('fs'), vm = require('vm'), path = require('path');
const [html, casosPath, outDir] = process.argv.slice(2);
const src = [...fs.readFileSync(html, 'utf8').matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]).join('\n');
const el = () => ({ innerHTML: '', style: {}, value: '', focus() {}, setSelectionRange() {}, addEventListener() {} });
const ctx = {
  console, Math, JSON, Date, Number, String, Array, Object, Set, isNaN, setTimeout,
  localStorage: { getItem: () => null, setItem() {} },
  document: { getElementById: el, querySelector: el, activeElement: null, addEventListener() {}, createElement: el, body: el() },
  window: {}, XLSX: {}, FileReader: function () {}, alert() {},
};
ctx.window = ctx;
vm.createContext(ctx);
vm.runInContext(src + '\n;globalThis.__api={calcStats,getStatus,buildReport,APP,ST};', ctx);
const { calcStats, getStatus, buildReport, APP, ST } = ctx.__api;
const casos = JSON.parse(fs.readFileSync(casosPath, 'utf8'));
const res = {};
for (const c of casos) {
  let meas = c.meas.map((m, i) => ({ id: i + 1, ...m }));
  if (c.excluir_dia1) { const d1 = meas.map(m => m.date).sort()[0]; meas = meas.filter(m => m.date !== d1); }
  const st = calcStats(meas), status = getStatus(st, c.clinic[0], c.clinic[1]);
  const info = { ...ST.info, device: 'Tensiómetro validado (datos simulados)', clinicSys: c.clinic[0], clinicDia: c.clinic[1] };
  fs.writeFileSync(path.join(outDir, `informe_${c.id}.html`), buildReport(meas, info, st, status, [], []));
  res[c.id] = { version: APP.version, sesiones: st.totalSessions, dias: st.validDays, global: st.global, manana: st.mornG, tarde: st.aftG,
    de_pas: st.pasSd, de_pad: st.padSd, elevadas: st.elevCount, efecto_alerta: st.avgAlert, estado: status.badge };
}
fs.writeFileSync(path.join(outDir, 'resultados_herramienta.json'), JSON.stringify(res, null, 1));
console.log(JSON.stringify(res));
