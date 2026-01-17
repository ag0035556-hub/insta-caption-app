from flask import Flask, render_template_string, request, jsonify
import random

app = Flask(__name__)

# Rebranded HTML Template (InstaCaps v2.3)
HTML_TEMPLATE = r'''
<!DOCTYPE html>
<html>
<head>
    <title>InstaCaps v2.3</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            max-width: 600px; 
            margin: 40px auto; 
            padding: 20px; 
            color: #e0e0e0; 
            background-color: #1a1a1a; 
        }
        
        h1 { 
            color: #f1c40f; 
            margin-bottom: 5px; 
            text-align: center; 
            font-weight: 700;
            letter-spacing: -1px;
        }
        
        .subtitle {
            text-align: center;
            color: #888;
            font-size: 14px;
            margin-bottom: 30px;
            font-weight: 400;
        }

        .form-container { 
            background: #2d2d2d; 
            padding: 30px; 
            border-radius: 12px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.3); 
            border: 1px solid #333;
        }
        
        .form-group { margin-bottom: 20px; }
        
        label { 
            display: block; 
            font-weight: 600; 
            margin-bottom: 8px; 
            color: #ccc; 
            font-size: 14px;
        }
        
        input, select { 
            width: 100%; 
            padding: 12px; 
            background: #383838;
            border: 1px solid #444; 
            border-radius: 8px; 
            box-sizing: border-box; 
            font-size: 15px; 
            color: white;
            transition: border 0.2s, background 0.2s; 
        }
        
        input:focus, select:focus { 
            border-color: #f1c40f; 
            background: #404040;
            outline: none; 
        }
        
        button#genBtn { 
            width: 100%; 
            background: #f1c40f; 
            color: #1a1a1a; 
            padding: 14px; 
            border: none; 
            border-radius: 8px; 
            cursor: pointer; 
            font-size: 16px; 
            font-weight: 800; 
            margin-top: 10px; 
            transition: transform 0.1s, background 0.2s; 
        }
        
        button#genBtn:hover { 
            background: #f39c12; 
        }
        
        button#genBtn:active {
            transform: scale(0.98);
        }
        
        button#genBtn:disabled { 
            background: #555; 
            color: #888;
            cursor: not-allowed; 
            transform: none; 
        }
        
        .limit-msg {
            background-color: #f39c12; color: #1a1a1a; padding: 15px; 
            border-radius: 8px; margin-top: 20px; text-align: center; 
            font-weight: bold; display: none; margin-bottom: 20px;
        }
        
        /* Animations */
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .caption-card { 
            background: #2d2d2d; 
            border: 1px solid #333; 
            padding: 25px; 
            margin-top: 20px; 
            border-radius: 10px; 
            position: relative; 
            box-shadow: 0 4px 10px rgba(0,0,0,0.1); 
            animation: slideUp 0.4s ease-out forwards;
        }
        
        .caption-text { 
            white-space: pre-wrap; 
            font-size: 16px; 
            color: #eee; 
            line-height: 1.6; 
            margin-bottom: 15px; 
        }
        
        .copy-btn {
            background-color: transparent; 
            border: 1px solid #555; 
            color: #aaa;
            padding: 8px 16px; 
            font-size: 12px; 
            border-radius: 20px; 
            cursor: pointer;
            display: inline-block; 
            transition: all 0.2s; 
            font-weight: 600;
        }
        
        .copy-btn:hover { 
            border-color: #f1c40f; 
            color: #f1c40f; 
        }
        
        .copy-btn.copied { 
            background-color: #f1c40f; 
            color: #1a1a1a; 
            border-color: #f1c40f; 
            transform: scale(1.05);
        }
        
        .credits { 
            text-align: center; 
            margin-top: 40px; 
            font-size: 12px; 
            color: #555; 
        }
        
        .archetype-tag {
            font-size: 10px; 
            text-transform: uppercase; 
            color: #f1c40f; 
            letter-spacing: 1px; 
            margin-bottom: 8px; 
            display: block;
            opacity: 0.7;
        }
    </style>
</head>
<body>
    <h1>InstaCaps</h1>
    <div class="subtitle">Simple caption tool for students & creators.</div>
    
    <div class="form-container">
        <form id="genForm">
            <div class="form-group">
                <label>Product Name</label>
                <input type="text" id="product" required placeholder="e.g. Vintage Camera">
            </div>
            <div class="form-group">
                <label>Price (₹)</label>
                <input type="number" id="price" required placeholder="e.g. 5999">
            </div>

             <div class="form-group">
                <label>Include price in caption?</label>
                <select id="include_price">
                    <option value="yes">Yes, show price</option>
                    <option value="no">No (Hidden)</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>Caption Style</label>
                <select id="style">
                    <option value="viral">Viral 🔥</option>
                    <option value="funny">Funny 😂</option>
                    <option value="luxury">Luxury ✨</option>
                    <option value="emotional">Emotional 💖</option>
                    <option value="sales">Sales 🛒</option>
                </select>
            </div>

            <div class="form-group">
                <label>Category</label>
                <select id="category">
                    <option value="clothing">Clothing</option>
                    <option value="beauty">Beauty</option>
                    <option value="gadgets">Gadgets</option>
                    <option value="others">Others</option>
                </select>
            </div>
            <div class="form-group">
                <label>Target Audience</label>
                <select id="audience">
                    <option value="women">Women</option>
                    <option value="men">Men</option>
                    <option value="students">Students</option>
                    <option value="general">General</option>
                </select>
            </div>
            
            <button type="submit" id="genBtn">Generate Captions ⚡</button>
        </form>
        
        <div id="limitMsg" class="limit-msg">
            You’ve reached today’s free limit. Come back tomorrow! ✨
        </div>
    </div>

    <div id="results"></div>
    
    <div class="credits">Free Plan: 5 Generations / Day</div>

    <script>
        const MAX_DAILY_LIMIT = 5;

        // --- Usage Limit Logic ---
        function checkLimit() {
            const today = new Date().toISOString().split('T')[0];
            const stored = JSON.parse(localStorage.getItem('instaCaps_usage') || '{}');
            
            if (stored.date !== today) {
                // Reset if new day
                localStorage.setItem('instaCaps_usage', JSON.stringify({ date: today, count: 0 }));
                return true;
            }
            
            if (stored.count >= MAX_DAILY_LIMIT) {
                document.getElementById('genBtn').disabled = true;
                document.getElementById('genBtn').innerText = "Limit Reached 🛑";
                document.getElementById('limitMsg').style.display = 'block';
                return false;
            }
            
            return true;
        }

        function incrementUsage() {
            const today = new Date().toISOString().split('T')[0];
            const stored = JSON.parse(localStorage.getItem('instaCaps_usage') || `{"date":"${today}","count":0}`);
            stored.count++;
            localStorage.setItem('instaCaps_usage', JSON.stringify(stored));
            checkLimit(); 
        }

        // Initialize check on load
        document.addEventListener('DOMContentLoaded', checkLimit);

        document.getElementById('genForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            if (!checkLimit()) return;

            const results = document.getElementById('results');
            const btn = document.getElementById('genBtn');
            const style = document.getElementById('style').value;
            
            btn.disabled = true;
            btn.innerText = "Creating magic... ✨";
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
                const captions = await res.json();
                
                captions.forEach((item, index) => {
                    const card = document.createElement('div');
                    card.className = 'caption-card';
                    card.style.animationDelay = `${index * 0.1}s`; 
                    card.innerHTML = `
                        <span class="archetype-tag">${item.archetype}</span>
                        <div class="caption-text" id="cap-${index}">${item.text}</div>
                        <button class="copy-btn" onclick="copyCaption(${index}, this)">Copy Caption</button>
                    `;
                    results.appendChild(card);
                });
                
                incrementUsage();
                
            } catch (err) {
                console.error(err);
                results.innerHTML = '<p style="color:#e74c3c; text-align:center;">Error generating captions.</p>';
            } finally {
                // Only re-enable if limit not reached
                if (checkLimit()) {
                    btn.disabled = false;
                    btn.innerText = "Generate Captions ⚡";
                }
            }
        });

        function copyCaption(id, btn) {
            const text = document.getElementById(`cap-${id}`).innerText;
            navigator.clipboard.writeText(text).then(() => {
                const originalText = btn.innerText;
                btn.innerText = "Copied ✓";
                btn.classList.add('copied');
                setTimeout(() => {
                    btn.innerText = originalText;
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
    
    results = []
    for arch in selected_archetypes:
        caption_text = generate_caption_by_archetype(arch, product, price, style, category, include_price)
        readable_name = arch.replace('_', ' ')
        results.append({'text': caption_text, 'archetype': readable_name})

    return jsonify(results)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    print(f"Server starting on http://0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
