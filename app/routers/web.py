from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["Web UI"])


@router.get("/", response_class=HTMLResponse)
def index_page():
    """
    Serve the interactive web interface.
    """
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AutoEDA & ML Report Generator</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
        <style>
            :root {
                --primary: #6366f1;
                --primary-hover: #4f46e5;
                --accent: #06b6d4;
                --bg: #090d16;
                --card-bg: rgba(22, 27, 44, 0.7);
                --card-border: rgba(255, 255, 255, 0.08);
                --text: #f8fafc;
                --text-muted: #94a3b8;
                --success: #10b981;
            }
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body {
                font-family: 'Outfit', sans-serif;
                background-color: var(--bg);
                background-image: radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15) 0px, transparent 50%),
                                  radial-gradient(at 100% 100%, rgba(6, 182, 212, 0.15) 0px, transparent 50%);
                color: var(--text);
                min-height: 100vh;
                padding: 40px 20px;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            .container {
                width: 100%;
                max-width: 900px;
            }
            header {
                text-align: center;
                margin-bottom: 35px;
            }
            .badge {
                display: inline-block;
                padding: 6px 14px;
                background: rgba(99, 102, 241, 0.15);
                border: 1px solid rgba(99, 102, 241, 0.3);
                border-radius: 50px;
                color: #a5b4fc;
                font-size: 0.85rem;
                font-weight: 600;
                margin-bottom: 15px;
                letter-spacing: 0.5px;
            }
            h1 {
                font-size: 2.8rem;
                font-weight: 800;
                background: linear-gradient(135deg, #ffffff 30%, #94a3b8 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 12px;
            }
            p.subtitle {
                color: var(--text-muted);
                font-size: 1.15rem;
            }
            .card {
                background: var(--card-bg);
                backdrop-filter: blur(16px);
                border: 1px solid var(--card-border);
                border-radius: 20px;
                padding: 35px;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
                margin-bottom: 30px;
            }
            .drop-zone {
                border: 2px dashed rgba(99, 102, 241, 0.4);
                border-radius: 14px;
                padding: 40px 20px;
                text-align: center;
                cursor: pointer;
                transition: all 0.3s ease;
                background: rgba(99, 102, 241, 0.03);
            }
            .drop-zone:hover, .drop-zone.dragover {
                border-color: var(--primary);
                background: rgba(99, 102, 241, 0.08);
                transform: scale(1.01);
            }
            .drop-zone svg {
                width: 48px;
                height: 48px;
                fill: var(--accent);
                margin-bottom: 12px;
            }
            .drop-zone p {
                font-size: 1.05rem;
                color: var(--text);
                margin-bottom: 6px;
            }
            .drop-zone span {
                font-size: 0.85rem;
                color: var(--text-muted);
            }
            .input-group {
                margin-top: 20px;
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 15px;
            }
            .input-field {
                display: flex;
                flex-direction: column;
                gap: 6px;
            }
            label {
                font-size: 0.85rem;
                font-weight: 600;
                color: var(--text-muted);
            }
            input[type="text"] {
                background: rgba(15, 23, 42, 0.6);
                border: 1px solid var(--card-border);
                color: #fff;
                padding: 10px 14px;
                border-radius: 8px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.9rem;
            }
            input[type="text"]:focus {
                outline: none;
                border-color: var(--primary);
            }
            .actions {
                margin-top: 25px;
                display: flex;
                gap: 15px;
            }
            button {
                flex: 1;
                padding: 14px 20px;
                font-size: 1rem;
                font-weight: 600;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                transition: all 0.2s ease;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
            }
            .btn-primary {
                background: linear-gradient(135deg, var(--primary), var(--accent));
                color: #fff;
                box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
            }
            .btn-primary:hover {
                opacity: 0.95;
                transform: translateY(-1px);
            }
            .btn-secondary {
                background: rgba(255, 255, 255, 0.06);
                color: var(--text);
                border: 1px solid var(--card-border);
            }
            .btn-secondary:hover {
                background: rgba(255, 255, 255, 0.12);
            }
            #statusCard {
                display: none;
            }
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
                gap: 15px;
                margin-top: 20px;
            }
            .stat-box {
                background: rgba(15, 23, 42, 0.6);
                padding: 15px;
                border-radius: 12px;
                border: 1px solid var(--card-border);
                text-align: center;
            }
            .stat-val {
                font-size: 1.4rem;
                font-weight: 700;
                color: var(--accent);
            }
            .stat-lbl {
                font-size: 0.8rem;
                color: var(--text-muted);
                margin-top: 4px;
            }
            .download-btn {
                margin-top: 25px;
                display: block;
                text-decoration: none;
                text-align: center;
                padding: 14px;
                background: linear-gradient(135deg, #10b981, #059669);
                color: white;
                font-weight: 700;
                border-radius: 10px;
                box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
                transition: transform 0.2s;
            }
            .download-btn:hover {
                transform: translateY(-2px);
            }
            .spinner {
                border: 3px solid rgba(255, 255, 255, 0.1);
                border-radius: 50%;
                border-top: 3px solid #fff;
                width: 20px;
                height: 20px;
                animation: spin 1s linear infinite;
                display: none;
            }
            @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
            .links {
                text-align: center;
                margin-top: 15px;
                font-size: 0.9rem;
            }
            .links a {
                color: #a5b4fc;
                text-decoration: none;
                margin: 0 10px;
            }
            .links a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <div class="badge">⚡ FASTAPI + ML EDA AUTOMATION</div>
                <h1>CSV to Report Generator</h1>
                <p class="subtitle">Upload a dataset to instantly generate comprehensive EDA & Baseline ML PDF reports</p>
            </header>

            <div class="card">
                <form id="uploadForm">
                    <div class="drop-zone" id="dropZone">
                        <svg viewBox="0 0 24 24"><path d="M19.35 10.04C18.67 6.59 15.64 4 12 4 9.11 4 6.6 5.64 5.35 8.04 2.34 8.36 0 10.91 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.65-4.96zM14 13v4h-4v-4H7l5-5 5 5h-3z"/></svg>
                        <p id="fileNameDisplay">Click or Drag & Drop your CSV file here</p>
                        <span>Supports .csv format</span>
                        <input type="file" id="fileInput" name="file" accept=".csv" style="display: none;">
                    </div>

                    <div class="input-group">
                        <div class="input-field">
                            <label>Target Column (Optional)</label>
                            <input type="text" id="targetColumn" name="target_column" placeholder="e.g. diagnosis">
                        </div>
                        <div class="input-field">
                            <label>ID Columns to Drop (Comma-separated)</label>
                            <input type="text" id="idColumns" name="id_columns" placeholder="e.g. id">
                        </div>
                    </div>

                    <div class="actions">
                        <button type="button" class="btn-secondary" id="sampleBtn">Run Sample (Cancer_Data.csv)</button>
                        <button type="submit" class="btn-primary" id="generateBtn">
                            <div class="spinner" id="spinner"></div>
                            <span id="btnText">Generate Full PDF Report</span>
                        </button>
                    </div>
                </form>
            </div>

            <div class="card" id="statusCard">
                <h3 style="color: var(--success); display: flex; align-items: center; gap: 8px;">
                    ✓ Report Generated Successfully!
                </h3>
                <div class="stats-grid" id="statsContainer"></div>
                <a href="#" id="downloadLink" class="download-btn" target="_blank">📥 Download PDF Report</a>
            </div>

            <div class="links">
                <a href="/docs" target="_blank">📚 Swagger API Docs</a>
                <a href="/redoc" target="_blank">📖 ReDoc</a>
                <a href="/health" target="_blank">🩺 Health Status</a>
            </div>
        </div>

        <script>
            const dropZone = document.getElementById('dropZone');
            const fileInput = document.getElementById('fileInput');
            const fileNameDisplay = document.getElementById('fileNameDisplay');
            const uploadForm = document.getElementById('uploadForm');
            const generateBtn = document.getElementById('generateBtn');
            const sampleBtn = document.getElementById('sampleBtn');
            const spinner = document.getElementById('spinner');
            const btnText = document.getElementById('btnText');
            const statusCard = document.getElementById('statusCard');
            const statsContainer = document.getElementById('statsContainer');
            const downloadLink = document.getElementById('downloadLink');

            dropZone.onclick = () => fileInput.click();

            dropZone.ondragover = (e) => {
                e.preventDefault();
                dropZone.classList.add('dragover');
            };
            dropZone.ondragleave = () => dropZone.classList.remove('dragover');
            dropZone.ondrop = (e) => {
                e.preventDefault();
                dropZone.classList.remove('dragover');
                if (e.dataTransfer.files.length > 0) {
                    fileInput.files = e.dataTransfer.files;
                    fileNameDisplay.textContent = fileInput.files[0].name;
                }
            };

            fileInput.onchange = () => {
                if (fileInput.files.length > 0) {
                    fileNameDisplay.textContent = fileInput.files[0].name;
                }
            };

            function setLoading(loading) {
                spinner.style.display = loading ? 'block' : 'none';
                btnText.textContent = loading ? 'Analyzing & Compiling Report...' : 'Generate Full PDF Report';
                generateBtn.disabled = loading;
                sampleBtn.disabled = loading;
            }

            function displayResults(data) {
                statusCard.style.display = 'block';
                downloadLink.href = data.report_url;
                downloadLink.setAttribute('download', data.filename);

                const ov = data.overview || {};
                const met = data.metrics || {};

                statsContainer.innerHTML = `
                    <div class="stat-box">
                        <div class="stat-val">${ov.rows ?? '-'}</div>
                        <div class="stat-lbl">Rows</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-val">${ov.columns ?? '-'}</div>
                        <div class="stat-lbl">Columns</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-val">${ov.task_type ?? '-'}</div>
                        <div class="stat-lbl">Task</div>
                    </div>
                    ${met.accuracy ? `
                    <div class="stat-box">
                        <div class="stat-val">${(met.accuracy * 100).toFixed(1)}%</div>
                        <div class="stat-lbl">Accuracy</div>
                    </div>` : ''}
                    ${met.f1 ? `
                    <div class="stat-box">
                        <div class="stat-val">${(met.f1 * 100).toFixed(1)}%</div>
                        <div class="stat-lbl">F1 Score</div>
                    </div>` : ''}
                `;
                statusCard.scrollIntoView({ behavior: 'smooth' });
            }

            uploadForm.onsubmit = async (e) => {
                e.preventDefault();
                if (!fileInput.files.length) {
                    alert('Please select a CSV file first!');
                    return;
                }
                const formData = new FormData(uploadForm);
                setLoading(true);
                statusCard.style.display = 'none';

                try {
                    const response = await fetch('/api/generate-report', {
                        method: 'POST',
                        body: formData
                    });
                    const data = await response.json();
                    if (!response.ok) throw new Error(data.detail || 'Failed to generate report');
                    displayResults(data);
                } catch (err) {
                    alert('Error: ' + err.message);
                } finally {
                    setLoading(false);
                }
            };

            sampleBtn.onclick = async () => {
                setLoading(true);
                statusCard.style.display = 'none';
                try {
                    const response = await fetch('/api/sample-report');
                    const data = await response.json();
                    if (!response.ok) throw new Error(data.detail || 'Sample generation failed');
                    displayResults(data);
                } catch (err) {
                    alert('Error: ' + err.message);
                } finally {
                    setLoading(false);
                }
            };
        </script>
    </body>
    </html>
    """
