document.addEventListener('DOMContentLoaded', () => {

    // ── DOM Refs ──────────────────────────────────────────────────
    const dropZone = document.getElementById('drop-zone');
    const pdfUpload = document.getElementById('pdf-upload');
    const fileCardWrap = document.getElementById('file-card-wrap');
    const filenameDisplay = document.getElementById('filename-display');
    const filesizeDisplay = document.getElementById('filesize-display');
    const progressBar = document.getElementById('upload-progress-bar');
    const progressFill = document.getElementById('progress-fill');
    const progressPct = document.getElementById('progress-pct');
    const progressLabel = document.getElementById('progress-label-text');
    const chatMessages = document.getElementById('chat-messages');
    const welcomeState = document.getElementById('welcome-state');
    const userQuery = document.getElementById('user-query');
    const sendBtn = document.getElementById('send-btn');
    const clearBtn = document.getElementById('clear-btn');
    const statusDot = document.getElementById('status-dot');
    const statusText = document.getElementById('status-text');
    const sidebarStatus = document.getElementById('sidebar-status');

    let isDocumentReady = false;
    let messageCount = 0;

    // ── Status Helper ─────────────────────────────────────────────
    function setStatus(state) {
        const states = {
            idle: { color: '#475569', shadow: 'none', text: 'Ready to Sync' },
            loading: { color: '#f59e0b', shadow: '0 0 8px #f59e0b', text: 'Encoding Vectors...' },
            ready: { color: '#10b981', shadow: '0 0 10px rgba(16,185,129,0.6)', text: 'Neural Link Active' },
            thinking: { color: '#3b82f6', shadow: '0 0 10px rgba(59,130,246,0.6)', text: 'Processing Query...' },
        };
        const s = states[state] || states.idle;
        statusDot.style.background = s.color;
        statusDot.style.boxShadow = s.shadow;
        statusDot.style.transition = 'all 0.4s ease';
        statusText.textContent = s.text;
    }

    // ── Timestamp ─────────────────────────────────────────────────
    function getTime() {
        return new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    }

    // ── Build Bot Message Row ─────────────────────────────────────
    function createBotMessage(html) {
        const row = document.createElement('div');
        row.className = 'message-row';
        row.innerHTML = `
            <div class="avatar bot-avatar"><i class="fa-solid fa-brain"></i></div>
            <div class="message-body">
                <span class="message-meta">Nexus AI · ${getTime()}</span>
                <div class="bubble bot-bubble">${html}</div>
            </div>`;
        return row;
    }

    // ── Build User Message Row ────────────────────────────────────
    function createUserMessage(text) {
        const row = document.createElement('div');
        row.className = 'message-row user-row';
        row.innerHTML = `
            <div class="avatar user-avatar"><i class="fa-solid fa-user"></i></div>
            <div class="message-body">
                <span class="message-meta">${getTime()}</span>
                <div class="bubble user-bubble">${escapeHtml(text)}</div>
            </div>`;
        return row;
    }

    // ── Typing Indicator ──────────────────────────────────────────
    function createTypingRow() {
        const row = document.createElement('div');
        row.className = 'message-row';
        row.id = 'typing-row';
        row.innerHTML = `
            <div class="avatar bot-avatar"><i class="fa-solid fa-brain"></i></div>
            <div class="message-body">
                <span class="message-meta">Nexus AI · thinking</span>
                <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>`;
        return row;
    }

    // ── Append & Scroll ───────────────────────────────────────────
    function appendMessage(el) {
        if (welcomeState) welcomeState.style.display = 'none';
        chatMessages.appendChild(el);
        chatMessages.scrollTo({ top: chatMessages.scrollHeight, behavior: 'smooth' });
        messageCount++;
    }

    // ── Escape HTML ───────────────────────────────────────────────
    function escapeHtml(str) {
        return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }

    // ── Format Bot Text (basic markdown) ─────────────────────────
    function formatResponse(text) {
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`(.*?)`/g, '<code style="font-family:JetBrains Mono,monospace;background:rgba(255,255,255,0.08);padding:2px 6px;border-radius:5px;font-size:0.88em;">$1</code>')
            .replace(/\n/g, '<br>');
    }

    // ════════════════════════════════════════════════════════════
    //  FILE UPLOAD
    // ════════════════════════════════════════════════════════════
    //  FILE UPLOAD
    //  NOTE: dropZone is now a <label for="pdf-upload">.
    //  Clicking it natively opens the file picker on ALL devices
    //  (iOS, Android, desktop) — no .click() delegation needed.
    // ════════════════════════════════════════════════════════════

    // File selected via picker
    pdfUpload.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) handleFileUpload(file);
        // Reset so the same file can be re-uploaded if needed
        pdfUpload.value = '';
    });

    // ── Drag & Drop ─────────────────────────────────────────────
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('drag-over');
    });

    dropZone.addEventListener('dragleave', (e) => {
        // Only clear if leaving the zone itself (not a child)
        if (!dropZone.contains(e.relatedTarget)) {
            dropZone.classList.remove('drag-over');
        }
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
        const file = e.dataTransfer.files[0];
        if (file && file.type === 'application/pdf') {
            handleFileUpload(file);
        } else {
            shakeElement(dropZone);
        }
    });



    async function handleFileUpload(file) {
        // Show file card
        dropZone.classList.add('hidden');
        fileCardWrap.classList.remove('hidden');
        filenameDisplay.textContent = file.name;
        filesizeDisplay.textContent = `${(file.size / (1024 * 1024)).toFixed(2)} MB · PDF Document`;

        // Show progress
        progressBar.classList.remove('hidden');
        setProgress(0, 'Reading document...');
        setStatus('loading');

        const formData = new FormData();
        formData.append('file', file);

        // Simulated incremental progress
        const steps = [
            { pct: 20, label: 'Parsing PDF pages...' },
            { pct: 45, label: 'Splitting into chunks...' },
            { pct: 70, label: 'Generating embeddings...' },
            { pct: 88, label: 'Building FAISS index...' },
        ];
        let stepIdx = 0;
        const interval = setInterval(() => {
            if (stepIdx < steps.length) {
                const s = steps[stepIdx++];
                setProgress(s.pct, s.label);
            }
        }, 800);

        try {
            const response = await fetch('/upload', { method: 'POST', body: formData });
            const result = await response.json();

            clearInterval(interval);
            setProgress(100, 'Complete!');

            if (response.ok) {
                setTimeout(() => {
                    progressBar.classList.add('hidden');
                    isDocumentReady = true;
                    sendBtn.disabled = false;
                    userQuery.disabled = false;
                    userQuery.placeholder = 'Ask anything about your document...';
                    setStatus('ready');

                    // Welcome bot message in chat
                    const msg = createBotMessage(
                        `✅ <strong>${escapeHtml(file.name)}</strong> has been indexed successfully.<br><br>` +
                        `I've built a semantic knowledge graph from your document. Ask me anything!`
                    );
                    appendMessage(msg);
                    userQuery.focus();
                }, 600);
            } else {
                throw new Error(result.error || 'Upload failed');
            }
        } catch (err) {
            clearInterval(interval);
            setStatus('idle');
            progressBar.classList.add('hidden');
            fileCardWrap.classList.add('hidden');
            dropZone.classList.remove('hidden');
            shakeElement(dropZone);
            const errMsg = createBotMessage(
                `⚠️ <strong>Upload failed:</strong> ${escapeHtml(err.message)}<br>Please try again.`
            );
            appendMessage(errMsg);
        }
    }

    function setProgress(pct, label) {
        progressFill.style.width = `${pct}%`;
        progressPct.textContent = `${Math.round(pct)}%`;
        progressLabel.textContent = label;
    }

    // ════════════════════════════════════════════════════════════
    //  CHAT
    // ════════════════════════════════════════════════════════════

    async function handleSend() {
        const text = userQuery.value.trim();
        if (!text || !isDocumentReady) return;

        userQuery.value = '';
        userQuery.style.height = 'auto';

        appendMessage(createUserMessage(text));
        sendBtn.disabled = true;
        setStatus('thinking');

        const typingRow = createTypingRow();
        appendMessage(typingRow);

        try {
            const response = await fetch('/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: text })
            });
            const result = await response.json();

            typingRow.remove();
            sendBtn.disabled = false;
            setStatus('ready');

            if (response.ok) {
                appendMessage(createBotMessage(formatResponse(result.answer)));
            } else {
                appendMessage(createBotMessage(
                    `⚠️ <strong>Error:</strong> ${escapeHtml(result.error || 'Unknown error')}`
                ));
            }
        } catch (err) {
            typingRow.remove();
            sendBtn.disabled = false;
            setStatus('ready');
            appendMessage(createBotMessage(
                `🔌 <strong>Connection lost.</strong> The server may have restarted. Please refresh and try again.`
            ));
        }
    }

    sendBtn.addEventListener('click', handleSend);

    userQuery.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    });

    // Auto-resize textarea
    userQuery.addEventListener('input', () => {
        userQuery.style.height = 'auto';
        userQuery.style.height = Math.min(userQuery.scrollHeight, 120) + 'px';
    });

    // Clear chat
    clearBtn.addEventListener('click', () => {
        if (messageCount === 0) return;
        const msgs = chatMessages.querySelectorAll('.message-row');
        msgs.forEach(m => m.remove());
        messageCount = 0;
        if (welcomeState) welcomeState.style.display = '';
    });

    // ── Shake animation helper ────────────────────────────────────
    function shakeElement(el) {
        el.style.animation = 'none';
        el.offsetHeight; // reflow
        el.style.animation = 'shake 0.4s ease';
        el.addEventListener('animationend', () => el.style.animation = '', { once: true });
    }

    // Inject shake keyframe
    const style = document.createElement('style');
    style.textContent = `@keyframes shake {
        0%,100%{transform:translateX(0)}
        20%{transform:translateX(-8px)}
        40%{transform:translateX(8px)}
        60%{transform:translateX(-5px)}
        80%{transform:translateX(5px)}
    }`;
    document.head.appendChild(style);
});
