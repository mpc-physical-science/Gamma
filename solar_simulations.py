# solar_simulations.py
from IPython.display import HTML, display

def run_introduction():
    """Mode 2: Default introduction simulation with fixed parameters (L=1.0, 100 Photons)."""
    html_str = """
    <div style="background-color: #0f172a; padding: 20px; border-radius: 10px; width: 640px; font-family: monospace; color: #f1f5f9; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);">
        <div style="margin-bottom: 20px; padding: 12px; background-color: #1e293b; border-radius: 6px; border: 1px solid #475569; font-size: 13px;">
            <span style="color: #38bdf8; font-weight: bold;">Introduction Simulation Configuration:</span><br>
            • Baseline Mean Free Path (L): <span style="color: #faf015; font-weight: bold;">1.00</span><br>
            • Sample Ray Count: <span style="color: #faf015; font-weight: bold;">100</span><br>
            • Visual Ray Tracing: <span style="color: #22c55e; font-weight: bold;">ON</span>
        </div>
        <div style="margin-bottom: 15px;">
            <button id="start-btn-m2" style="background-color: #38bdf8; color: #0f172a; border: none; padding: 8px 20px; border-radius: 4px; cursor: pointer; font-weight: bold; width: 100%;">Initialize Introduction Walk</button>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
            <span style="color: #e2e8f0; font-weight: bold; font-size: 15px;">Model 2: Initial Boundary Demo</span>
            <span id="status-display-m2" style="color: #94a3b8; font-weight: bold;">Ready</span>
        </div>
        <div style="position: relative; width: 600px; height: 450px; background-color: #1e293b; border-radius: 8px; border: 1px solid #475569;">
            <canvas id="canvas-m2" width="600" height="450" style="position: absolute; left: 0; top: 0;"></canvas>
        </div>
        <div id="stats-panel-m2" style="margin-top: 15px; padding: 12px; background-color: #0f172a; border: 1px solid #38bdf8; border-radius: 6px; font-size: 13px; line-height: 1.5; display: none;">
            <span style="color: #faf015; font-weight: bold; font-size: 14px;">Demo Statistics:</span><br>
            • Total Escaped Rays: <span id="stat-escaped-m2" style="color: #22c55e; font-weight: bold;">0</span> / 100<br>
            • System Status: <span id="stat-status-text-m2" style="color: #38bdf8;">Processing...</span>
        </div>
    </div>
    <script>
    (function() {
        const canvas = document.getElementById('canvas-m2'); 
        const ctx = canvas.getContext('2d');
        const startBtn = document.getElementById('start-btn-m2'); 
        const statusDisp = document.getElementById('status-display-m2');
        const statsPanel = document.getElementById('stats-panel-m2'); 
        const statEscaped = document.getElementById('stat-escaped-m2');
        const statStatusText = document.getElementById('stat-status-text-m2');
        
        const cx = canvas.width / 2; 
        const cy = canvas.height / 2; 
        const sunRadius = 200; 
        const sunRadiusSq = sunRadius * sunRadius;
        const mfp = 1.0; 
        const totalRays = 100;
        
        const PALETTE = ['#0000aa', '#00aa00', '#00aaaa', '#aa0000', '#aa00aa', '#aa5500', '#aaaaaa', '#555555', '#5555ff', '#55ff55', '#55ffff', '#ff5555', '#ff55ff', '#ffff55'];
        function getPhotonColor(idx) { return PALETTE[((idx - 1) % 13) + 1 % PALETTE.length]; }
        
        let animationFrameId; 
        let photons = []; 
        let escapedCount = 0;
        
        drawBackground();
        
        function drawBackground() {
            ctx.clearRect(0, 0, canvas.width, canvas.height); 
            ctx.strokeStyle = '#475569'; 
            ctx.lineWidth = 2;
            ctx.beginPath(); 
            ctx.arc(cx, cy, sunRadius, 0, 2 * Math.PI); 
            ctx.stroke();
        }
        
        startBtn.addEventListener('click', function() {
            cancelAnimationFrame(animationFrameId); 
            drawBackground(); 
            photons = []; 
            escapedCount = 0;
            
            statusDisp.innerText = "Simulating Baseline..."; 
            statusDisp.style.color = "#fa4c4c"; 
            statsPanel.style.display = "block";
            statStatusText.innerText = "Processing random walk arrays..."; 
            statStatusText.style.color = "#38bdf8";
            
            for (let i = 1; i <= totalRays; i++) { 
                photons.push({ x: 0, y: 0, inside: true, color: getPhotonColor(i) }); 
            }
            
            function getStepR() { 
                const denom = 100 + 17 + (mfp / 5.0) * (-4); 
                return (mfp * Math.random() * 2) / denom * sunRadius; 
            }
            
            function introductionStep() {
                let activeParticles = false;
                for (let i = 0; i < photons.length; i++) {
                    let p = photons[i]; 
                    if (!p.inside) continue; 
                    activeParticles = true;
                    
                    const theta = Math.random() * 2 * Math.PI; 
                    const stepR = getStepR();
                    
                    let oldX = p.x; 
                    let oldY = p.y; 
                    let newX = oldX + stepR * Math.cos(theta); 
                    let newY = oldY + stepR * Math.sin(theta);
                    
                    if ((newX * newX + newY * newY) >= sunRadiusSq) {
                        p.inside = false; 
                        escapedCount++;
                        
                        const bVal = oldX * Math.cos(theta) + oldY * Math.sin(theta); 
                        const disc = sunRadiusSq - (oldX * oldX + oldY * oldY) + (bVal * bVal);
                        const root = disc >= 0 ? Math.sqrt(disc) : 0; 
                        let boundR = root - bVal; 
                        if (boundR < 0) boundR = -root - bVal;
                        
                        const boundX = oldX + boundR * Math.cos(theta); 
                        const boundY = oldY + boundR * Math.sin(theta);
                        
                        ctx.strokeStyle = p.color; 
                        ctx.lineWidth = 1.0; 
                        ctx.beginPath(); 
                        ctx.moveTo(cx + oldX, cy + oldY); 
                        ctx.lineTo(cx + boundX, cy + boundY); 
                        ctx.stroke();
                        
                        ctx.beginPath(); 
                        ctx.moveTo(cx + boundX, cy + boundY); 
                        ctx.lineTo(cx + 1.2 * boundX, cy + 1.2 * boundY); 
                        ctx.stroke();
                    } else {
                        ctx.strokeStyle = p.color; 
                        ctx.lineWidth = 1.0; 
                        ctx.beginPath(); 
                        ctx.moveTo(cx + oldX, cy + oldY); 
                        ctx.lineTo(cx + newX, cy + newY); 
                        ctx.stroke();
                        
                        p.x = newX; 
                        p.y = newY;
                    }
                }
                
                statEscaped.innerText = escapedCount;
                
                if (activeParticles && escapedCount < totalRays) { 
                    animationFrameId = requestAnimationFrame(introductionStep); 
                } else { 
                    statusDisp.innerText = "Demo Complete!"; 
                    statusDisp.style.color = "#85ff55"; 
                    statStatusText.innerText = "All introductory rays cleared boundary grid successfully."; 
                    statStatusText.style.color = "#22c55e"; 
                }
            }
            introductionStep();
        });
    })();
    </script>
    """
    display(HTML(html_str))

