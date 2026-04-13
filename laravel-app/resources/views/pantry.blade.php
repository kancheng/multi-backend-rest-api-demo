<!doctype html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Pantry · Laravel</title>
    <style>
        :root { color-scheme: light; }
        * { box-sizing: border-box; }
        body {
            margin: 0;
            font-family: Arial, "Microsoft JhengHei", sans-serif;
            background: #f3f6fb;
            color: #1a1a1a;
            line-height: 1.5;
        }
        .wrap { max-width: 960px; margin: 0 auto; padding: 24px 16px 48px; }
        .badge {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 999px;
            background: #e8f0ff;
            color: #1f4db8;
            font-size: 0.85rem;
            font-weight: 700;
        }
        h1 { margin: 10px 0 6px; font-size: 1.5rem; }
        .sub { color: #5a6570; font-size: 0.95rem; margin-bottom: 20px; }
        .card {
            background: #fff;
            border-radius: 14px;
            box-shadow: 0 4px 18px rgba(0,0,0,.06);
            padding: 20px;
            margin-bottom: 18px;
        }
        .card h2 { margin: 0 0 14px; font-size: 1.05rem; }
        label { display: block; font-size: 0.8rem; color: #5a6570; margin-bottom: 4px; }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
            gap: 12px;
        }
        input, button {
            font: inherit;
            border-radius: 8px;
            border: 1px solid #d0d7e2;
            padding: 8px 10px;
        }
        input { width: 100%; }
        button {
            cursor: pointer;
            border: none;
            font-weight: 600;
        }
        .btn-primary { background: #1f4db8; color: #fff; }
        .btn-secondary { background: #eef1f6; color: #1a1a1a; }
        .btn-danger { background: #c42b2b; color: #fff; }
        .btn-sm { padding: 6px 10px; font-size: 0.85rem; border-radius: 6px; }
        .form-actions { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 14px; }
        .msg { margin-top: 10px; font-size: 0.9rem; min-height: 1.2em; }
        .msg.err { color: #b00020; }
        .msg.ok { color: #0d6e3c; }
        table { width: 100%; border-collapse: collapse; font-size: 0.9rem; }
        th, td { text-align: left; padding: 10px 8px; border-bottom: 1px solid #e8ecf4; vertical-align: top; }
        th { color: #5a6570; font-weight: 600; font-size: 0.78rem; text-transform: uppercase; letter-spacing: .02em; }
        .num { text-align: right; font-variant-numeric: tabular-nums; }
        .row-actions { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }
        .use-row { display: flex; gap: 6px; align-items: center; margin-top: 6px; }
        .use-row input { width: 72px; padding: 4px 6px; }
        details.usage { margin-top: 8px; font-size: 0.85rem; color: #5a6570; }
        details.usage pre { margin: 6px 0 0; white-space: pre-wrap; word-break: break-all; background: #f6f8fc; padding: 8px; border-radius: 6px; }
        @@media (max-width: 640px) {
            th:nth-child(3), td:nth-child(3) { display: none; }
        }
    </style>
</head>
<body>
    <div class="wrap">
        <span class="badge">Laravel · Smart Pantry</span>
        <h1>智慧食材庫</h1>
        <p class="sub">資料來自本機 REST API（<code>/api/ingredients</code>），可在此查詢、新增、修改、刪除與記錄使用。</p>

        <section class="card">
            <h2 id="form-title">新增食材</h2>
            <form id="ing-form">
                <div class="grid">
                    <div><label for="f-name">名稱</label><input id="f-name" name="name" required></div>
                    <div><label for="f-qty">數量</label><input id="f-qty" name="quantity" type="number" step="any" required></div>
                    <div><label for="f-unit">單位</label><input id="f-unit" name="unit" required placeholder="bottle"></div>
                    <div><label for="f-exp">到期日</label><input id="f-exp" name="expiry_date" type="date" required></div>
                </div>
                <div class="form-actions">
                    <button type="submit" class="btn-primary" id="btn-submit">新增</button>
                    <button type="button" class="btn-secondary" id="btn-cancel" hidden>取消編輯</button>
                </div>
            </form>
            <div class="msg" id="form-msg" aria-live="polite"></div>
        </section>

        <section class="card">
            <h2>食材列表</h2>
            <div class="msg err" id="list-err"></div>
            <div style="overflow-x: auto;">
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>名稱</th>
                            <th>到期日</th>
                            <th class="num">數量</th>
                            <th>操作</th>
                        </tr>
                    </thead>
                    <tbody id="tbody"></tbody>
                </table>
            </div>
            <p id="empty-hint" class="sub" style="display:none;">尚無資料，請先新增食材。</p>
        </section>
    </div>

    <script>
(function () {
    const tbody = document.getElementById('tbody');
    const form = document.getElementById('ing-form');
    const formMsg = document.getElementById('form-msg');
    const listErr = document.getElementById('list-err');
    const emptyHint = document.getElementById('empty-hint');
    const formTitle = document.getElementById('form-title');
    const btnSubmit = document.getElementById('btn-submit');
    const btnCancel = document.getElementById('btn-cancel');
    let editingId = null;

    async function api(path, opts = {}) {
        const res = await fetch(path, {
            ...opts,
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
                ...opts.headers,
            },
            body: opts.body != null && typeof opts.body === 'object' ? JSON.stringify(opts.body) : opts.body,
        });
        const text = await res.text();
        let data = null;
        if (text) {
            try { data = JSON.parse(text); } catch { data = text; }
        }
        if (!res.ok) {
            let msg = 'HTTP ' + res.status;
            if (data && typeof data === 'object') {
                if (data.error) msg = String(data.error);
                else if (data.message) msg = String(data.message);
                else if (data.errors && typeof data.errors === 'object') {
                    const parts = [];
                    for (const k of Object.keys(data.errors)) {
                        const v = data.errors[k];
                        if (Array.isArray(v)) parts.push(...v.map(String));
                        else if (v != null) parts.push(String(v));
                    }
                    if (parts.length) msg = parts.join(' ');
                }
            }
            throw new Error(msg);
        }
        return data;
    }

    function setFormMsg(text, ok) {
        formMsg.textContent = text || '';
        formMsg.className = 'msg' + (text ? (ok ? ' ok' : ' err') : '');
    }

    function resetForm() {
        editingId = null;
        form.reset();
        formTitle.textContent = '新增食材';
        btnSubmit.textContent = '新增';
        btnCancel.hidden = true;
        setFormMsg('');
    }


    function formatDateOnly(v) {
        const s = String(v);
        return s.length >= 10 ? s.slice(0, 10) : s;
    }

    function renderRow(item) {
        const tr = document.createElement('tr');
        tr.dataset.id = String(item.id);
        tr.innerHTML =
            '<td>' + item.id + '</td>' +
            '<td><strong>' + escapeHtml(item.name) + '</strong><div class="sub" style="margin:4px 0 0;font-size:.8rem;">' + escapeHtml(item.unit) + '</div></td>' +
            '<td>' + escapeHtml(formatDateOnly(item.expiry_date)) + '</td>' +
            '<td class="num">' + escapeHtml(String(item.quantity)) + '</td>' +
            '<td></td>';
        const td = tr.querySelector('td:last-child');
        const wrap = document.createElement('div');
        wrap.className = 'row-actions';
        const bEdit = document.createElement('button');
        bEdit.type = 'button'; bEdit.className = 'btn-secondary btn-sm'; bEdit.textContent = '編輯';
        bEdit.onclick = () => startEdit(item);
        const bDel = document.createElement('button');
        bDel.type = 'button'; bDel.className = 'btn-danger btn-sm'; bDel.textContent = '刪除';
        bDel.onclick = () => removeItem(item.id);
        wrap.appendChild(bEdit);
        wrap.appendChild(bDel);
        td.appendChild(wrap);

        const useDiv = document.createElement('div');
        useDiv.className = 'use-row';
        const uIn = document.createElement('input');
        uIn.type = 'number'; uIn.step = 'any'; uIn.min = '0'; uIn.placeholder = '用量';
        uIn.value = '1';
        const bUse = document.createElement('button');
        bUse.type = 'button'; bUse.className = 'btn-primary btn-sm'; bUse.textContent = '使用';
        bUse.onclick = async () => {
            try {
                await api('/api/ingredients/' + item.id + '/use', { method: 'POST', body: { used_quantity: Number(uIn.value) } });
                setFormMsg('已記錄使用', true);
                await loadList();
            } catch (e) {
                setFormMsg(e.message, false);
            }
        };
        useDiv.appendChild(uIn);
        useDiv.appendChild(bUse);
        td.appendChild(useDiv);

        const det = document.createElement('details');
        det.className = 'usage';
        const sum = document.createElement('summary');
        sum.textContent = '查看使用紀錄';
        det.appendChild(sum);
        const pre = document.createElement('pre');
        pre.textContent = '（點開載入）';
        det.appendChild(pre);
        det.ontoggle = async () => {
            if (!det.open) return;
            try {
                const logs = await api('/api/ingredients/' + item.id + '/usage');
                const arr = Array.isArray(logs) ? logs : [];
                pre.textContent = arr.length ? JSON.stringify(arr, null, 2) : '尚無紀錄';
            } catch (e) {
                pre.textContent = '載入失敗：' + e.message;
            }
        };
        td.appendChild(det);

        return tr;
    }

    function escapeHtml(s) {
        return String(s)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    }

    async function loadList() {
        listErr.textContent = '';
        try {
            const items = await api('/api/ingredients');
            const list = Array.isArray(items) ? items : [];
            tbody.innerHTML = '';
            emptyHint.style.display = list.length ? 'none' : 'block';
            list.forEach((item) => tbody.appendChild(renderRow(item)));
        } catch (e) {
            listErr.textContent = '無法載入列表：' + e.message;
            tbody.innerHTML = '';
            emptyHint.style.display = 'none';
        }
    }

    function startEdit(item) {
        editingId = item.id;
        document.getElementById('f-name').value = item.name;
        document.getElementById('f-qty').value = item.quantity;
        document.getElementById('f-unit').value = item.unit;
        document.getElementById('f-exp').value = formatDateOnly(item.expiry_date);
        formTitle.textContent = '編輯食材 #' + item.id;
        btnSubmit.textContent = '儲存變更';
        btnCancel.hidden = false;
        setFormMsg('');
        form.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    async function removeItem(id) {
        if (!confirm('確定刪除 ID ' + id + '？')) return;
        try {
            await api('/api/ingredients/' + id, { method: 'DELETE' });
            if (editingId === id) resetForm();
            await loadList();
            setFormMsg('已刪除', true);
        } catch (e) {
            setFormMsg(e.message, false);
        }
    }

    form.addEventListener('submit', async (ev) => {
        ev.preventDefault();
        setFormMsg('');
        const body = {
            name: document.getElementById('f-name').value.trim(),
            quantity: Number(document.getElementById('f-qty').value),
            unit: document.getElementById('f-unit').value.trim(),
            expiry_date: document.getElementById('f-exp').value,
        };
        try {
            if (editingId == null) {
                await api('/api/ingredients', { method: 'POST', body });
                setFormMsg('已新增', true);
            } else {
                await api('/api/ingredients/' + editingId, { method: 'PUT', body });
                setFormMsg('已更新', true);
            }
            resetForm();
            await loadList();
        } catch (e) {
            setFormMsg(e.message, false);
        }
    });

    btnCancel.addEventListener('click', resetForm);

    loadList();
})();
    </script>
</body>
</html>
