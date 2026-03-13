from flask import Flask, render_template_string, request, jsonify
import random

app = Flask(__name__)

# Rebranded HTML Template (InstaCaps v2.3)
HTML_TEMPLATE = r'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>InstaCaps: Glowing AI Captions</title>
    <!-- Modern Typography -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --glass-bg: rgba(255, 255, 255, 0.05);
            --glass-border: rgba(255, 255, 255, 0.1);
            --glass-blur: 24px;
            --primary: #ff6200; /* Strong Orange */
            --secondary: #00a8ff; /* Strong Water Blue */
            --accent: #ff3d00;
            --text-main: #ffffff;
            --text-muted: rgba(255, 255, 255, 0.6);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Outfit', sans-serif;
        }

        body {
            background-color: #050510;
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 40px 20px;
            position: relative;
            overflow-x: hidden;
        }

        /* Animated Glowing Orbs Background */
        .ambient-light {
            position: fixed;
            border-radius: 50%;
            filter: blur(140px);
            z-index: -1;
            opacity: 0.8;
            animation: pulse-glow 12s ease-in-out infinite alternate;
        }

        .orb-1 {
            width: 700px;
            height: 700px;
            background: var(--primary); /* Strong Orange Spurge */
            top: -200px;
            left: -200px;
            animation-delay: 0s;
        }

        .orb-2 {
            width: 800px;
            height: 800px;
            background: var(--secondary); /* Strong Water Blue Spurge */
            bottom: -250px;
            right: -250px;
            animation-delay: -6s;
        }

        .orb-3 {
            display: none; /* Removed the center mixed orb to keep diagonals pure */
        }

        /* Interactive Mouse Following Glow */
        .mouse-glow {
            position: fixed;
            width: 800px;
            height: 800px;
            background: radial-gradient(circle, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0) 60%);
            border-radius: 50%;
            pointer-events: none;
            transform: translate(-50%, -50%);
            z-index: 0;
            opacity: 0;
            transition: opacity 0.5s ease;
            will-change: transform, left, top;
        }

        @media (min-width: 768px) {
            body:hover .mouse-glow {
                opacity: 1;
            }
        }

        @keyframes pulse-glow {
            0% { transform: scale(1) translate(0, 0); opacity: 0.4; }
            50% { transform: scale(1.2) translate(50px, -50px); opacity: 0.7; }
            100% { transform: scale(0.9) translate(-50px, 50px); opacity: 0.3; }
        }

        .app-container {
            width: 100%;
            max-width: 540px;
            display: flex;
            flex-direction: column;
            gap: 30px;
            z-index: 1;
        }

        /* Glassmorphism Panel Utility */
        .glass-panel {
            background: var(--glass-bg);
            backdrop-filter: blur(var(--glass-blur));
            -webkit-backdrop-filter: blur(var(--glass-blur));
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 32px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        }

        header {
            text-align: center;
        }

        h1 {
            font-size: 2.8rem;
            font-weight: 800;
            background: linear-gradient(to right, #fff, #a0bde3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
            letter-spacing: -1px;
        }

        .subtitle {
            color: var(--text-muted);
            font-size: 1.1rem;
            font-weight: 300;
        }

        .form-group {
            margin-bottom: 24px;
        }

        label {
            display: block;
            font-size: 0.9rem;
            font-weight: 600;
            color: var(--text-muted);
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .glass-input {
            width: 100%;
            padding: 14px 18px;
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid var(--glass-border);
            border-radius: 12px;
            color: #fff;
            font-size: 1rem;
            transition: all 0.3s ease;
            outline: none;
        }

        .glass-input::placeholder {
            color: rgba(255, 255, 255, 0.3);
        }

        .glass-input:focus {
            background: rgba(255, 255, 255, 0.1);
            border-color: rgba(255, 255, 255, 0.5);
            box-shadow: 0 0 15px rgba(255, 255, 255, 0.1);
        }

        /* Hide Number Input Arrows */
        input[type="number"]::-webkit-inner-spin-button,
        input[type="number"]::-webkit-outer-spin-button {
            -webkit-appearance: none;
            margin: 0;
        }
        input[type="number"] {
            -moz-appearance: textfield; /* Firefox */
        }

        /* Grid for 2 columns */
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
        }

        @media (max-width: 480px) {
            .form-row {
                grid-template-columns: 1fr;
            }
        }

        /* Generator Button */
        .btn-generate {
            width: 100%;
            padding: 16px;
            border-radius: 14px;
            border: none;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            font-size: 1.1rem;
            font-weight: 800;
            letter-spacing: 0.5px;
            cursor: pointer;
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
            box-shadow: 0 10px 20px rgba(58, 134, 255, 0.3);
            margin-top: 10px;
        }

        .btn-generate::before {
            content: '';
            position: absolute;
            top: 0; left: -100%; width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s ease;
        }

        .btn-generate:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 25px rgba(58, 134, 255, 0.4);
            filter: brightness(1.1);
        }

        .btn-generate:hover::before {
            left: 100%;
        }

        .btn-generate:active {
            transform: translateY(1px);
        }
        
        .btn-generate:disabled {
            background: rgba(255, 255, 255, 0.1);
            color: rgba(255, 255, 255, 0.3);
            box-shadow: none;
            cursor: not-allowed;
            transform: none;
        }

        .limit-msg {
            background: rgba(255, 0, 110, 0.15);
            border: 1px solid rgba(255, 0, 110, 0.3);
            color: #ffb3c6;
            padding: 16px;
            border-radius: 12px;
            text-align: center;
            font-weight: 600;
            display: none;
            margin-bottom: 24px;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        }

        /* Results Container */
        #generator-panel {
            position: relative;
            z-index: 10; /* Keeps dropdowns above results */
        }

        #results {
            position: relative;
            z-index: 1;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .caption-card {
            padding: 24px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            position: relative;
            opacity: 0;
            animation: slideUpFade 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }

        @keyframes slideUpFade {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .caption-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.2);
            background: rgba(255, 255, 255, 0.08); /* slightly lighter on hover */
            border-color: rgba(255, 255, 255, 0.2);
        }

        .archetype-tag {
            display: inline-block;
            padding: 4px 10px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #a0bde3;
            margin-bottom: 16px;
            border: 1px solid rgba(255, 255, 255, 0.15);
        }

        .caption-text {
            font-size: 1.05rem;
            line-height: 1.6;
            color: #f8f9fa;
            white-space: pre-wrap;
            margin-bottom: 20px;
        }

        .copy-btn {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--glass-border);
            color: var(--text-muted);
            padding: 10px 20px;
            border-radius: 30px;
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }

        .copy-btn:hover {
            background: rgba(255, 255, 255, 0.15);
            color: #fff;
            border-color: rgba(255, 255, 255, 0.3);
        }

        .copy-btn.copied {
            background: var(--primary);
            color: #fff;
            border-color: var(--primary);
            box-shadow: 0 0 15px rgba(255, 154, 60, 0.4);
        }

        .credits {
            text-align: center;
            font-size: 0.85rem;
            color: var(--text-muted);
            opacity: 0.7;
            margin-top: 20px;
            margin-bottom: 40px;
        }

        .credits-highlight {
            color: #fff;
            font-weight: 600;
        }
        
        /* --- Luxury iOS Custom Dropdown --- */
        .select-wrapper {
            position: relative;
            user-select: none;
            width: 100%;
        }

        .select-wrapper.open {
            z-index: 999;
        }

        .select-wrapper select {
            display: none; /* Hide default select */
        }

        .custom-select-trigger {
            width: 100%;
            padding: 14px 18px;
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid var(--glass-border);
            border-radius: 12px;
            color: #fff;
            font-size: 1rem;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.3s ease;
        }

        .select-wrapper.open .custom-select-trigger {
            background: rgba(255, 255, 255, 0.1);
            border-color: rgba(255, 255, 255, 0.5);
            box-shadow: 0 0 15px rgba(255, 255, 255, 0.1);
        }

        /* Chevron Icon */
        .custom-select-trigger::after {
            content: '';
            width: 12px;
            height: 12px;
            background-image: url("data:image/svg+xml,%3Csvg width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
            background-size: contain;
            background-repeat: no-repeat;
            transition: transform 0.3s ease;
            opacity: 0.8;
            margin-left: 10px;
        }

        .select-wrapper.open .custom-select-trigger::after {
            transform: rotate(-180deg);
        }

        /* iOS Frosted Glass Menu Options */
        .custom-options {
            position: absolute;
            top: calc(100% + 8px);
            left: 0;
            right: 0;
            background: rgba(30, 30, 35, 0.7);
            backdrop-filter: blur(25px);
            -webkit-backdrop-filter: blur(25px);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 14px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);
            overflow: hidden;
            opacity: 0;
            visibility: hidden;
            transform: translateY(-10px);
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
            z-index: 100;
            padding: 6px;
        }

        .select-wrapper.open .custom-options {
            opacity: 1;
            visibility: visible;
            transform: translateY(0);
        }

        .custom-option {
            padding: 12px 14px;
            color: #f8f9fa;
            font-size: 1rem;
            font-weight: 500;
            cursor: pointer;
            border-radius: 10px;
            transition: background 0.2s ease, transform 0.1s ease;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .custom-option:hover {
            background: rgba(255, 255, 255, 0.12);
        }

        .custom-option:active {
            transform: scale(0.98);
        }

        /* Checkmark for Selected State */
        .custom-option.selected {
            color: var(--secondary);
            font-weight: 600;
        }

        .custom-option.selected::after {
            content: '';
            width: 14px;
            height: 14px;
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 24 24' fill='none' stroke='%2387ceeb' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='20 6 9 17 4 12'%3E%3C/polyline%3E%3C/svg%3E");
            background-size: contain;
            background-repeat: no-repeat;
        }
    </style>
</head>
<body>
    <div class="mouse-glow" id="mouseGlow"></div>
    
    <div class="ambient-light orb-1"></div>
    <div class="ambient-light orb-2"></div>
    <div class="ambient-light orb-3"></div>

    <div class="app-container">
        <header>
            <h1>InstaCaps</h1>
            <p class="subtitle">AI Captions</p>
        </header>

        <div class="glass-panel" id="generator-panel">
            <div id="limitMsg" class="limit-msg">
                Daily limit reached. Magic resets tomorrow! ✨
            </div>

            <form id="genForm">
                <div class="form-group">
                    <label>Product Name</label>
                    <input type="text" id="product" class="glass-input" required placeholder="e.g. Midnight Onyx Watch">
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label>Price (₹)</label>
                        <input type="number" id="price" class="glass-input" required placeholder="e.g. 8999">
                    </div>
                    <div class="form-group">
                        <label>Include price in caption?</label>
                        <select id="include_price" class="glass-input">
                            <option value="yes">Yes, show price</option>
                            <option value="no">No (Hidden)</option>
                        </select>
                    </div>
                </div>

                <div class="form-row">
                    <div class="form-group">
                        <label>Category</label>
                        <select id="category" class="glass-input">
                            <option value="clothing">Style / Clothing</option>
                            <option value="beauty">Beauty / Care</option>
                            <option value="gadgets">Tech / Gadgets</option>
                            <option value="others">Lifestyle / Others</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Caption Style</label>
                        <select id="style" class="glass-input">
                            <option value="viral">Viral 🔥</option>
                            <option value="funny">Relatable 😂</option>
                            <option value="luxury">Luxury ✨</option>
                            <option value="emotional">Vibes 💖</option>
                            <option value="sales">Drop 🛒</option>
                        </select>
                    </div>
                </div>

                <div class="form-group">
                    <label>Target Audience</label>
                    <select id="audience" class="glass-input">
                        <option value="general">Broad Audience</option>
                        <option value="men">Men</option>
                        <option value="women">Women</option>
                        <option value="students">Gen Z & Creatives</option>
                    </select>
                </div>

                <button type="submit" id="genBtn" class="btn-generate">
                    Generate Captions ✨
                </button>
            </form>
        </div>

        <div id="results"></div>

        <div class="credits">
            Daily Free Quota: <span class="credits-highlight">15 Gens</span>
        </div>
    </div>

    <!-- SVG Icons -->
    <svg style="display:none">
        <symbol id="icon-copy" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
        </symbol>
        <symbol id="icon-check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"></polyline>
        </symbol>
    </svg>

    <script>
        const MAX_DAILY_LIMIT = 15;

        // Interactive Mouse Glow Tracker
        const mouseGlow = document.getElementById('mouseGlow');
        document.addEventListener('mousemove', (e) => {
            if (window.innerWidth >= 768) {
                requestAnimationFrame(() => {
                    mouseGlow.style.left = e.clientX + 'px';
                    mouseGlow.style.top = e.clientY + 'px';
                });
            }
        });

        function checkLimit() {
            const today = new Date().toISOString().split('T')[0];
            const stored = JSON.parse(localStorage.getItem('instaCaps_usage_v3') || '{}');
            
            if (stored.date !== today) {
                localStorage.setItem('instaCaps_usage_v3', JSON.stringify({ date: today, count: 0 }));
                return true;
            }
            
            if (stored.count >= MAX_DAILY_LIMIT) {
                document.getElementById('genBtn').disabled = true;
                document.getElementById('genBtn').innerHTML = "Limit Reached ⚡";
                document.getElementById('limitMsg').style.display = 'block';
                return false;
            }
            return true;
        }

        function incrementUsage() {
            const today = new Date().toISOString().split('T')[0];
            const stored = JSON.parse(localStorage.getItem('instaCaps_usage_v3') || `{"date":"${today}","count":0}`);
            stored.count++;
            localStorage.setItem('instaCaps_usage_v3', JSON.stringify(stored));
            checkLimit(); 
        }

        document.addEventListener('DOMContentLoaded', () => {
            checkLimit();

            // Initialize Luxury Custom Selects
            document.querySelectorAll('select.glass-input').forEach(select => {
                const wrapper = document.createElement('div');
                wrapper.className = 'select-wrapper';
                select.parentNode.insertBefore(wrapper, select);
                wrapper.appendChild(select);
                
                const trigger = document.createElement('div');
                trigger.className = 'custom-select-trigger';
                trigger.textContent = select.options[select.selectedIndex].textContent;
                wrapper.appendChild(trigger);
                
                const optionsContainer = document.createElement('div');
                optionsContainer.className = 'custom-options';
                wrapper.appendChild(optionsContainer);
                
                Array.from(select.options).forEach(option => {
                    const customOption = document.createElement('div');
                    customOption.className = 'custom-option';
                    if (option.selected) customOption.classList.add('selected');
                    customOption.textContent = option.textContent;
                    customOption.dataset.value = option.value;
                    
                    customOption.addEventListener('click', function(e) {
                        e.stopPropagation();
                        trigger.textContent = this.textContent;
                        select.value = this.dataset.value;
                        
                        // Update visual selection state
                        optionsContainer.querySelectorAll('.custom-option').forEach(opt => opt.classList.remove('selected'));
                        this.classList.add('selected');
                        wrapper.classList.remove('open');
                    });
                    optionsContainer.appendChild(customOption);
                });
                
                trigger.addEventListener('click', function(e) {
                    e.stopPropagation();
                    // Close other toggles
                    document.querySelectorAll('.select-wrapper').forEach(w => {
                        if (w !== wrapper) w.classList.remove('open');
                    });
                    wrapper.classList.toggle('open');
                });
            });

            // Close dropdowns when clicking anywhere outside
            document.addEventListener('click', () => {
                document.querySelectorAll('.select-wrapper').forEach(w => w.classList.remove('open'));
            });
        });

        document.getElementById('genForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            if (!checkLimit()) return;

            const results = document.getElementById('results');
            const btn = document.getElementById('genBtn');
            const style = document.getElementById('style').value;
            
            btn.disabled = true;
            btn.innerHTML = `Crafting Magic... ✨`;
            results.innerHTML = '';
            
            const data = {
                product: document.getElementById('product').value,
                price: document.getElementById('price').value,
                include_price: document.getElementById('include_price').value,
                style: style,
                category: document.getElementById('category').value,
                audience: document.getElementById('audience').value
            };

            try {
                const res = await fetch('/generate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                const responseData = await res.json();
                
                // Render Captions
                responseData.captions.forEach((item, index) => {
                    const card = document.createElement('div');
                    card.className = 'glass-panel caption-card';
                    card.style.animationDelay = `${index * 0.15}s`; 
                    card.innerHTML = `
                        <span class="archetype-tag">${item.archetype}</span>
                        <div class="caption-text" id="cap-${index}">${item.text}</div>
                        <button class="copy-btn" onclick="copyCaption('cap-${index}', this)">
                            <svg width="14" height="14"><use href="#icon-copy"></use></svg>
                            Copy Caption
                        </button>
                    `;
                    results.appendChild(card);
                });
                
                // Render Hashtags
                if (responseData.hashtags) {
                    const tagCard = document.createElement('div');
                    tagCard.className = 'glass-panel caption-card';
                    tagCard.style.animationDelay = `0.6s`;
                    tagCard.innerHTML = `
                        <span class="archetype-tag" style="color: var(--primary); border-color: rgba(255, 98, 0, 0.3);">HASHTAGS</span>
                        <div class="caption-text" id="cap-tags" style="color: #a0bde3; font-weight: 500;">${responseData.hashtags.replace(/\n/g, '<br>')}</div>
                        <button class="copy-btn" onclick="copyCaption('cap-tags', this)">
                            <svg width="14" height="14"><use href="#icon-copy"></use></svg>
                            Copy Hashtags
                        </button>
                    `;
                    results.appendChild(tagCard);
                }
                
                incrementUsage();
                
            } catch (err) {
                console.error(err);
                results.innerHTML = `
                    <div class="glass-panel caption-card" style="border-color: rgba(255,0,110,0.4)">
                        <span style="color: #ff006e">Connection lost. Try again.</span>
                    </div>`;
            } finally {
                if (checkLimit()) {
                    btn.disabled = false;
                    btn.innerHTML = "Generate Captions ✨";
                }
            }
        });

        function copyCaption(id, btn) {
            const text = document.getElementById(id).innerText;
            navigator.clipboard.writeText(text).then(() => {
                const originalHtml = btn.innerHTML;
                btn.innerHTML = `
                    <svg width="14" height="14"><use href="#icon-check"></use></svg>
                    Copied!
                `;
                btn.classList.add('copied');
                
                setTimeout(() => {
                    btn.innerHTML = originalHtml;
                    btn.classList.remove('copied');
                }, 2000);
            });
        }
    </script>
</body>
</html>
'''

# --- ARCHETYPE ENGINE (Soft Price Copy Logic - Unchanged) ---

# Emojis bank
EMOJIS = {
    'clothing': ['👗', '👕', '👠', '✨'],
    'beauty': ['💄', '💋', '✨', '💅'],
    'gadgets': ['📱', '🎧', '💻', '⚡'],
    'others': ['🎁', '📦', '🔥', '✨']
}

def get_emojis(category):
    return EMOJIS.get(category, EMOJIS['others'])

def generate_caption_by_archetype(archetype, product, price, style, category, include_price):
    emojis = get_emojis(category)
    e1 = random.choice(emojis)
    e2 = random.choice(emojis)
    
    # Soft Price Copy Logic
    prefixes = ["Just", "Only", "Yours for", "At just", "Steal deal:", "Starts at", "Grab it for"]
    prefix = random.choice(prefixes)
    
    formatted_price = f"{prefix} ₹{price}" if include_price else ""
    
    if archetype == 'pov_hook':
        scenarios = [
             f"You found the perfect {product}",
             f"Your search for the best {product} ends here",
             f"You finally bought the {product} of your dreams"
        ]
        scenario = random.choice(scenarios)
        cta = f"Get yours: {formatted_price}. {e1}" if include_price else f"Get yours today. {e1}"
        return f"POV: {scenario}. 🤯\n\nIt’s everything you imagined and more.\n\n{cta}\nLink in bio!"

    elif archetype == 'problem_solution':
        problems = [
            f"Tired of looking for a good {product}?",
            f"Need a {product} that actually works?",
            f"Want to upgrade your {product} game?"
        ]
        prob = random.choice(problems)
        price_line = f"{formatted_price}.\n" if include_price else ""
        return f"{prob} 🤔\n\nMeet the all-new {product}. {e1}\n\nProblem solved. ✅\n{price_line}Order now!"

    elif archetype == 'social_proof':
        openers = [
            f"Why everyone is obsessed with this {product}...",
            f"The best-selling {product} is back in stock!",
            f"5-Star reviews are rolling in for our {product}. ⭐"
        ]
        opener = random.choice(openers)
        cta = f"Grab yours. {formatted_price}." if include_price else "Grab yours before it's gone."
        return f"{opener}\n\nDon't miss the hype. {e1}\n\n{cta}\nDM to order! 📲"

    elif archetype == 'luxury_brand':
        adjectives = ["Elegant", "Timeless", "Premium", "Exquisite", "Bold"]
        a1, a2 = random.sample(adjectives, 2)
        price_line = f"\n\n{formatted_price}." if include_price else ""
        return f"{a1}. {a2}. {product}. ✨\n\nExperience usage like never before.{price_line}\nLink in bio to shop. {e2}"

    elif archetype == 'urgency_drop':
        urgency_price = f"Just ₹{price}" if include_price else ""
        line2 = f"Price drops to {urgency_price} for today only. 📉" if include_price else "Stock is extremely limited! 📉"
        return f"🚨 LOW STOCK ALERT 🚨\n\nOur {product} is selling out fast!\n\n{line2}\n\nHurry! DM or WhatsApp to book. 🏃💨"

    elif archetype == 'minimal_cta':
        price_line = f"\n\n{formatted_price}." if include_price else ""
        return f"{product}.{price_line}\n\nDM to order. {e1}\nLink in bio. 🔗"
        
    return f"Check out this {product}! {e1}" # Fallback

def generate_hashtags(product, category, audience):
    # Generates 20 mock hashtags based on the inputs
    base_tags = ["#trending", "#musthave", "#shopping", "#instafind"]
    
    category_tags = {
        'clothing': ["#ootd", "#fashioninspo", "#style", "#outfitoftheday", "#streetwear"],
        'beauty': ["#skincare", "#makeup", "#glow", "#beautycommunity", "#selfcare"],
        'gadgets': ["#tech", "#gadget", "#innovation", "#smarttech", "#setup"],
        'others': ["#lifestyle", "#homedecor", "#decor", "#aesthetic", "#vibes"]
    }
    
    audience_tags = {
        'women': ["#womensfashion", "#girlboss", "#forher"],
        'men': ["#mensstyle", "#gentleman", "#formhim"],
        'students': ["#genz", "#collegelife", "#aesthetic", "#trendy"],
        'general': ["#everyone", "#viral", "#foryou"]
    }
    
    # Process product name (remove spaces, lowercase)
    product_clean = f"#{''.join(e for e in product if e.isalnum()).lower()}"
    if not product_clean or product_clean == "#": product_clean = "#newproduct"
    
    tags = set([product_clean])
    tags.update(base_tags)
    tags.update(category_tags.get(category, category_tags['others']))
    tags.update(audience_tags.get(audience, audience_tags['general']))
    
    # Pad to 20 tags with generic filler if needed
    filler = ["#shopnow", "#discount", "#offer", "#love", "#instagood", "#photooftheday", "#beautiful", "#happy", "#cute", "#tbt", "#like4like", "#followme"]
    while len(tags) < 20:
        tags.add(random.choice(filler))
        
    tag_list = list(tags)[:20]
    random.shuffle(tag_list)
    
    # Format the block
    formatted = "Popular Hashtags:\n\n"
    formatted += " ".join(tag_list[:10]) + "\n"
    formatted += " ".join(tag_list[10:])
    return formatted

@app.route('/')
def home():
    return HTML_TEMPLATE

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    product = data.get('product', 'product')
    price = data.get('price', '0')
    style = data.get('style', 'viral')
    category = data.get('category', 'others')
    audience = data.get('audience', 'general')
    include_price_str = data.get('include_price', 'yes') 
    include_price = (include_price_str == 'yes')
    
    # 1. Define Archetypes
    archetypes = [
        'pov_hook',
        'problem_solution',
        'social_proof',
        'luxury_brand',
        'urgency_drop',
        'minimal_cta'
    ]
    
    # 2. Select 3 UNIQUE archetypes
    selected_archetypes = random.sample(archetypes, 3)
    
    # 3. Generate Hashtags
    hashtags = generate_hashtags(product, category, audience)
    
    results = []
    for arch in selected_archetypes:
        caption_text = generate_caption_by_archetype(arch, product, price, style, category, include_price)
        readable_name = arch.replace('_', ' ')
        results.append({'text': caption_text, 'archetype': readable_name})

    return jsonify({"captions": results, "hashtags": hashtags})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    print(f"Server starting on http://0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