def run_single_photon():
    """Mode 3: Single photon tracking model with adjustable Mean Free Path slider."""
    html_str = """
    <div style="background-color: #0f172a; padding: 20px; border-radius: 10px; width: 640px; font-family: monospace; color: #f1f5f9; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);">
        <div style="margin-bottom: 20px; display: flex; align-items: center; gap: 15px;">
            <label for="mfp-range" style="color: #cbd5e1;">Mean Free Path (L):</label>
            <input type="range" id="mfp-range" min="1" max="50" step="0.5" value="10" style="width: 200px;">
            <span id="mfp-val" style="color: #faf015; font-weight: bold; min-width: 30px;">10.0</span>
            <button id="start-btn" style="background-color: #22c55e; color: white; border: none; padding: 6px 16px; border-radius: 4px; cursor: pointer; font-weight: bold;">Run Simulation</button>
        </div>
        
        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
            <span style="color: #38bdf8; font-weight: bold; font-size: 16px;">Gamma Ray Single Photon Tracking</span>
            <span id="status-display" style="color: #fa4c4c; font-weight: bold;">Ready</span>
        </div>
        
        <div style="position: relative; width: 600px; height: 450px; background-color: #1e293b; border-radius: 8px; border: 1px solid #475569;">
            <canvas id="canvas" width="600" height="450" style="position: absolute; left: 0; top: 0;"></canvas>
        </div>
        
        <div id="stats-panel" style="margin-top: 15px; padding: 12px; background-color: #0f172a; border: 1px solid #38bdf8; border-radius: 6px; font-size: 13px; line-height: 1.5; display: none;">
            <span style="color: #faf015; font-weight: bold; font-size: 14px;">Photon Statistics:</span><br>
            • Total Steps/Collisions: <span id="stat-steps" style="color: #38bdf8;">0</span><br>
            • Total Distance Traveled: <span id="stat-dist" style="color: #38bdf8;">0</span>% of Sun's Radius
        </div>
    </div>
    
    <script>
    (function() {
        const canvas = document.getElementById('canvas'); 
        const ctx = canvas.getContext('2d');
        const slider = document.getElementById('mfp-range'); 
        const sliderVal = document.getElementById('mfp-val');
        const startBtn = document.getElementById('start-btn'); 
        const statusDisp = document.getElementById('status-display');
        const statsPanel = document.getElementById('stats-panel'); 
        const statSteps = document.getElementById('stat-steps');
        const statDist = document.getElementById('stat-dist');
        const cx = canvas.width / 2; 
        const cy = canvas.height / 2; 
        const sunRadius = 200; 
        const sunRadiusSq = sunRadius * sunRadius;
        
        let animationFrameId;
        
        drawBackground();
        
        slider.addEventListener('input', function() { 
            sliderVal.innerText = parseFloat(slider.value).toFixed(1); 
        });
        
        function drawBackground() {
            ctx.clearRect(0, 0, canvas.width, canvas.height); 
            ctx.strokeStyle = '#475569'; 
            ctx.lineWidth = 2;
            ctx.beginPath(); 
            ctx.arc(cx, cy, sunRadius, 0, 2 * Math.PI); 
            ctx.stroke();
        }
        
        startBtn.addEventListener('click', function() {
            cancelAnimationFrame(animationFrameId); 
            drawBackground();
            
            let posX = 0, posY = 0; 
            let totalDistance = 0; 
            let stepCount = 0; 
            const mfp = parseFloat(slider.value);
            
            statusDisp.innerText = "Simulating..."; 
            statusDisp.style.color = "#fa4c4c"; 
            statsPanel.style.display = "none";
            
            function getStepR() { 
                const denom = 100 + 17 + (mfp / 5.0) * (-4); 
                return (mfp * Math.random() * 2) / denom * sunRadius; 
            }
            
            function simulationStep() {
                const theta = Math.random() * 2 * Math.PI; 
                const stepR = getStepR();
                
                let oldX = posX; 
                let oldY = posY; 
                let newX = oldX + stepR * Math.cos(theta); 
                let newY = oldY + stepR * Math.sin(theta);
                
                totalDistance += stepR; 
                stepCount++;
                
                if ((newX * newX + newY * newY) >= sunRadiusSq) {
                    const bVal = oldX * Math.cos(theta) + oldY * Math.sin(theta); 
                    const disc = sunRadiusSq - (oldX * oldX + oldY * oldY) + (bVal * bVal);
                    const root = disc >= 0 ? Math.sqrt(disc) : 0; 
                    let boundR = root - bVal; 
                    if (boundR < 0) boundR = -root - bVal;
                    
                    const boundX = oldX + boundR * Math.cos(theta); 
                    const boundY = oldY + boundR * Math.sin(theta);
                    
                    ctx.strokeStyle = '#38bdf8'; 
                    ctx.lineWidth = 1.5; 
                    ctx.beginPath(); 
                    ctx.moveTo(cx + oldX, cy + oldY); 
                    ctx.lineTo(cx + boundX, cy + boundY); 
                    ctx.stroke();
                    
                    ctx.strokeStyle = '#fa4c4c'; 
                    ctx.beginPath(); 
                    ctx.moveTo(cx + boundX, cy + boundY); 
                    ctx.lineTo(cx + 2 * boundX, cy + 2 * boundY); 
                    ctx.stroke();
                    
                    statusDisp.innerText = "Escaped!"; 
                    statusDisp.style.color = "#85ff55";
                    
                    statSteps.innerText = stepCount; 
                    statDist.innerText = ((totalDistance / sunRadius) * 100).toFixed(2);
                    statsPanel.style.display = "block"; 
                    return;
                }
                
                ctx.strokeStyle = '#38bdf8'; 
                ctx.lineWidth = 1.5; 
                ctx.beginPath(); 
                ctx.moveTo(cx + oldX, cy + oldY); 
                ctx.lineTo(cx + newX, cy + newY); 
                ctx.stroke();
                
                posX = newX; 
                posY = newY; 
                animationFrameId = requestAnimationFrame(simulationStep);
            }
            simulationStep();
        });
    })();
    </script>
    """
    display(HTML(html_str))

