document.addEventListener('DOMContentLoaded', () => {
    // Tab switching logic
    const navItems = document.querySelectorAll('.nav-item');
    const tabPanels = document.querySelectorAll('.tab-panel');

    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const targetTab = item.getAttribute('data-tab');
            
            navItems.forEach(nav => nav.classList.remove('active'));
            tabPanels.forEach(panel => panel.classList.remove('active'));
            
            item.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
        });
    });

    // Sample data load simulation
    const sampleRecords = [
        { id: 'FR-001', title: 'Liberté de Delacroix', desc: 'Marianne dinâmica empunhando bandeira nos barricadas.', scores: [0, 0, 1, 0, 1, 0, 1, 2, 2, 2], regime: 'FUNDACIONAL' },
        { id: 'FR-007', title: '3e Emprunt (Lelong)', desc: 'Marianne petrificada como estátua acima das tropas.', scores: [2, 3, 2, 2, 2, 1, 2, 3, 3, 3], regime: 'MILITAR' },
        { id: 'FR-009', title: 'Buste de Marianne (Cívico)', desc: 'Busto oficial dessexualizado e padronizado em selos/muretas.', scores: [3, 3, 3, 3, 2, 2, 3, 3, 3, 3], regime: 'NORMATIVO' },
        { id: 'FR-005', title: 'La République aimable (Rops)', desc: 'Caricatura grotesca de Marianne, mão na cintura.', scores: [0, 1, 0, 0, 1, 0, 0, 2, 1, 1], regime: 'CONTRA-ALEGORIA' }
    ];

    // Load sample buttons
    const selectElement = document.getElementById('sample-loader');
    if (selectElement) {
        sampleRecords.forEach((rec, idx) => {
            const btn = document.createElement('button');
            btn.className = 'btn';
            btn.style.padding = '0.4rem 0.8rem';
            btn.style.fontSize = '0.85rem';
            btn.style.marginRight = '0.5rem';
            btn.style.marginBottom = '0.5rem';
            btn.innerText = rec.id + ' (' + rec.regime.toLowerCase() + ')';
            btn.onclick = () => loadRecord(rec);
            selectElement.appendChild(btn);
        });
    }

    function loadRecord(rec) {
        rec.scores.forEach((score, idx) => {
            const input = document.getElementById(`ind-${idx + 1}`);
            if (input) {
                input.value = score;
                const valDisp = document.getElementById(`ind-val-${idx + 1}`);
                if (valDisp) valDisp.innerText = score;
            }
        });
        calculateScore();
    }

    // Calculator live update logic
    const inputs = document.querySelectorAll('.ind-slider');
    inputs.forEach(input => {
        input.addEventListener('input', (e) => {
            const idx = e.target.id.split('-')[1];
            const display = document.getElementById(`ind-val-${idx}`);
            if (display) {
                display.innerText = e.target.value;
            }
            calculateScore();
        });
    });

    function calculateScore() {
        let total = 0;
        let count = 0;
        
        inputs.forEach(input => {
            total += parseFloat(input.value);
            count++;
        });

        const score = total / count;
        const formatted = score.toFixed(2);
        
        // Update display numbers
        const scoreNumEl = document.getElementById('score-num');
        if (scoreNumEl) scoreNumEl.innerText = formatted;

        // Update radial progress bar
        // Circle circumference is 2 * PI * 90 = 565.48
        const circle = document.querySelector('.radial-bar');
        if (circle) {
            const maxScore = 3.00;
            const percentage = score / maxScore;
            const offset = 565.48 - (percentage * 565.48);
            circle.style.strokeDashoffset = offset;
        }

        // Determine matching regime visually
        const regimeEl = document.getElementById('regime-tag');
        if (regimeEl) {
            let regime = 'FUNDACIONAL';
            
            // Heuristics for demo calculator matching regimes
            if (score >= 1.90) {
                regime = 'NORMATIVO';
            } else if (score >= 1.40) {
                regime = 'MILITAR';
            } else {
                regime = 'FUNDACIONAL';
            }

            // Check if user specifically lowered indicators indicative of Contra-alegoria
            const desincorporacao = parseInt(document.getElementById('ind-1').value);
            const rigidez = parseInt(document.getElementById('ind-2').value);
            if (desincorporacao === 0 && rigidez === 0 && score < 1.0) {
                regime = 'CONTRA-ALEGORIA';
            }

            regimeEl.innerText = regime;
        }
    }

    // Initial calculation
    calculateScore();

    // Repertoire / Testimony Submission
    const testimonyForm = document.getElementById('testimony-form');
    const testimonyContainer = document.getElementById('testimony-list-container');

    // Seed data
    const initialTestimonies = [
        { author: 'Lúcia M. (Liderança de Coletivo)', time: '2026-05-18 14:32', content: 'Olhar para este selo oficial de Marianne no busto recortado me faz perceber que a purificação do Estado atua justamente removendo a capacidade de movimento do corpo. A estátua é bonita, mas não tem pernas para correr ou lutar conosco nos cortiços.' },
        { author: 'Profa. Dra. Elaine Ramos (UFSC)', time: '2026-05-19 11:10', content: 'A inclusão da tese de vocês como itens 166-169 fecha o circuito. É o único jeito de ser metodologicamente honesto. Se a tese não codificasse a si mesma, a crítica à iconocracia alheia pareceria uma pretensão de soberania visual isolada.' }
    ];

    function renderTestimonies() {
        if (!testimonyContainer) return;
        testimonyContainer.innerHTML = '';
        initialTestimonies.forEach(t => {
            const card = document.createElement('div');
            card.className = 'testimony-card';
            card.innerHTML = `
                <div class="testimony-header">
                    <span class="testimony-author">${t.author}</span>
                    <span class="testimony-time">${t.time}</span>
                </div>
                <div class="testimony-content">${t.content}</div>
            `;
            testimonyContainer.appendChild(card);
        });
    }

    if (testimonyForm) {
        testimonyForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const authorInput = document.getElementById('test-author');
            const contentInput = document.getElementById('test-content');
            
            if (authorInput && contentInput && authorInput.value.trim() && contentInput.value.trim()) {
                const now = new Date();
                const timeStr = now.toISOString().slice(0, 16).replace('T', ' ');
                
                initialTestimonies.unshift({
                    author: authorInput.value.trim(),
                    time: timeStr,
                    content: contentInput.value.trim()
                });
                
                authorInput.value = '';
                contentInput.value = '';
                
                renderTestimonies();
                updateRepertoireCounter();
            }
        });
    }

    function updateRepertoireCounter() {
        const countEl = document.getElementById('repertoire-count');
        if (countEl) {
            countEl.innerText = `${initialTestimonies.length} registros ativos`;
        }
    }

    renderTestimonies();
    updateRepertoireCounter();
});
