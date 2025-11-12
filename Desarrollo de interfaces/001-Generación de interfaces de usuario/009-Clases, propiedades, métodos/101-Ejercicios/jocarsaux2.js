(function(global){
    const NAMESPACE = 'jux';
    const NS = (name) => `${NAMESPACE}-${name}`;

    function ensureStyles(){
      const id = `${NAMESPACE}-styles`; if (document.getElementById(id)) return;
      const css = `
:root { --jux-bg:#ffffff; --jux-text:#0f172a; --jux-muted:#475569; --jux-line:#e2e8f0; --jux-chip:#f8fafc; }
.${NS('root')} { font:14px/1.5 system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,Cantarell,Noto Sans,Arial; color:var(--jux-text); }
.${NS('wrap')} { max-width:1000px; margin:32px auto; padding:0 16px; }
.${NS('title')} { margin:0 0 6px; font-size:clamp(18px,3.5vw,26px); }
.${NS('subtitle')} { margin:0 0 14px; color:var(--jux-muted); }
.${NS('card')} { border:1px solid var(--jux-line); border-radius:12px; overflow:hidden; background:#fff }
.${NS('pad')} { padding:14px }
.${NS('toolbar')} { display:flex; gap:10px; align-items:center; justify-content:space-between }
.${NS('badge')} { display:inline-block; background:var(--jux-chip); padding:2px 8px; border:1px solid var(--jux-line); border-radius:999px; font-size:12px; color:var(--jux-muted) }
.${NS('search')} { display:flex; gap:8px; align-items:center }
.${NS('search')} input { border:1px solid var(--jux-line); border-radius:10px; padding:8px 10px; min-width:220px }
.${NS('count')} { font-size:12px; color:var(--jux-muted) }
.${NS('scroll')} { max-height:70vh; overflow:auto; border-top:1px solid var(--jux-line) }
.${NS('table')} { width:100%; border-collapse:separate; border-spacing:0; font-size:14px }
.${NS('thead')} th { position:sticky; top:0; background:linear-gradient(0deg,#f8fafc,#ffffff); border-bottom:1px solid var(--jux-line); text-align:left; font-weight:700; padding:10px 12px; white-space:nowrap }
.${NS('th-sortable')} { cursor:pointer; user-select:none }
.${NS('th-sortable')} .${NS('dir')} { margin-left:6px; font-size:11px; color:var(--jux-muted) }
.${NS('tbody')} td { border-bottom:1px solid var(--jux-line); padding:10px 12px; vertical-align:top }
.${NS('row-odd')} { background:#fafafa }
.${NS('form')} { padding:20px }
.${NS('field')} { margin-bottom:20px }
.${NS('label')} { display:block; margin-bottom:6px; font-weight:600; color:var(--jux-text); font-size:13px }
.${NS('input')}, .${NS('textarea')}, .${NS('select')} { width:100%; border:1px solid var(--jux-line); border-radius:8px; padding:10px 12px; font:inherit; color:var(--jux-text); transition:border-color 0.2s }
.${NS('input')}:focus, .${NS('textarea')}:focus, .${NS('select')}:focus { outline:none; border-color:#94a3b8 }
.${NS('textarea')} { min-height:100px; resize:vertical; font-family:inherit }
.${NS('select')} { cursor:pointer }
.${NS('hint')} { display:block; margin-top:4px; font-size:12px; color:var(--jux-muted) }
.${NS('btn-group')} { display:flex; gap:10px; margin-top:24px; padding-top:20px; border-top:1px solid var(--jux-line) }
.${NS('btn')} { padding:10px 20px; border:1px solid var(--jux-line); border-radius:8px; font:inherit; cursor:pointer; transition:all 0.2s }
.${NS('btn-primary')} { background:var(--jux-text); color:#fff; border-color:var(--jux-text) }
.${NS('btn-primary')}:hover { background:#1e293b }
.${NS('btn-secondary')} { background:#fff; color:var(--jux-text) }
.${NS('btn-secondary')}:hover { background:var(--jux-chip) }
`;
      const style = document.createElement('style');
      style.id = id; style.textContent = css; document.head.appendChild(style);
    }

    const isPlain = v => Object.prototype.toString.call(v) === '[object Object]';
    
    function flatten(value, prefix=''){
      const out = {}; const stack = [{v:value,p:prefix}];
      while (stack.length){
        const {v,p} = stack.pop();
        if (Array.isArray(v)){
          const primitives = v.every(x => !isPlain(x) && !Array.isArray(x));
          if (primitives){ out[p||'value'] = v.join(', '); }
          else {
            out[p||'value'] = v.map(x => isPlain(x) ? JSON.stringify(x) : String(x)).join(', ');
          }
        } else if (isPlain(v)){
          const ks = Object.keys(v); 
          if (!ks.length){ out[p||'value'] = '{}'; continue; }
          ks.forEach(k=>{
            const nv=v[k]; 
            const np = p ? `${p}.${k}` : k;
            if (isPlain(nv)) {
              stack.push({v:nv,p:np});
            } else if (Array.isArray(nv)) {
              const primitives = nv.every(x => !isPlain(x) && !Array.isArray(x));
              out[np] = primitives ? nv.join(', ') : nv.map(x => isPlain(x) ? JSON.stringify(x) : String(x)).join(', ');
            } else {
              out[np] = nv==null ? '' : String(nv);
            }
          });
        } else { 
          out[p||'value'] = v==null ? '' : String(v); 
        }
      }
      return out;
    }
    
    function normalizeTop(json){ 
      if (Array.isArray(json)) return json; 
      if (isPlain(json)){ 
        const key=Object.keys(json).find(k=>Array.isArray(json[k])); 
        return key?json[key]:[json]; 
      } 
      return [json]; 
    }
    
    const collectColumns = rows => Array.from(rows.reduce((s,r)=>{ Object.keys(r).forEach(k=>s.add(k)); return s; }, new Set()));

    // Analyze field data to determine best input type
    function analyzeField(values){
      const nonEmpty = values.filter(v => v != null && v !== '');
      if (!nonEmpty.length) return { type: 'text' };

      // Check if all numeric
      const allNumeric = nonEmpty.every(v => !isNaN(Number(v)));
      if (allNumeric) return { type: 'number' };

      // Convert to strings
      const strings = nonEmpty.map(v => String(v));
      
      // Check for repetition (select dropdown)
      const unique = [...new Set(strings)];
      const repetitionRatio = unique.length / strings.length;
      if (repetitionRatio < 0.5 && unique.length > 1 && unique.length < 20) {
        return { type: 'select', options: unique.sort() };
      }

      // Check average length
      const avgLength = strings.reduce((sum, s) => sum + s.length, 0) / strings.length;
      if (avgLength > 80) {
        return { type: 'textarea' };
      }

      return { type: 'text' };
    }

    class JocarsaUX {
      constructor(){ ensureStyles(); this.state={ columns:[], rows:[], view:[], sort:{key:null, dir:1}, query:'' }; this._els={ host:null, table:null, thead:null, tbody:null, search:null, count:null }; }

      tableRenderer({ target, data, flattenObjects=true, title='jocarsa|ux', subtitle='Table renderer (search + sort)' }={}){
        const host = (typeof target==='string') ? document.querySelector(target) : target; if (!host) throw new Error('Target not found');
        this._els.host = host;
        host.classList.add(NS('root'));
        host.innerHTML = '';

        const wrap = el('div', NS('wrap'));
        const h1 = el('h1', NS('title'), title);
        const p = el('p', NS('subtitle'), subtitle);
        const card = el('div', NS('card'));
        const pad = el('div', NS('pad'));
        const toolbar = el('div', NS('toolbar'));
        const badge = el('span', NS('badge'), 'Table demo');
        const searchBox = el('div', NS('search'));
        const label = el('label', null, 'Search'); label.htmlFor = NS('search-input');
        const input = el('input'); input.id = NS('search-input');
        const count = el('span', NS('count'));
        searchBox.append(label, input, count);
        toolbar.append(badge, searchBox);
        pad.append(toolbar);

        const scroll = el('div', NS('scroll'));
        const table = el('table', NS('table'));
        const thead = document.createElement('thead'); thead.className = NS('thead');
        const tbody = document.createElement('tbody'); tbody.className = NS('tbody');
        table.append(thead, tbody);
        scroll.append(table);
        card.append(pad, scroll);
        wrap.append(h1, p, card);
        host.append(wrap);

        this._els = { host, table, thead, tbody, search: input, count };

        const arr = normalizeTop(data);
        const flat = flattenObjects ? arr.map(obj => flatten(obj)) : arr;
        this.state.columns = collectColumns(flat);
        this.state.rows = flat; 
        this.state.view = flat.slice(); 
        this.state.sort = {key:null, dir:1}; 
        this.state.query='';

        input.value = '';
        input.oninput = () => this.setFilter(input.value);

        this._renderHead();
        this._renderBody();
        return this;
      }

      formRenderer({ target, data, flattenObjects=true, title='jocarsa|ux', subtitle='Form renderer (smart input types)', onSubmit=null, onReset=null }={}){
        const host = (typeof target==='string') ? document.querySelector(target) : target; if (!host) throw new Error('Target not found');
        this._els.host = host;
        host.classList.add(NS('root'));
        host.innerHTML = '';

        const wrap = el('div', NS('wrap'));
        const h1 = el('h1', NS('title'), title);
        const p = el('p', NS('subtitle'), subtitle);
        const card = el('div', NS('card'));

        const arr = normalizeTop(data);
        const flat = flattenObjects ? arr.map(obj => flatten(obj)) : arr;
        const columns = collectColumns(flat);

        // Analyze each field
        const fieldTypes = {};
        columns.forEach(col => {
          const values = flat.map(row => row[col]);
          fieldTypes[col] = analyzeField(values);
        });

        // Create form
        const form = el('form', NS('form'));
        form.onsubmit = (e) => {
          e.preventDefault();
          const formData = {};
          columns.forEach(col => {
            const input = form.elements[col];
            formData[col] = input.value;
          });
          if (onSubmit) onSubmit(formData);
        };

        columns.forEach(col => {
          const fieldDiv = el('div', NS('field'));
          const label = el('label', NS('label'), col);
          label.htmlFor = `${NAMESPACE}-${col}`;

          const fieldInfo = fieldTypes[col];
          let input;

          if (fieldInfo.type === 'select') {
            input = document.createElement('select');
            input.className = NS('select');
            const emptyOption = document.createElement('option');
            emptyOption.value = '';
            emptyOption.textContent = '-- Select --';
            input.appendChild(emptyOption);
            fieldInfo.options.forEach(opt => {
              const option = document.createElement('option');
              option.value = opt;
              option.textContent = opt;
              input.appendChild(option);
            });
            const hint = el('span', NS('hint'), `${fieldInfo.options.length} options available`);
            fieldDiv.append(label, input, hint);
          } else if (fieldInfo.type === 'textarea') {
            input = document.createElement('textarea');
            input.className = NS('textarea');
            const hint = el('span', NS('hint'), 'Long text field');
            fieldDiv.append(label, input, hint);
          } else if (fieldInfo.type === 'number') {
            input = document.createElement('input');
            input.type = 'number';
            input.className = NS('input');
            input.step = 'any';
            const hint = el('span', NS('hint'), 'Numeric field');
            fieldDiv.append(label, input, hint);
          } else {
            input = document.createElement('input');
            input.type = 'text';
            input.className = NS('input');
            const hint = el('span', NS('hint'), 'Text field');
            fieldDiv.append(label, input, hint);
          }

          input.id = `${NAMESPACE}-${col}`;
          input.name = col;
          form.appendChild(fieldDiv);
        });

        // Button group
        const btnGroup = el('div', NS('btn-group'));
        const submitBtn = el('button', `${NS('btn')} ${NS('btn-primary')}`, 'Submit');
        submitBtn.type = 'submit';
        const resetBtn = el('button', `${NS('btn')} ${NS('btn-secondary')}`, 'Reset');
        resetBtn.type = 'button';
        resetBtn.onclick = () => {
          form.reset();
          if (onReset) onReset();
        };
        btnGroup.append(submitBtn, resetBtn);
        form.appendChild(btnGroup);

        card.appendChild(form);
        wrap.append(h1, p, card);
        host.append(wrap);

        return this;
      }

      setFilter(query=''){
        this.state.query = String(query).toLowerCase();
        const { rows, columns } = this.state;
        if (!this.state.query) this.state.view = rows.slice();
        else this.state.view = rows.filter(r=>columns.some(k=>{ const v=r[k]; return v && String(v).toLowerCase().includes(this.state.query); }));
        this._renderBody();
        return this;
      }

      sortBy(key, dir){
        if (!key) return this;
        const s = this.state;
        if (dir == null){ if (s.sort.key === key) s.sort.dir *= -1; else { s.sort.key = key; s.sort.dir = 1; } }
        else { s.sort.key = key; s.sort.dir = dir >= 0 ? 1 : -1; }
        const d = s.sort.dir; const k = s.sort.key;
        s.view.sort((a,b)=>{
          const va=a[k] ?? '', vb=b[k] ?? '';
          const na=Number(va), nb=Number(vb);
          const bothNum = !isNaN(na) && !isNaN(nb);
          if (bothNum) return (na-nb)*d;
          return String(va).localeCompare(String(vb), undefined, {numeric:true, sensitivity:'base'})*d;
        });
        this._renderHead();
        this._renderBody();
        return this;
      }

      _renderHead(){
        const { columns, sort } = this.state; const thead = this._els.thead;
        thead.innerHTML = '';
        const tr = document.createElement('tr');
        columns.forEach(c=>{
          const th = document.createElement('th');
          th.className = `${NS('th-sortable')}`; th.title = `Sort by ${c}`; th.textContent = c;
          const dir = el('span', NS('dir'), sort.key===c ? (sort.dir===1 ? '▲' : '▼') : '');
          th.append(dir);
          th.addEventListener('click', ()=>this.sortBy(c));
          tr.append(th);
        });
        thead.append(tr);
      }

      _renderBody(){
        const { columns, view } = this.state; const tbody = this._els.tbody;
        tbody.innerHTML = '';
        const frag = document.createDocumentFragment();
        view.forEach((r, idx)=>{
          const tr = document.createElement('tr');
          if (idx % 2 === 0) tr.classList.add(NS('row-odd'));
          columns.forEach(c=>{
            const td = document.createElement('td');
            td.textContent = r[c] ?? '';
            tr.append(td);
          });
          frag.append(tr);
        });
        tbody.append(frag);
        if (this._els.count) this._els.count.textContent = `${view.length} row(s)`;
      }
    }

    function el(tag, className, text){ const x=document.createElement(tag); if (className) x.className=className; if (text!=null) x.textContent=text; return x; }

    global.JocarsaUX = JocarsaUX;
    global['jocarsa|ux'] = { UX: JocarsaUX };

  })(window);