def run_multi_photon():
    """Mode 4: Simultaneously tracks a multiple photon cluster swarm (up to 2,000 photons)."""
    html_str = """
    <div style="background-color: #0f172a; padding: 20px; border-radius: 10px; width: 640px; font-family: monospace; color: #f1f5f9; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);">
        <div style="margin-bottom: 20px; display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <label for="mfp-range-m4" style="color: #cbd5e1; min-width: 140px;">Mean Free Path (L):</label>
                <input type="range" id="mfp-range-m4" min="1" max="50" step="0.5" value="10" style="width: 120px;">
                <span id="mfp-val-m4" style="color: #faf015; font-weight: bold;">10.0</span>
            </div>
            <div style="display: flex; align-items: center; gap: 10px;">
                <label for="rays-range-m4" style="color: #cbd5e1; min-width: 140px;">Photons (Max 2000):</label>
                <input type="range" id="rays-range-m4" min="5" max="2000" step="5" value="100" style="width: 120px;">
                <span id="rays-val-m4" style="color: #faf015; font-weight: bold;">100</span>
            </div>
        </div>
        
        <div style="margin-bottom: 15px;">
            <button id="start-btn-m4" style="background-color: #22c55e; color: white; border: none; padding: 8px 20px; border-radius: 4px; cursor: pointer; font-weight: bold; width: 100%;">Spawn Photon Swarm</button>
        </div>
        
        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
            <span style="color: #38bdf8; font-weight: bold; font-size: 16px;">Gamma Ray Multiple Photon Swarm</span>
            <span id="status-display-m4" style="color: #fa4c4c; font-weight: bold;">Ready</span>
        </div>
        
        <div style="position: relative; width: 600px; height: 450px; background-color: #1e293b; border-radius: 8px; border: 1px solid #475569;">
            <canvas id="canvas-m4" width="600" height="450" style="position: absolute; left: 0; top: 0;"></canvas>
        </div>
        
        <div id="stats-panel-m4" style="margin-top: 15px; padding: 12px; background-color: #0f172a; border: 1px solid #38bdf8; border-radius: 6px; font-size: 13px; line-height: 1.6; display: none;">
            <span style="color: #faf015; font-weight: bold; font-size: 14px;">Swarm Simulation Metrics:</span><br>
            • Total Population Simulated: <span id="stat-total-m4" style="color: #38bdf8;">0</span><br>
            • Escaped Photon Rays: <span id="stat-escaped-m4" style="color: #22c55e; font-weight: bold;">0</span> / <span id="stat-target-m4">0</span><br>
            <div id="extended-metrics-m4" style="margin-top: 5px; border-top: 1px dashed #334155; padding-top: 5px; display: none;">
                <span style="color: #faf015; font-weight: bold;">Collision Profile Results:</span><br>
                • Minimum Collisions (Fastest Escape): <span id="stat-min-coll-m4" style="color: #38bdf8; font-weight: bold;">0</span><br>
                • Maximum Collisions (Slowest Escape): <span id="stat-max-coll-m4" style="color: #38bdf8; font-weight: bold;">0</span><br>
                • Average Swarm Collisions: <span id="stat-avg-coll-m4" style="color: #38bdf8; font-weight: bold;">0</span>
            </div>
        </div>
    </div>
    
    <script>
    (function() {
        const canvas = document.getElementById('canvas-m4'); const ctx = canvas.getContext('2d');
        const mfpSlider = document.getElementById('mfp-range-m4'); const mfpVal = document.getElementById('mfp-val-m4');
        const raysSlider = document.getElementById('rays-range-m4'); const raysVal = document.getElementById('rays-val-m4');
        const startBtn = document.getElementById('start-btn-m4'); const statusDisp = document.getElementById('status-display-m4');
        const statsPanel = document.getElementById('stats-panel-m4'); const extendedMetrics = document.getElementById('extended-metrics-m4');
        const statTotal = document.getElementById('stat-total-m4'); const statEscaped = document.getElementById('stat-escaped-m4'); const statTarget = document.getElementById('stat-target-m4'); 
        const statMinColl = document.getElementById('stat-min-coll-m4'); const statMaxColl = document.getElementById('stat-max-coll-m4'); const statAvgColl = document.getElementById('stat-avg-coll-m4');
        const cx = canvas.width / 2; const cy = canvas.height / 2; const sunRadius = 200; const sunRadiusSq = sunRadius * sunRadius;
        const PALETTE = ['#0000aa', '#00aa00', '#00aaaa', '#aa0000', '#aa00aa', '#aa5500', '#aaaaaa', '#555555', '#5555ff', '#55ff55', '#55ffff', '#ff5555', '#ff55ff', '#ffff55', '#ffffff'];
        function getPhotonColor(index) { return PALETTE[((index - 1) % 13) + 1 % PALETTE.length]; }
        let animationFrameId; let photons = []; let totalRays = 0; let escapedCount = 0;
        drawBackground();
        mfpSlider.addEventListener('input', () => mfpVal.innerText = parseFloat(mfpSlider.value).toFixed(1));
        raysSlider.addEventListener('input', () => raysVal.innerText = parseInt(raysSlider.value));
        function drawBackground() {
            ctx.clearRect(0, 0, canvas.width, canvas.height); ctx.strokeStyle = '#475569'; ctx.lineWidth = 2;
            ctx.beginPath(); ctx.arc(cx, cy, sunRadius, 0, 2 * Math.PI); ctx.stroke();
        }
        startBtn.addEventListener('click', function() {
            cancelAnimationFrame(animationFrameId); drawBackground(); totalRays = parseInt(raysSlider.value); const mfp = parseFloat(mfpSlider.value);
            photons = []; escapedCount = 0;
            statusDisp.innerText = "Simulating Swarm..."; statusDisp.style.color = "#fa4c4c"; statsPanel.style.display = "block"; extendedMetrics.style.display = "none";
            for (let i = 1; i <= totalRays; i++) { photons.push({ id: i, x: 0, y: 0, inside: true, collisions: 0, color: getPhotonColor(i) }); }
            function getStepR() { const denom = 100 + 17 + (mfp / 5.0) * (-4); return (mfp * Math.random() * 2) / denom * sunRadius; }
            function showEndStats() {
                let minC = photons[0].collisions, maxC = photons[0].collisions, sumC = 0;
                for (let i = 0; i < photons.length; i++) {
                    let c = photons[i].collisions; sumC += c; if (c < minC) minC = c; if (c > maxC) maxC = c;
                }
                statMinColl.innerText = minC; statMaxColl.innerText = maxC; statAvgColl.innerText = (sumC / totalRays).toFixed(1); extendedMetrics.style.display = "block";
            }
            function swarmStep() {
                let active = false; const denom = 100 + 17 + (mfp / 5.0) * (-4);
                for (let i = 0; i < photons.length; i++) {
                    let p = photons[i]; if (!p.inside) continue; active = true;
                    const theta = Math.random() * 2 * Math.PI; const stepR = (mfp * Math.random() * 2) / denom * sunRadius;
                    let oldX = p.x, oldY = p.y, newX = oldX + stepR * Math.cos(theta), newY = oldY + stepR * Math.sin(theta);
                    p.collisions++;
                    if ((newX * newX + newY * newY) >= sunRadiusSq) {
                        p.inside = false; escapedCount++;
                        const bVal = oldX * Math.cos(theta) + oldY * Math.sin(theta); const disc = sunRadiusSq - (oldX * oldX + oldY * oldY) + (bVal * bVal);
                        const root = disc >= 0 ? Math.sqrt(disc) : 0; let boundR = root - bVal; if (boundR < 0) boundR = -root - bVal;
                        const boundX = oldX + boundR * Math.cos(theta), boundY = oldY + boundR * Math.sin(theta);
                        ctx.strokeStyle = p.color; ctx.lineWidth = 1.0; ctx.beginPath(); ctx.moveTo(cx + oldX, cy + oldY); ctx.lineTo(cx + boundX, cy + boundY); ctx.stroke();
                        ctx.beginPath(); ctx.moveTo(cx + boundX, cy + boundY); ctx.lineTo(cx + 1.3 * boundX, cy + 1.3 * boundY); ctx.stroke();
                    } else {
                        ctx.strokeStyle = p.color; ctx.lineWidth = 1.0; ctx.beginPath(); ctx.moveTo(cx + oldX, cy + oldY); ctx.lineTo(cx + newX, cy + newY); ctx.stroke();
                        p.x = newX; p.y = newY;
                    }
                }
                statTotal.innerText = totalRays; statEscaped.innerText = escapedCount; statTarget.innerText = totalRays;
                if (active && escapedCount < totalRays) { animationFrameId = requestAnimationFrame(swarmStep); }
                else { statusDisp.innerText = "All Escaped!"; statusDisp.style.color = "#85ff55"; showEndStats(); }
            }
            swarmStep();
        });
    })();
    </script>
    """
    display(HTML(html_str))

