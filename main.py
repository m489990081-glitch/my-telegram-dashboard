import asyncio
import os
import re
from flask import Flask, render_template_string, request, jsonify
from telethon import TelegramClient

API_ID = 37856149
API_HASH = '15cd6c8e937dd1066c7845e87c8964e0'
TARGET_BOT = '@NewCXMZXT_bot'

app = Flask(__name__)
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

client = TelegramClient('session_web', API_ID, API_HASH, loop=loop)

HTML_CODE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Merss Control Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * { 
            box-sizing: border-box; 
            font-family: 'Plus Jakarta Sans', sans-serif; 
            outline: none !important; 
            -webkit-tap-highlight-color: transparent !important;
        }

        body { 
            background: #0f172a; 
            color: #f8fafc; 
            margin: 0; 
            padding: 0; 
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        /* Full App Layout Container */
        .app-container {
            width: 100%;
            max-width: 600px;
            margin: 0 auto;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            background: #111827;
            box-shadow: 0 0 50px rgba(0,0,0,0.5);
            position: relative;
        }

        /* Top Bar Header */
        .app-header {
            padding: 20px;
            background: linear-gradient(180deg, #1f2937 0%, #111827 100%);
            border-bottom: 1px solid #1f2937;
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: sticky;
            top: 0;
            z-index: 10;
            backdrop-filter: blur(10px);
        }

        .app-header h1 {
            font-size: 18px;
            font-weight: 800;
            margin: 0;
            background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.3px;
        }

        .app-header p {
            font-size: 11px;
            color: #6b7280;
            margin: 2px 0 0 0;
            font-weight: 500;
        }

        .content-area {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        /* Quick Action Bar */
        .action-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
        }

        .btn {
            border: none;
            padding: 12px 16px;
            font-size: 13px;
            border-radius: 14px;
            cursor: pointer;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            user-select: none;
            position: relative;
            overflow: hidden;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .btn:active {
            transform: scale(0.96);
            opacity: 0.9;
        }

        .btn-primary { 
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); 
            color: #ffffff;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        }

        .btn-secondary { 
            background: #1f2937; 
            color: #d1d5db; 
            border: 1px solid #374151;
        }

        /* Modern Display Card for Bot Message/Stats */
        .display-card {
            background: rgba(31, 41, 55, 0.6);
            border: 1px solid #374151;
            border-radius: 16px;
            padding: 16px;
            font-size: 13px;
            color: #e5e7eb;
            line-height: 1.6;
            white-space: pre-line;
            word-wrap: break-word;
            backdrop-filter: blur(8px);
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.05);
            animation: fadeIn 0.3s ease-out;
        }

        /* Smooth Input Box */
        #input-container {
            max-height: 0;
            opacity: 0;
            overflow: hidden;
            transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        }

        #input-container.show {
            max-height: 160px;
            opacity: 1;
        }

        .input-card {
            background: rgba(17, 24, 39, 0.8);
            border: 1px solid #3b82f6;
            border-radius: 16px;
            padding: 14px;
            box-shadow: 0 0 20px rgba(59, 130, 246, 0.15);
        }

        .input-card label {
            display: block;
            font-size: 12px;
            font-weight: 700;
            color: #60a5fa;
            margin-bottom: 10px;
        }

        .input-group {
            display: flex;
            gap: 8px;
        }

        input[type="text"] {
            flex: 1;
            min-width: 0;
            background: #1f2937;
            border: 1px solid #374151;
            color: #f8fafc;
            padding: 10px 14px;
            border-radius: 10px;
            font-size: 13px;
            transition: border-color 0.2s;
        }

        input[type="text"]:focus {
            border-color: #60a5fa;
        }

        .btn-send {
            background: #2563eb;
            color: #fff;
            padding: 0 16px;
            border-radius: 10px;
        }

        .section-header {
            font-size: 11px;
            font-weight: 800;
            color: #4b5563;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-top: 8px;
        }

        /* Buttons Grid */
        .dynamic-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            min-height: 60px;
        }

        .btn-dynamic {
            background: #1f2937;
            color: #e5e7eb;
            border: 1px solid #374151;
            border-radius: 12px;
            padding: 12px;
            font-size: 12.5px;
            font-weight: 600;
            animation: pulseIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .btn-dynamic:hover {
            background: #374151;
            border-color: #4b5563;
        }

        /* Bottom Floating Status Bar */
        .status-footer {
            padding: 12px 20px;
            background: #1f2937;
            border-top: 1px solid #374151;
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 12px;
            color: #9ca3af;
            font-weight: 500;
        }

        .status-indicator {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .dot {
            width: 8px;
            height: 8px;
            background: #10b981;
            border-radius: 50%;
            box-shadow: 0 0 10px #10b981;
        }

        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(6px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes pulseIn {
            from { opacity: 0; transform: scale(0.95); }
            to { opacity: 1; transform: scale(1); }
        }

        /* Custom Modern Spinner */
        .spinner-wrapper {
            grid-column: span 2;
            display: flex;
            justify-content: center;
            padding: 20px 0;
        }

        .spinner {
            width: 24px;
            height: 24px;
            border: 3px solid rgba(255, 255, 255, 0.1);
            border-top-color: #3b82f6;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        svg { width: 16px; height: 16px; fill: currentColor; }
    </style>
</head>
<body>
    <div class="app-container">
        <div class="app-header">
            <div>
                <h1>Merss Dashboard</h1>
                <p>System Management Platform</p>
            </div>
            <div class="status-indicator">
                <div class="dot"></div>
            </div>
        </div>

        <div class="content-area">
            <div class="action-grid">
                <button class="btn btn-primary" onclick="sendCmd('/start')">
                    <svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg> Start
                </button>
                <button class="btn btn-secondary" onclick="manualRefresh()">
                    <svg viewBox="0 0 24 24"><path d="M17.65 6.35A7.958 7.958 0 0012 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg> Refresh
                </button>
            </div>

            <div id="output-display" class="display-card" style="display: none;"></div>

            <div id="input-container">
                <div class="input-card">
                    <label id="input-prompt">Instruksi Input</label>
                    <div class="input-group">
                        <input type="text" id="user-input" placeholder="Ketik balasan di sini...">
                        <button class="btn btn-send" onclick="submitInput()">Kirim</button>
                    </div>
                </div>
            </div>

            <div class="section-header">Menu Pilihan</div>

            <div id="dynamic-buttons" class="dynamic-grid">
                <div class="spinner-wrapper"><div class="spinner"></div></div>
            </div>
        </div>

        <div class="status-footer">
            <span id="status-text">Menghubungkan ke sistem...</span>
            <span style="font-size: 10px; color: #4b5563;">v2.0 Full UI</span>
        </div>
    </div>

    <script>
        let isProcessing = false;

        function showLoading() {
            const container = document.getElementById('dynamic-buttons');
            container.innerHTML = '<div class="spinner-wrapper"><div class="spinner"></div></div>';
        }

        function sendCmd(command) {
            isProcessing = true;
            updateStatus('Mengirim perintah...');
            showLoading();
            fetch('/send?cmd=' + encodeURIComponent(command))
                .then(res => res.json())
                .then(data => {
                    updateStatus('Memproses respon...');
                    setTimeout(() => { isProcessing = false; loadBotButtons(); }, 1200);
                });
        }

        function clickBtn(btnText) {
            isProcessing = true;
            updateStatus('Memproses aksi...');
            showLoading();
            fetch('/click?text=' + encodeURIComponent(btnText))
                .then(res => res.json())
                .then(data => {
                    if(data.status === 'success') {
                        updateStatus('Berhasil dikirim');
                    } else {
                        updateStatus('Gagal memproses');
                    }
                    setTimeout(() => { isProcessing = false; loadBotButtons(); }, 1200);
                });
        }

        function manualRefresh() {
            showLoading();
            loadBotButtons();
        }

        function submitInput() {
            const inputVal = document.getElementById('user-input').value;
            if(!inputVal) return;
            sendCmd(inputVal);
            document.getElementById('user-input').value = '';
        }

        function loadBotButtons() {
            if (isProcessing) return;
            
            fetch('/get_bot_state')
                .then(res => res.json())
                .then(data => {
                    const outputDisplay = document.getElementById('output-display');
                    if (data.last_text && data.last_text.trim() !== '') {
                        outputDisplay.innerText = data.last_text;
                        outputDisplay.style.display = 'block';
                    } else {
                        outputDisplay.style.display = 'none';
                    }

                    const container = document.getElementById('dynamic-buttons');
                    if (data.buttons && data.buttons.length > 0) {
                        container.innerHTML = '';
                        data.buttons.forEach(text => {
                            const btn = document.createElement('button');
                            btn.className = 'btn btn-dynamic';
                            btn.innerText = text;
                            btn.onclick = () => clickBtn(text);
                            container.appendChild(btn);
                        });
                    } else {
                        container.innerHTML = '<p style="grid-column: span 2; font-size: 12px; color: #4b5563; text-align: center; margin: 12px 0;">Tidak ada pilihan menu aktif</p>';
                    }

                    const inputContainer = document.getElementById('input-container');
                    const inputPrompt = document.getElementById('input-prompt');
                    if (data.requires_input) {
                        inputPrompt.innerText = 'Input Diperlukan:';
                        inputContainer.classList.add('show');
                    } else {
                        inputContainer.classList.remove('show');
                    }

                    updateStatus('Sistem Siap');
                });
        }

        function updateStatus(msg) {
            document.getElementById('status-text').innerText = msg;
        }

        window.onload = () => {
            loadBotButtons();
            setInterval(loadBotButtons, 2500);
        };
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_CODE)

@app.route('/send')
def send_command():
    cmd = request.args.get('cmd', '')
    try:
        async def action():
            await client.send_message(TARGET_BOT, cmd)
        loop.run_until_complete(action())
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)})

