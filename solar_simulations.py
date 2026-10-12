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
        const canvas = document.getElementById('canvas-m2'); const ctx = canvas.getContext('2d');
        const startBtn = document.getElementById('start-btn-m2'); const statusDisp = document.getElementById('status-display-m2');
        const statsPanel = document.getElementById('stats-panel-m2'); const statEscaped = document.getElementById('stat-escaped-m2');
        const statStatusText = document.getElementById('stat-status-text-m2');
        const cx = canvas.width / 2; const cy = canvas.height / 2; const sunRadius = 200; const sunRadiusSq = sunRadius * sunRadius;
        const mfp = 1.0; const totalRays = 100;
        const PALETTE = ['#0000aa', '#00aa00', '#00aaaa', '#aa0000', '#aa00aa', '#aa5500', '#aaaaaa', '#555555', '#5555ff', '#55ff55', '#55ffff', '#ff5555', '#ff55ff', '#ffff55'];
        function getPhotonColor(idx) { return PALETTE[((idx - 1) % 13) + 1 % PALETTE.length]; }
        let animationFrameId; let photons = []; let escapedCount = 0;
        drawBackground();
        function drawBackground() {
            ctx.clearRect(0, 0, canvas.width, canvas.height); ctx.strokeStyle = '#475569'; ctx.lineWidth = 2;
            ctx.beginPath(); ctx.arc(cx, cy, sunRadius, 0, 2 * Math.PI); ctx.stroke();
        }
        startBtn.addEventListener('click', function() {
            cancelAnimationFrame(animationFrameId); drawBackground(); photons = []; escapedCount = 0;
            statusDisp.innerText = "Simulating Baseline..."; statusDisp.style.color = "#fa4c4c"; statsPanel.style.display = "block";
            statStatusText.innerText = "Processing random walk arrays..."; statStatusText.style.color = "#38bdf8";
            for (let i = 1; i <= totalRays; i++) { photons.push({ x: 0, y: 0, inside: true, color: getPhotonColor(i) }); }
            function getStepR() { const denom = 100 + 17 + (mfp / 5.0) * (-4); return (mfp * Math.random() * 2) / denom * sunRadius; }
            function introductionStep() {
                let activeParticles = false;
                for (let i = 0; i < photons.length; i++) {
                    let p = photons[i]; if (!p.inside) continue; activeParticles = true;
                    const theta = Math.random() * 2 * Math.PI; const stepR = getStepR();
                    let oldX = p.x; let oldY = p.y; let newX = oldX + stepR * Math.cos(theta); let newY = oldY + stepR * Math.sin(theta);
                    if ((newX * newX + newY * newY) >= sunRadiusSq) {
                        p.inside = false; escapedCount++;
                        const bVal = oldX * Math.cos(theta) + oldY * Math.sin(theta); const disc = sunRadiusSq - (oldX * oldX + oldY * oldY) + (bVal * bVal);
                        const root = disc >= 0 ? Math.sqrt(disc) : 0; let boundR = root - bVal; if (boundR < 0) boundR = -root - bVal;
                        const boundX = oldX + boundR * Math.cos(theta); const boundY = oldY + boundR * Math.sin(theta);
                        ctx.strokeStyle = p.color; ctx.lineWidth = 1.0; ctx.beginPath(); ctx.moveTo(cx + oldX, cy + oldY); ctx.lineTo(cx + boundX, cy + boundY); ctx.stroke();
                        ctx.beginPath(); ctx.moveTo(cx + boundX, cy + boundY); ctx.lineTo(cx + 1.2 * boundX, cy + 1.2 * boundY); ctx.stroke();
                    } else {
                        ctx.strokeStyle = p.color; ctx.lineWidth = 1.0; ctx.beginPath(); ctx.moveTo(cx + oldX, cy + oldY); ctx.lineTo(cx + newX, cy + newY); ctx.stroke();
                        p.x = newX; p.y = newY;
                    }
                }
                statEscaped.innerText = escapedCount;
                if (activeParticles && escapedCount < totalRays) { animationFrameId = requestAnimationFrame(introductionStep); }
                else { statusDisp.innerText = "Demo Complete!"; statusDisp.style.color = "#85ff55"; statStatusText.innerText = "All introductory rays cleared boundary grid successfully."; statStatusText.style.color = "#22c55e"; }
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
        const canvas = document.getElementById('canvas'); const ctx = canvas.getContext('2d');
        const slider = document.getElementById('mfp-range'); const sliderVal = document.getElementById('mfp-val');
        const startBtn = document.getElementById('start-btn'); const statusDisp = document.getElementById('status-display');
        const statsPanel = document.getElementById('stats-panel'); const statSteps = document.getElementById('stat-steps');
        const statDist = document.getElementById('stat-dist');
        const cx = canvas.width / 2; const cy = canvas.height / 2; const sunRadius = 200; const sunRadiusSq = sunRadius * sunRadius;
        let animationFrameId;
        drawBackground();
        slider.addEventListener('input', function() { sliderVal.innerText = parseFloat(slider.value).toFixed(1); });
        function drawBackground() {
            ctx.clearRect(0, 0, canvas.width, canvas.height); ctx.strokeStyle = '#475569'; ctx.lineWidth = 2;
            ctx.beginPath(); ctx.arc(cx, cy, sunRadius, 0, 2 * Math.PI); ctx.stroke();
        }
        startBtn.addEventListener('click', function() {
            cancelAnimationFrame(animationFrameId); drawBackground();
            let posX = 0, posY = 0; let totalDistance = 0; let stepCount = 0; const mfp = parseFloat(slider.value);
            statusDisp.innerText = "Simulating..."; statusDisp.style.color = "#fa4c4c"; statsPanel.style.display = "none";
function getStepR() { const denom = 100 + 17 + (mfp / 5.0) * (-4); return (mfp * Math.random() * 2) / denom * sunRadius; }
function simulationStep() {
const theta = Math.random() * 2 * Math.PI; const stepR = getStepR();
let oldX = posX; let oldY = posY; let newX = oldX + stepR * Math.cos(theta); let newY = oldY + stepR * Math.sin(theta);
totalDistance += stepR; stepCount++;
if ((newX * newX + newY * newY) >= sunRadiusSq) {
const bVal = oldX * Math.cos(theta) + oldY * Math.sin(theta); const disc = sunRadiusSq - (oldX * oldX + oldY * oldY) + (bVal * bVal);
const root = disc >= 0 ? Math.sqrt(disc) : 0; let boundR = root - bVal; if (boundR < 0) boundR = -root - bVal;
const boundX = oldX + boundR * Math.cos(theta); const boundY = oldY + boundR * Math.sin(theta);
ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.moveTo(cx + oldX, cy + oldY); ctx.lineTo(cx + boundX, cy + boundY); ctx.stroke();
ctx.strokeStyle = '#fa4c4c'; ctx.beginPath(); ctx.moveTo(cx + boundX, cy + boundY); ctx.lineTo(cx + 2 * boundX, cy + 2 * boundY); ctx.stroke();
statusDisp.innerText = "Escaped!"; statusDisp.style.color = "#85ff55";
statSteps.innerText = stepCount; statDist.innerText = ((totalDistance / sunRadius) * 100).toFixed(2);
statsPanel.style.display = "block"; return;
}
ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.moveTo(cx + oldX, cy + oldY); ctx.lineTo(cx + newX, cy + newY); ctx.stroke();
posX = newX; posY = newY; animationFrameId = requestAnimationFrame(simulationStep);
}
simulationStep();
});
})();

"""
display(HTML(html_str))
def run_multi_photon():
"""Mode 4: Simultaneously tracks a multiple photon cluster swarm (up to 2,000 photons)."""
html_str = """


Mean Free Path (L):
10.0

Photons (Max 2000):
100



Spawn Photon Swarm


Gamma Ray Multiple Photon Swarm
Ready





Swarm Statistics:

• Total Photons Simulated: 0

• Escaped Photons: 0 / 0

• Swarm Average Collisions: 0



(function() {
const canvas = document.getElementById('canvas-m4'); const ctx = canvas.getContext('2d');
const mfpSlider = document.getElementById('mfp-range-m4'); const mfpVal = document.getElementById('mfp-val-m4');
const raysSlider = document.getElementById('rays-range-m4'); const raysVal = document.getElementById('rays-val-m4');
const startBtn = document.getElementById('start-btn-m4'); const statusDisp = document.getElementById('status-display-m4');
const statsPanel = document.getElementById('stats-panel-m4');
const statTotal = document.getElementById('stat-total-m4'); const statEscaped = document.getElementById('stat-escaped-m4');
const statTarget = document.getElementById('stat-target-m4'); const statAvgColl = document.getElementById('stat-avg-coll-m4');
const cx = canvas.width / 2; const cy = canvas.height / 2; const sunRadius = 200; const sunRadiusSq = sunRadius * sunRadius;
const PALETTE = ['#0000aa', '#00aa00', '#00aaaa', '#aa0000', '#aa00aa', '#aa5500', '#aaaaaa', '#555555', '#5555ff', '#55ff55', '#55ffff', '#ff5555', '#ff55ff', '#ffff55', '#ffffff'];
function getPhotonColor(index) { let mappedIdx = ((index - 1) % 13) + 1; return PALETTE[mappedIdx % PALETTE.length]; }
let animationFrameId; let photons = []; let totalRays = 0; let escapedCount = 0; let totalCollisionsEver = 0;
drawBackground();
mfpSlider.addEventListener('input', () => mfpVal.innerText = parseFloat(mfpSlider.value).toFixed(1));
raysSlider.addEventListener('input', () => raysVal.innerText = parseInt(raysSlider.value));
function drawBackground() {
ctx.clearRect(0, 0, canvas.width, canvas.height); ctx.strokeStyle = '#475569'; ctx.lineWidth = 2;
ctx.beginPath(); ctx.arc(cx, cy, sunRadius, 0, 2 * Math.PI); ctx.stroke();
}
startBtn.addEventListener('click', function() {
cancelAnimationFrame(animationFrameId); drawBackground(); totalRays = parseInt(raysSlider.value); const mfp = parseFloat(mfpSlider.value);
photons = []; escapedCount = 0; totalCollisionsEver = 0;
statusDisp.innerText = "Simulating Swarm..."; statusDisp.style.color = "#fa4c4c"; statsPanel.style.display = "none";
for (let i = 1; i <= totalRays; i++) { photons.push({ id: i, x: 0, y: 0, inside: true, collisions: 0, color: getPhotonColor(i) }); }
function getStepR() { const denom = 100 + 17 + (mfp / 5.0) * (-4); return (mfp * Math.random() * 2) / denom * sunRadius; }
function swarmStep() {
let activeThisFrame = false;
for (let i = 0; i < photons.length; i++) {
let p = photons[i]; if (!p.inside) continue; activeThisFrame = true;
const theta = Math.random() * 2 * Math.PI; const stepR = getStepR();
let oldX = p.x; let oldY = p.y; let newX = oldX + stepR * Math.cos(theta); let newY = oldY + stepR * Math.sin(theta);
p.collisions++; totalCollisionsEver++;
if ((newX * newX + newY * newY) >= sunRadiusSq) {
p.inside = false; escapedCount++;
const bVal = oldX * Math.cos(theta) + oldY * Math.sin(theta); const disc = sunRadiusSq - (oldX * oldX + oldY * oldY) + (bVal * bVal);
const root = disc >= 0 ? Math.sqrt(disc) : 0; let boundR = root - bVal; if (boundR < 0) boundR = -root - bVal;
const boundX = oldX + boundR * Math.cos(theta); const boundY = oldY + boundR * Math.sin(theta);
ctx.strokeStyle = p.color; ctx.lineWidth = 1.0; ctx.beginPath(); ctx.moveTo(cx + oldX, cy + oldY); ctx.lineTo(cx + boundX, cy + boundY); ctx.stroke();
ctx.beginPath(); ctx.moveTo(cx + boundX, cy + boundY); ctx.lineTo(cx + 1.3 * boundX, cy + 1.3 * boundY); ctx.stroke();
} else {
ctx.strokeStyle = p.color; ctx.lineWidth = 1.0; ctx.beginPath(); ctx.moveTo(cx + oldX, cy + oldY); ctx.lineTo(cx + newX, cy + newY); ctx.stroke();
p.x = newX; p.y = newY;
}
}
statTotal.innerText = totalRays; statEscaped.innerText = escapedCount; statTarget.innerText = totalRays;
statAvgColl.innerText = (totalCollisionsEver / totalRays).toFixed(1); statsPanel.style.display = "block";
if (activeThisFrame && escapedCount < totalRays) { animationFrameId = requestAnimationFrame(swarmStep); }
else { statusDisp.innerText = "All Escaped!"; statusDisp.style.color = "#85ff55"; }
}
swarmStep();
});
})();

"""
display(HTML(html_str))
def run_batches_and_dying_sun():
"""Modes 5 & 6: Unified core batch tracker tracking spatial decay release arrays alongside live histogram graph."""
html_str = """


Mean Free Path:10.0
Photons/Batch:50
Total Batches:10
Step Interval:20

Run Batches
Solar Core Batch Release ProfileReady

Spatial Tracker
Escape Distribution Profile (Histogram)


Advanced Batch Metrics:

• Total Simulated Photons: 0 | Active Batches Deployed: 0

• Escaped Population Count: 0 / 0

• Grand Total Calculations Completed: 0



(function() {
const cSpatial = document.getElementById('canvas-spatial-m5'); const ctxS = cSpatial.getContext('2d');
const { id } = { id: "canvas-graph-m5" }; const cGraph = document.getElementById('canvas-graph-m5'); const ctxG = cGraph.getContext('2d');
const sliders = ['mfp-m5', 'rays-m5', 'groups-m5', 'interval-m5'];
sliders.forEach(id => {
const input = document.getElementById(id); const output = document.getElementById(id.replace('range', 'val').replace('m5', 'val-m5'));
if (input && output) { input.addEventListener('input', () => { output.innerText = id.includes('mfp') ? parseFloat(input.value).toFixed(1) : input.value; }); }
});
const startBtn = document.getElementById('start-btn-m5'); const statusDisp = document.getElementById('status-display-m5'); const statsPanel = document.getElementById('stats-panel-m5');
const sTotal = document.getElementById('stat-total-m5'); const sDeployed = document.getElementById('stat-deployed-m5'); const sEscaped = document.getElementById('stat-escaped-m5'); const sTarget = document.getElementById('stat-target-m5'); const sColl = document.getElementById('stat-total-coll-m5');
const sunRadius = 110; const sunRadiusSq = sunRadius * sunRadius; const cx = cSpatial.width / 2; const cy = cSpatial.height / 2;
const PALETTE = ['#0000aa', '#00aa00', '#00aaaa', '#aa0000', '#aa00aa', '#aa5500', '#aaaaaa', '#555555', '#5555ff', '#55ff55', '#55ffff', '#ff5555', '#ff55ff', '#ffff55'];
function getGroupColor(idx) { return PALETTE[idx % PALETTE.length]; }
let animationId; let globalPhotons = []; let escapeHistoryLog = []; let currentCollisionTick = 0;
let configRays = 0; let configGroups = 0; let configInterval = 0; let configMfp = 0;
let activeGroupsCount = 0; let totalEscapedEver = 0; let grandTotalCollisions = 0;
resetDisplays();
function resetDisplays() {
ctxS.clearRect(0, 0, cSpatial.width, cSpatial.height); ctxS.strokeStyle = '#475569'; ctxS.lineWidth = 1.5;
ctxS.beginPath(); ctxS.arc(cx, cy, sunRadius, 0, 2 * Math.PI); ctxS.stroke();
ctxG.clearRect(0, 0, cGraph.width, cGraph.height); ctxG.strokeStyle = '#334155'; ctxG.lineWidth = 1;
ctxG.beginPath(); ctxG.moveTo(40, 10); ctxG.lineTo(40, 140); ctxG.lineTo(580, 140); ctxG.stroke();
}
startBtn.addEventListener('click', function() {
cancelAnimationFrame(animationId);
configRays = parseInt(document.getElementById('rays-m5').value); configGroups = parseInt(document.getElementById('groups-m5').value);
configInterval = parseInt(document.getElementById('interval-m5').value); configMfp = parseFloat(document.getElementById('mfp-m5').value);
globalPhotons = []; escapeHistoryLog = new Array(100).fill(0); currentCollisionTick = 0; activeGroupsCount = 0; totalEscapedEver = 0; grandTotalCollisions = 0;
statusDisp.innerText = "Processing Cycles..."; statusDisp.style.color = "#fa4c4c"; statsPanel.style.display = "block";
resetDisplays(); spawnNextBatchGroup(); engineLoop();
});
function spawnNextBatchGroup() {
if (activeGroupsCount >= configGroups) return; activeGroupsCount++; let color = getGroupColor(activeGroupsCount);
for (let i = 0; i < configRays; i++) { globalPhotons.push({ x: 0, y: 0, inside: true, color: color, groupOwner: activeGroupsCount }); }
}
function drawDistributionHistogram() {
ctxG.clearRect(0, 0, cGraph.width, cGraph.height); ctxG.strokeStyle = '#334155'; ctxG.lineWidth = 1; ctxG.beginPath(); ctxG.moveTo(40, 10); ctxG.lineTo(40, 140); ctxG.lineTo(580, 140); ctxG.stroke();
ctxG.fillStyle = '#94a3b8'; ctxG.font = '9px monospace'; ctxG.fillText("Escapes", 2, 15); ctxG.fillText("Collision Timesteps", 480, 152);
let maxEscapedVal = Math.max(...escapeHistoryLog, 10); let barWidth = 500 / escapeHistoryLog.length; ctxG.fillStyle = '#38bdf8';
for (let i = 0; i < escapeHistoryLog.length; i++) {
let val = escapeHistoryLog[i]; if (val === 0) continue; let barHeight = (val / maxEscapedVal) * 115; let bx = 42 + i * barWidth; let by = 140 - barHeight; ctxG.fillRect(bx, by, barWidth - 1, barHeight);
}
}
function engineLoop() {
let calculationsCompletedThisFrame = 0; let escapesRecordedInThisStep = 0; const denom = 100 + 17 + (configMfp / 5.0) * (-4);
for (let iter = 0; iter < configInterval; iter++) {
currentCollisionTick++; let stepEscapes = 0;
for (let i = 0; i < globalPhotons.length; i++) {
let p = globalPhotons[i]; if (!p.inside) continue; calculationsCompletedThisFrame++; grandTotalCollisions++;
let theta = Math.random() * 2 * Math.PI; let stepR = (configMfp * Math.random() * 2) / denom * sunRadius;
let oldX = p.x; let oldY = p.y; let newX = oldX + stepR * Math.cos(theta); let newY = oldY + stepR * Math.sin(theta);
if ((newX * newX + newY * newY) >= sunRadiusSq) { p.inside = false; totalEscapedEver++; stepEscapes++; ctxS.strokeStyle = p.color; ctxS.lineWidth = 1; ctxS.beginPath(); ctxS.moveTo(cx + oldX, cy + oldY); ctxS.lineTo(cx + 1.1 * newX, cy + 1.1 * newY); ctxS.stroke(); }
else { p.x = newX; p.y = newY; }
}
let profileIndex = Math.floor(currentCollisionTick / configInterval); if (profileIndex < escapeHistoryLog.length) { escapeHistoryLog[profileIndex] += stepEscapes; }
if (currentCollisionTick % configInterval === 0 && activeGroupsCount < configGroups) { spawnNextBatchGroup(); }
}
drawDistributionHistogram();
let totalTargetPopulation = configRays * configGroups; sTotal.innerText = totalTargetPopulation; sDeployed.innerText = activeGroupsCount; sEscaped.innerText = totalEscapedEver; sTarget.innerText = totalTargetPopulation; sColl.innerText = grandTotalCollisions;
if (calculationsCompletedThisFrame > 0 || activeGroupsCount < configGroups) { animationId = requestAnimationFrame(engineLoop); }
else { statusDisp.innerText = "All Batches Clear!"; statusDisp.style.color = "#85ff55"; }
}
})();

"""
display(HTML(html_str))