def run_batches():
    """Mode 5: Tracks consecutive grouped batch releases with uniform colors per batch layer, 
    speed factor tuning, dynamic fading, and explicit output height overrides."""
    
    html_str = """
    <!-- Outer wrapper forcing Jupyter to render the complete block height without clipping scrollbars -->
    <div style="display: block; overflow: visible; height: auto; padding-bottom: 10px;">
        
        <div style="background-color: #0f172a; padding: 20px; border-radius: 10px; width: 640px; font-family: monospace; color: #f1f5f9; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);">
            
            <!-- Interactive Constraints Control Panel -->
            <div style="margin-bottom: 15px; display: grid; grid-template-columns: 1fr 1fr; gap: 15px; font-size: 12px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <label for="mfp-m5" style="color: #cbd5e1; min-width: 120px;">Mean Free Path:</label>
                    <input type="range" id="mfp-m5" min="1" max="50" step="0.5" value="10" style="width: 100px;">
                    <span id="mfp-val-m5" style="color: #faf015; font-weight: bold;">10.0</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <label for="rays-m5" style="color: #cbd5e1; min-width: 120px;">Photons/Batch:</label>
                    <input type="range" id="rays-m5" min="5" max="200" step="5" value="100" style="width: 100px;">
                    <span id="rays-val-m5" style="color: #faf015; font-weight: bold;">100</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <label for="groups-m5" style="color: #cbd5e1; min-width: 120px;">Total Batches:</label>
                    <input type="range" id="groups-m5" min="2" max="25" step="1" value="20" style="width: 100px;">
                    <span id="groups-val-m5" style="color: #faf015; font-weight: bold;">20</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <label for="interval-m5" style="color: #cbd5e1; min-width: 120px;">Step Interval:</label>
                    <input type="range" id="interval-m5" min="5" max="50" step="5" value="20" style="width: 100px;">
                    <span id="interval-val-m5" style="color: #faf015; font-weight: bold;">20</span>
                </div>
            </div>
            
            <!-- Simulation Speed slider layout bar tray -->
            <div style="margin-bottom: 15px; display: grid; grid-template-columns: 1fr; gap: 10px; font-size: 12px; background-color: #1e293b; padding: 10px; border-radius: 6px; border: 1px solid #334155;">
                <div style="display: flex; align-items: center; gap: 10px; width: 100%;">
                    <label for="speed-m5" style="color: #38bdf8; font-weight: bold; min-width: 140px;">Simulation Speed:</label>
                    <input type="range" id="speed-m5" min="1" max="100" step="1" value="40" style="flex-grow: 1;">
                    <span id="speed-val-m5" style="color: #faf015; font-weight: bold; min-width: 45px; text-align: right;">40%</span>
                </div>
            </div>
            
            <div style="margin-bottom: 15px;">
                <button id="start-btn-m5" style="background-color: #22c55e; color: white; border: none; padding: 8px 20px; border-radius: 4px; cursor: pointer; font-weight: bold; width: 100%;">Release Batch Sequence</button>
            </div>

            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span style="color: #38bdf8; font-weight: bold; font-size: 15px;">Solar Core Batch Release Profile</span>
                <span id="status-display-m5" style="color: #fa4c4c; font-weight: bold;">Ready</span>
            </div>
            
            <div style="position: relative; width: 600px; height: 450px; background-color: #0f172a; border-radius: 8px; border: 1px solid #475569; overflow: hidden;">
                <canvas id="canvas-particles-m5" width="600" height="450" style="position: absolute; left: 0; top: 0; z-index: 1;"></canvas>
                <canvas id="canvas-boundary-m5" width="600" height="450" style="position: absolute; left: 0; top: 0; z-index: 2; pointer-events: none;"></canvas>
            </div>
            
            <div id="stats-panel-m5" style="margin-top: 15px; padding: 12px; background-color: #0f172a; border: 1px solid #38bdf8; border-radius: 6px; font-size: 13px; line-height: 1.6; display: none;">
                <span style="color: #faf015; font-weight: bold; font-size: 14px;">Batch Group Metrics:</span><br>
                • Target Population: <span id="stat-total-m5" style="color: #38bdf8;">0</span> | Batches Launched: <span id="stat-deployed-m5" style="color: #38bdf8;">0</span> / <span id="stat-max-groups-m5">0</span><br>
                • Escaped Photon Count: <span id="stat-escaped-m5" style="color: #22c55e; font-weight: bold;">0</span><br>
                • Calculations Processed: <span id="stat-total-coll-m5" style="color: #e2e8f0;">0</span>
            </div>
        </div>
    </div>
    """
    html_script = """
    <script>
    (function() {
        const cParticles = document.getElementById('canvas-particles-m5'); const ctxP = cParticles.getContext('2d');
        const cBoundary = document.getElementById('canvas-boundary-m5'); const ctxB = cBoundary.getContext('2d');
        const startBtn = document.getElementById('start-btn-m5'); const statusDisp = document.getElementById('status-display-m5'); const statsPanel = document.getElementById('stats-panel-m5');
        const sTotal = document.getElementById('stat-total-m5'); const sDeployed = document.getElementById('stat-deployed-m5'); 
        const sMaxGroups = document.getElementById('stat-max-groups-m5'); const sEscaped = document.getElementById('stat-escaped-m5'); const sColl = document.getElementById('stat-total-coll-m5');
        const speedSlider = document.getElementById('speed-m5'); const speedVal = document.getElementById('speed-val-m5');

        const elements = ['mfp-m5', 'rays-m5', 'groups-m5', 'interval-m5'];
        elements.forEach(id => {
            const el = document.getElementById(id); const val = document.getElementById(id.replace('m5', 'val-m5'));
            if (el && val) el.addEventListener('input', () => { val.innerText = id.includes('mfp') ? parseFloat(el.value).toFixed(1) : el.value; });
        });

        speedSlider.addEventListener('input', () => { speedVal.innerText = speedSlider.value + '%'; });

        const sunRadius = 200; const sunRadiusSq = sunRadius * sunRadius; const cx = cParticles.width / 2; const cy = cParticles.height / 2;
        const PALETTE = ['#00aa00', '#00aaaa', '#aa0000', '#aa00aa', '#aa5500', '#aaaaaa', '#555555', '#5555ff', '#55ff55', '#55ffff', '#ff5555', '#ff55ff', '#ffff55', '#0000aa'];
        function getBatchColor(idx) { return PALETTE[(idx - 1) % PALETTE.length]; }

        let animationId; let globalPhotons = []; let currentCollisionTick = 0;
        let configRays = 0; let configGroups = 0; let configInterval = 0; let configMfp = 0;
        let activeGroupsCount = 0; let totalEscapedEver = 0; let grandTotalCollisions = 0;
        let frameAccumulator = 0;

        drawStaticBoundary();
        ctxP.fillStyle = '#0f172a'; ctxP.fillRect(0, 0, cParticles.width, cParticles.height);

        function drawStaticBoundary() {
            ctxB.clearRect(0, 0, cBoundary.width, cBoundary.height); ctxB.strokeStyle = '#475569'; ctxB.lineWidth = 2;
            ctxB.beginPath(); ctxB.arc(cx, cy, sunRadius, 0, 2 * Math.PI); ctxB.stroke();
        }

        startBtn.addEventListener('click', function() {
            cancelAnimationFrame(animationId);
            configRays = parseInt(document.getElementById('rays-m5').value);
            configGroups = parseInt(document.getElementById('groups-m5').value);
            configInterval = parseInt(document.getElementById('interval-m5').value);
            configMfp = parseFloat(document.getElementById('mfp-m5').value);
            
            globalPhotons = []; currentCollisionTick = 0; activeGroupsCount = 0; totalEscapedEver = 0; grandTotalCollisions = 0; frameAccumulator = 0;
            statusDisp.innerText = "Releasing Swarms..."; statusDisp.style.color = "#fa4c4c"; statsPanel.style.display = "block";
            
            ctxP.fillStyle = '#0f172a'; ctxP.fillRect(0, 0, cParticles.width, cParticles.height);
            spawnNextBatchGroup(); engineLoop();
        });

        function spawnNextBatchGroup() {
            if (activeGroupsCount >= configGroups) return;
            activeGroupsCount++; let batchColor = getBatchColor(activeGroupsCount);
            for (let i = 0; i < configRays; i++) { globalPhotons.push({ x: 0, y: 0, inside: true, color: batchColor }); }
        }

        function engineLoop() {
            let calculationsThisFrame = 0; const denom = 100 + 17 + (configMfp / 5.0) * (-4);
            const speedPct = parseInt(speedSlider.value);
            let stepsToProcess = 1; let frameSkip = 0;

            if (speedPct >= 80) { stepsToProcess = Math.floor((speedPct - 79) * (configInterval / 10)) + 1; }
            else if (speedPct >= 20) { stepsToProcess = Math.max(1, Math.floor(configInterval * (speedPct / 80))); }
            else { stepsToProcess = 1; frameSkip = Math.floor((20 - speedPct) / 2); }

            frameAccumulator++;
            if (frameAccumulator <= frameSkip) { animationId = requestAnimationFrame(engineLoop); return; }
            frameAccumulator = 0;

            ctxP.fillStyle = "rgba(15, 23, 42, 0.04)"; ctxP.fillRect(0, 0, cParticles.width, cParticles.height);

            for (let step = 0; step < stepsToProcess; step++) {
                currentCollisionTick++;
                for (let i = 0; i < globalPhotons.length; i++) {
                    let p = globalPhotons[i]; if (!p.inside) continue;
                    calculationsThisFrame++; grandTotalCollisions++;
                    
                    let theta = Math.random() * 2 * Math.PI; let stepR = (configMfp * Math.random() * 2) / denom * sunRadius;
                    let oldX = p.x, oldY = p.y, newX = oldX + stepR * Math.cos(theta), newY = oldY + stepR * Math.sin(theta);
                    
                    if ((newX * newX + newY * newY) >= sunRadiusSq) {
                        p.inside = false; totalEscapedEver++;
                        const bVal = oldX * Math.cos(theta) + oldY * Math.sin(theta); const disc = sunRadiusSq - (oldX * oldX + oldY * oldY) + (bVal * bVal);
                        const root = disc >= 0 ? Math.sqrt(disc) : 0; let boundR = root - bVal; if (boundR < 0) boundR = -root - bVal;
                        
                        ctxP.strokeStyle = p.color; ctxP.lineWidth = 1.5; ctxP.beginPath(); ctxP.moveTo(cx + oldX, cy + oldY);
                        ctxP.lineTo(cx + (oldX + boundR * Math.cos(theta)), cy + (oldY + boundR * Math.sin(theta))); ctxP.stroke();
                        ctxP.beginPath(); ctxP.moveTo(cx + (oldX + boundR * Math.cos(theta)), cy + (oldY + boundR * Math.sin(theta)));
                        ctxP.lineTo(cx + 1.2 * newX, cy + 1.2 * newY); ctxP.stroke();
                    } else {
                        ctxP.strokeStyle = p.color; ctxP.lineWidth = 1.0; ctxP.beginPath(); ctxP.moveTo(cx + oldX, cy + oldY);
                        ctxP.lineTo(cx + newX, cy + newY); ctxP.stroke();
                        p.x = newX; p.y = newY;
                    }
                }
                if (currentCollisionTick % configInterval === 0 && activeGroupsCount < configGroups) { spawnNextBatchGroup(); }
            }

            sTotal.innerText = configRays * configGroups; sDeployed.innerText = activeGroupsCount;
            sMaxGroups.innerText = configGroups; sEscaped.innerText = totalEscapedEver; sColl.innerText = grandTotalCollisions;

            let particlesActive = false;
            for (let i = 0; i < globalPhotons.length; i++) { if (globalPhotons[i].inside) { particlesActive = true; break; } }

            if (particlesActive || activeGroupsCount < configGroups) {
                animationId = requestAnimationFrame(engineLoop);
            } else {
                statusDisp.innerText = "Sequence Complete!"; statusDisp.style.color = "#85ff55";
            }
        }
    })();
    </script>
    """
    
    display(HTML(html_str + html_script))