@app.route('/get_bot_state')
def get_bot_state():
    try:
        async def action():
            messages = await client.get_messages(TARGET_BOT, limit=1)
            btn_list = []
            requires_input = False
            clean_text = ""
            
            if messages:
                msg = messages[0]
                raw_text = msg.text or ""
                
                clean_text = re.sub(r'[-=]{3,}', '', raw_text).strip()
                
                if msg.buttons:
                    for row in msg.buttons:
                        for btn in row:
                            btn_list.append(btn.text)
                
                keywords = ['enter', 'input', 'send', 'type', 'masukkan', 'kirimkan', 'ketik', 'password']
                if any(kw in clean_text.lower() for kw in keywords):
                    requires_input = True

            return {"buttons": btn_list, "requires_input": requires_input, "last_text": clean_text}
        
        state = loop.run_until_complete(action())
        return jsonify(state)
    except Exception as e:
        return jsonify({"buttons": [], "requires_input": False, "error": str(e)})

@app.route('/click')
def click_button():
    btn_text = request.args.get('text', '')
    try:
        async def action():
            messages = await client.get_messages(TARGET_BOT, limit=1)
            if messages and messages[0].buttons:
                await messages[0].click(text=btn_text)
            else:
                raise Exception("Tombol tidak ditemukan")
        loop.run_until_complete(action())
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)})

if __name__ == '__main__':
    # Mulai koneksi Telegram
    loop.run_until_complete(client.start())
    # Mengambil port bawaan dari Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