def run_dying_sun():
    """Mode 6: Unified Full-Frame Solar Extinction Dashboard. Overlays analytical graphing axes 
    directly on top of a fading full-frame spatial simulation with anchored static scale intercepts."""
    
    html_str = """
    <!-- Outer wrapper forcing Jupyter to render the complete block height without clipping scrollbars -->
    <div style="display: block; overflow: visible; height: auto; padding-bottom: 10px;">
        
        <div style="background-color: #0f172a; padding: 20px; border-radius: 10px; width: 680px; font-family: monospace; color: #f1f5f9; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);">
            
            <!-- Interactive Constraints Control Panel -->
            <div style="margin-bottom: 15px; display: grid; grid-template-columns: 1fr 1fr; gap: 15px; font-size: 12px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <label for="mfp-m6" style="color: #cbd5e1; min-width: 120px;">Mean Free Path:</label>
                    <input type="range" id="mfp-m6" min="1" max="50" step="0.5" value="10" style="width: 120px;">
                    <span id="mfp-val-m6" style="color: #faf015; font-weight: bold;">10.0</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <label for="rays-m6" style="color: #cbd5e1; min-width: 120px;">Photons/Batch:</label>
                    <input type="range" id="rays-m6" min="10" max="300" step="10" value="150" style="width: 120px;">
                    <span id="rays-val-m6" style="color: #faf015; font-weight: bold;">150</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <label for="burn-m6" style="color: #cbd5e1; min-width: 120px;">Core Burn Batches:</label>
                    <input type="range" id="burn-m6" min="5" max="30" step="1" value="15" style="width: 120px;">
                    <span id="burn-val-m6" style="color: #faf015; font-weight: bold;">15</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <label for="speed-m6" style="color: #38bdf8; font-weight: bold; min-width: 120px;">Sim Speed:</label>
                    <input type="range" id="speed-m6" min="1" max="100" step="1" value="50" style="width: 120px;">
                    <span id="speed-val-m6" style="color: #faf015; font-weight: bold;">50%</span>
                </div>
            </div>
            
            <div style="margin-bottom: 15px;">
                <button id="start-btn-m6" style="background-color: #ef4444; color: white; border: none; padding: 8px 20px; border-radius: 4px; cursor: pointer; font-weight: bold; width: 100%;">Initiate Extinction Protocol</button>
            </div>

            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span style="color: #f43f5e; font-weight: bold; font-size: 15px;">Mode 6: Full-Frame Overlaid Extinction Dashboard</span>
                <span id="status-display-m6" style="color: #94a3b8; font-weight: bold;">Ready</span>
            </div>
            
            <!-- Full Frame Consolidated Workstation Area -->
            <div style="position: relative; width: 640px; height: 400px; background-color: #0f172a; border-radius: 8px; border: 1px solid #475569; overflow: hidden;">
                <canvas id="canvas-dashboard-m6" width="640" height="400" style="position: absolute; left: 0; top: 0; z-index: 1;"></canvas>
            </div>
            
            <!-- Statistical Laboratory Readout Desk -->
            <div id="stats-panel-m6" style="margin-top: 15px; padding: 12px; background-color: #0f172a; border: 1px solid #f43f5e; border-radius: 6px; font-size: 12px; line-height: 1.6; display: none;">
                <span style="color: #faf015; font-weight: bold; font-size: 13px;">Extinction Analysis Output Data:</span><br>
                • Total Simulated Photons: <span id="stat-total-m6" style="color: #38bdf8;">0</span> | Batches Generated Before Death: <span id="stat-burn-m6" style="color: #38bdf8;">0</span><br>
                • Core Extinction Event Time: <span id="stat-t-core-m6" style="color: #ef4444; font-weight: bold;">--</span> steps<br>
                • Half-Luminosity Decay Point: <span id="stat-t-half-m6" style="color: #f59e0b; font-weight: bold;">--</span> steps<br>
                • Surface Extinction Time (Sun Dies): <span id="stat-t-dead-m6" style="color: #64748b; font-weight: bold;">--</span> steps
            </div>
        </div>
    </div>
    """
    html_script = """
    <script>
    (function() {
        const canvas = document.getElementById('canvas-dashboard-m6'); const ctx = canvas.getContext('2d');
        const startBtn = document.getElementById('start-btn-m6'); const statusDisp = document.getElementById('status-display-m6'); const statsPanel = document.getElementById('stats-panel-m6');
        const sTotal = document.getElementById('stat-total-m6'); const sBurn = document.getElementById('stat-burn-m6');
        const sTCore = document.getElementById('stat-t-core-m6'); const sTHalf = document.getElementById('stat-t-half-m6'); const sTDead = document.getElementById('stat-t-dead-m6');
        const speedSlider = document.getElementById('speed-m6'); const speedVal = document.getElementById('speed-val-m6');

        const elements = ['mfp-m6', 'rays-m6', 'burn-m6'];
        elements.forEach(id => {
            const el = document.getElementById(id); const val = document.getElementById(id.replace('m6', 'val-m6'));
            if (el && val) el.addEventListener('input', () => { val.innerText = id.includes('mfp') ? parseFloat(el.value).toFixed(1) : el.value; });
        });
        speedSlider.addEventListener('input', () => { speedVal.innerText = speedSlider.value + '%'; });

        const cx = canvas.width / 2; const cy = canvas.height / 2;
        const sunRadius = 180; const sunRadiusSq = sunRadius * sunRadius;

        const graphLeft = 60; const graphRight = 580; const graphTop = 40; const graphBottom = 350;
        const graphWidth = graphRight - graphLeft; const graphHeight = graphBottom - graphTop;

        const PALETTE = ['#00aa00', '#00aaaa', '#aa0000', '#aa00aa', '#aa5500', '#aaaaaa', '#555555', '#5555ff', '#55ff55', '#55ffff', '#ff5555', '#ff55ff', '#ffff55', '#0000aa'];
        function getBatchColor(idx) { return PALETTE[(idx - 1) % PALETTE.length]; }

        let animationId; let globalPhotons = []; let escapeHistoryLog = [];
        let currentCollisionTick = 0; let fixedStepInterval = 25;
        let configRays = 0; let configBurnBatches = 0; let configMfp = 0;
        let activeGroupsCount = 0; let totalEscapedEver = 0;
        let coreIsDead = false; let maxSteadyStateLuminosity = 0;
        
        let tCoreDeath = 0; let tHalfBrightness = 0; let tSunExtinction = 0;

        ctx.fillStyle = '#0f172a'; ctx.fillRect(0, 0, canvas.width, canvas.height);
        drawOverlaidGrid(150 * 0.38);

        function drawOverlaidGrid(fixedLuminosityPeak) {
            ctx.strokeStyle = 'rgba(71, 85, 105, 0.4)'; ctx.lineWidth = 1;
            ctx.beginPath(); ctx.arc(cx, cy, sunRadius, 0, 2 * Math.PI); ctx.stroke();

            ctx.strokeStyle = '#64748b'; ctx.lineWidth = 1.5;
            ctx.beginPath(); ctx.moveTo(graphLeft, graphTop); ctx.lineTo(graphLeft, graphBottom); ctx.lineTo(graphRight, graphBottom); ctx.stroke();

            ctx.fillStyle = '#94a3b8'; ctx.font = '10px monospace';
            ctx.fillText("Photons Escaped / Interval", graphLeft + 10, graphTop - 15);
            ctx.fillText("Total Collisions (Time)", graphRight - 150, graphBottom + 25);

            let yScale = (graphHeight - 40) / fixedLuminosityPeak;
            let fullY = graphBottom - fixedLuminosityPeak * yScale;
            let halfY = graphBottom - (fixedLuminosityPeak * 0.5) * yScale;

            ctx.lineWidth = 1;
            ctx.strokeStyle = 'rgba(34, 197, 94, 0.5)';
            ctx.beginPath(); ctx.moveTo(graphLeft, fullY); ctx.lineTo(graphRight, fullY); ctx.stroke();
            ctx.fillStyle = '#22c55e'; ctx.fillText("Full Brightness (" + Math.round(fixedLuminosityPeak) + ")", graphLeft + 10, fullY - 4);

            ctx.strokeStyle = 'rgba(245, 158, 11, 0.5)';
            ctx.beginPath(); ctx.moveTo(graphLeft, halfY); ctx.lineTo(graphRight, halfY); ctx.stroke();
            ctx.fillStyle = '#f59e0b'; ctx.fillText("Half Brightness (" + Math.round(fixedLuminosityPeak * 0.5) + ")", graphLeft + 10, halfY - 4);

            let totalPossibleIntervals = Math.max(120, escapeHistoryLog.length);
            let xScale = graphWidth / totalPossibleIntervals;

            if (tCoreDeath > 0) {
                let cxG = graphLeft + (tCoreDeath / fixedStepInterval) * xScale;
                ctx.strokeStyle = 'rgba(239, 68, 68, 0.6)'; ctx.beginPath(); ctx.moveTo(cxG, graphTop); ctx.lineTo(cxG, graphBottom); ctx.stroke();
                ctx.fillStyle = '#ef4444'; ctx.fillText("Core Dies", cxG - 25, graphTop + 15);
            }
            if (tHalfBrightness > 0) {
                let hxG = graphLeft + (tHalfBrightness / fixedStepInterval) * xScale;
                ctx.strokeStyle = 'rgba(245, 158, 11, 0.6)'; ctx.beginPath(); ctx.moveTo(hxG, graphTop); ctx.lineTo(hxG, graphBottom); ctx.stroke();
                ctx.fillStyle = '#f59e0b'; ctx.fillText("1/2 Bright", hxG - 25, graphTop + 30);
            }
            if (tSunExtinction > 0) {
                let dxG = graphLeft + (tSunExtinction / fixedStepInterval) * xScale;
                ctx.strokeStyle = 'rgba(148, 163, 184, 0.7)'; ctx.beginPath(); ctx.moveTo(dxG, graphTop); ctx.lineTo(dxG, graphBottom); ctx.stroke();
                ctx.fillStyle = '#94a3b8'; ctx.fillText("Sun Dies", dxG - 25, graphTop + 45);
            }

            if (escapeHistoryLog.length > 0) {
                ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 2.5; ctx.beginPath();
                for (let i = 0; i < escapeHistoryLog.length; i++) {
                    let gx = graphLeft + i * xScale;
                    let gy = graphBottom - escapeHistoryLog[i] * yScale;
                    if (gy > graphBottom) gy = graphBottom;
                    if (i === 0) ctx.moveTo(gx, gy); else ctx.lineTo(gx, gy);
                }
                ctx.stroke();
            }

            ctx.fillStyle = '#64748b'; ctx.font = '9px monospace';
            let stepSpacing = Math.ceil(totalPossibleIntervals / 5);
            for (let i = 0; i <= totalPossibleIntervals; i += stepSpacing) {
                let tx = graphLeft + i * xScale;
                if (tx <= graphRight) ctx.fillText(i * fixedStepInterval, tx - 10, graphBottom + 12);
            }
        }

        startBtn.addEventListener('click', function() {
            cancelAnimationFrame(animationId);
            configRays = parseInt(document.getElementById('rays-m6').value);
            configBurnBatches = parseInt(document.getElementById('burn-m6').value);
            configMfp = parseFloat(document.getElementById('mfp-m6').value);
            
            globalPhotons = []; escapeHistoryLog = []; currentCollisionTick = 0;
            activeGroupsCount = 0; totalEscapedEver = 0; coreIsDead = false;
            tCoreDeath = 0; tHalfBrightness = 0; tSunExtinction = 0;

            maxSteadyStateLuminosity = configRays * 0.38; 
            if (maxSteadyStateLuminosity < 5) maxSteadyStateLuminosity = 5;
            
            statusDisp.innerText = "Core Burning..."; statusDisp.style.color = "#fbbf24";
            statsPanel.style.display = "block";
            sTCore.innerText = "--"; sTHalf.innerText = "--"; sTDead.innerText = "--";
            
            ctx.fillStyle = '#0f172a'; ctx.fillRect(0, 0, canvas.width, canvas.height);
            spawnNextBatchGroup(); engineLoop();
        });

        function spawnNextBatchGroup() {
            if (coreIsDead || activeGroupsCount >= configBurnBatches) return;
            activeGroupsCount++; let batchColor = getBatchColor(activeGroupsCount);
            for (let i = 0; i < configRays; i++) {
                globalPhotons.push({ x: 0, y: 0, inside: true, color: batchColor });
            }
        }

        function engineLoop() {
            let activePhotonsCount = 0;
            let escapesThisIntervalSegment = 0;
            const denom = 100 + 17 + (configMfp / 5.0) * (-4);

            const speedPct = parseInt(speedSlider.value);
            let intervalsToRun = speedPct >= 50 ? Math.floor((speedPct - 49) / 5) + 1 : 1;
            let delayLoops = speedPct < 50 ? Math.floor((50 - speedPct) / 3) : 0;

            for (let chunk = 0; chunk < intervalsToRun; chunk++) {
                if (coreIsDead && activePhotonsCount === 0) {
                    let insideRemaining = false;
                    for(let i=0; i<globalPhotons.length; i++) { if(globalPhotons[i].inside) { insideRemaining = true; break; } }
                    if(!insideRemaining && totalEscapedEver > 0) {
                        if(tSunExtinction === 0) {
                            tSunExtinction = currentCollisionTick; sTDead.innerText = tSunExtinction;
                            statusDisp.innerText = "Extinction Complete"; statusDisp.style.color = "#94a3b8";
                        }
                        break;
                    }
                }

                ctx.fillStyle = "rgba(15, 23, 42, 0.1)"; 
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                for (let iter = 0; iter < fixedStepInterval; iter++) {
                    currentCollisionTick++;
                    activePhotonsCount = 0;

                    for (let i = 0; i < globalPhotons.length; i++) {
                        let p = globalPhotons[i]; if (!p.inside) continue;
                        activePhotonsCount++;

                        let theta = Math.random() * 2 * Math.PI;
                        let stepR = (configMfp * Math.random() * 2) / denom * sunRadius;
                        let oldX = p.x, oldY = p.y, newX = oldX + stepR * Math.cos(theta), newY = oldY + stepR * Math.sin(theta);

                        if ((newX * newX + newY * newY) >= sunRadiusSq) {
                            p.inside = false; totalEscapedEver++; escapesThisIntervalSegment++;
                            ctx.strokeStyle = p.color; ctx.lineWidth = 1.2; ctx.beginPath(); ctx.moveTo(cx + oldX, cy + oldY);
                            ctx.lineTo(cx + 1.15 * newX, cy + 1.15 * newY); ctx.stroke();
                        } else {
                            ctx.strokeStyle = p.color; ctx.lineWidth = 0.8; ctx.beginPath(); ctx.moveTo(cx + oldX, cy + oldY);
                            ctx.lineTo(cx + newX, cy + newY); ctx.stroke();
                            p.x = newX; p.y = newY;
                        }
                    }

                    if (!coreIsDead && currentCollisionTick === (configBurnBatches * fixedStepInterval)) {
                        coreIsDead = true; tCoreDeath = currentCollisionTick;
                        sTCore.innerText = tCoreDeath; statusDisp.innerText = "Core Extinct. Decaying...";
                        statusDisp.style.color = "#f43f5e";
                    }

                    if (currentCollisionTick % fixedStepInterval === 0 && !coreIsDead) { spawnNextBatchGroup(); }
                }

                escapeHistoryLog.push(escapesThisIntervalSegment);
                escapesThisIntervalSegment = 0;
            }

            if (coreIsDead && tHalfBrightness === 0) {
                let targetIdx = Math.floor(tCoreDeath / fixedStepInterval);
                for (let i = targetIdx; i < escapeHistoryLog.length; i++) {
                    if (escapeHistoryLog[i] <= maxSteadyStateLuminosity * 0.5) {
                        tHalfBrightness = i * fixedStepInterval; sTHalf.innerText = tHalfBrightness; break;
                    }
                }
            }

            drawOverlaidGrid(maxSteadyStateLuminosity);

            sTotal.innerText = configRays * configBurnBatches;
            sBurn.innerText = coreIsDead ? configBurnBatches : activeGroupsCount;

            let systemIsActive = false;
            for(let i=0; i<globalPhotons.length; i++) { if(globalPhotons[i].inside) { systemIsActive = true; break; } }

            if (systemIsActive || !coreIsDead) {
                if (delayLoops > 0) {
                    setTimeout(() => { animationId = requestAnimationFrame(engineLoop); }, delayLoops * 15);
                } else {
                    animationId = requestAnimationFrame(engineLoop);
                }
            }
        }
    })();
    </script>
    """
    display(HTML(html_str + html_script))
