document.addEventListener('DOMContentLoaded', () => {
    // 1. Sidebar Active State Handling Based on URL
    const currentLocation = location.pathname.split("/").pop();
    const navLinks = document.querySelectorAll('.sidebar-nav a');
    
    navLinks.forEach(link => {
        const linkHref = link.getAttribute('href');
        if (linkHref === currentLocation || (currentLocation === '' && linkHref === 'index.html')) {
            document.querySelectorAll('.sidebar-nav li').forEach(nav => nav.classList.remove('active'));
            link.parentElement.classList.add('active');
        }
    });

    // 2. Animate Progress Bars on Load
    const progressBars = document.querySelectorAll('.progress-bar, .path-progress-bar');
    progressBars.forEach(bar => {
        const targetWidth = bar.style.width;
        bar.style.width = '0%';
        setTimeout(() => {
            bar.style.transition = 'width 1.5s cubic-bezier(0.2, 0.8, 0.2, 1)';
            bar.style.width = targetWidth;
        }, 300);
    });

    // 3. CTA Button Interaction (Mission Start)
    const ctaBtns = document.querySelectorAll('.cta-button');
    ctaBtns.forEach(ctaBtn => {
        ctaBtn.addEventListener('click', function(e) {
            e.preventDefault();
            if(this.classList.contains('loading')) return;
            
            const originalText = this.innerHTML;
            this.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Memuat...';
            this.style.opacity = '0.8';
            this.classList.add('loading');
            
            setTimeout(() => {
                this.innerHTML = 'Misi Dimulai <i class="fa-solid fa-check"></i>';
                this.style.background = 'var(--accent-green)';
                this.style.color = 'white';
                this.style.opacity = '1';
                
                showToast('Misi berhasil dimulai! +10 XP', 'success');

                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.style.background = '';
                    this.style.color = '';
                    this.classList.remove('loading');
                }, 2000);
            }, 1000);
        });
    });

    // 4. Badge Hover Micro-interaction
    const badges = document.querySelectorAll('.badge-item.earned');
    badges.forEach(badge => {
        badge.addEventListener('mouseenter', function() {
            this.style.transform = `scale(1.15) rotate(${Math.random() * 10 - 5}deg)`;
            this.style.filter = 'drop-shadow(0 0 10px rgba(138, 43, 226, 0.6))';
        });
        badge.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1) rotate(0deg)';
            this.style.filter = '';
        });
        
        badge.addEventListener('click', function() {
            showToast('Badge Spesial! Terus pertahankan kerjamu.', 'info');
        });
    });

    // 5. Module Click Interaction (Simulate completing a module)
    const activeModules = document.querySelectorAll('.module-item.active');
    activeModules.forEach(mod => {
        mod.addEventListener('click', function() {
            if(this.classList.contains('processing')) return;
            this.classList.add('processing');
            
            const icon = this.querySelector('.module-icon i');
            const status = this.querySelector('.module-status');
            
            icon.className = 'fa-solid fa-spinner fa-spin';
            status.innerText = 'Memproses...';
            
            setTimeout(() => {
                this.classList.remove('active', 'processing');
                this.classList.add('completed');
                icon.className = 'fa-solid fa-check';
                status.innerText = 'Selesai';
                
                showToast('Modul diselesaikan! +50 XP', 'success');
                
                // Animate progress bar locally if on index
                const pBar = document.querySelector('.path-progress-bar');
                if(pBar) {
                    pBar.style.width = '66%';
                    document.querySelector('.path-progress-text').innerText = '66% Selesai';
                }
            }, 1500);
        });
    });

    // 6. Interactive Toast Notification System
    function showToast(message, type = 'info') {
        let toastContainer = document.querySelector('.toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.className = 'toast-container';
            document.body.appendChild(toastContainer);
            
            // Add basic styles for toast container
            const style = document.createElement('style');
            style.innerHTML = `
                .toast-container { position: fixed; bottom: 20px; right: 20px; z-index: 9999; display: flex; flex-direction: column; gap: 10px; }
                .toast { padding: 15px 25px; border-radius: 12px; color: white; font-weight: 500; font-size: 0.95rem; backdrop-filter: blur(10px); transform: translateX(120%); transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55); display: flex; align-items: center; gap: 10px; box-shadow: 0 10px 20px rgba(0,0,0,0.2); }
                .toast.show { transform: translateX(0); }
                .toast.success { background: rgba(39, 174, 96, 0.9); border: 1px solid #2ecc71; }
                .toast.info { background: rgba(138, 43, 226, 0.9); border: 1px solid #9b59b6; }
            `;
            document.head.appendChild(style);
        }

        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        const icon = type === 'success' ? '<i class="fa-solid fa-circle-check"></i>' : '<i class="fa-solid fa-bell"></i>';
        toast.innerHTML = `${icon} <span>${message}</span>`;
        
        toastContainer.appendChild(toast);
        
        // Trigger reflow and show
        setTimeout(() => toast.classList.add('show'), 10);
        
        // Hide and remove after 3 seconds
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 400);
        }, 3000);
    }

    // 7. Page Transition Effect
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s ease';
    setTimeout(() => { document.body.style.opacity = '1'; }, 100);

    const allLinks = document.querySelectorAll('a:not([target="_blank"])');
    allLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if(href && href !== '#' && href.indexOf('http') !== 0) {
                e.preventDefault();
                document.body.style.opacity = '0';
                setTimeout(() => {
                    window.location.href = href;
                }, 400);
            } else if (href === '#') {
                e.preventDefault(); // Prevent jump to top for empty links
                showToast('Fitur ini masih dalam tahap pengembangan.', 'info');
            }
        });
    });

    // 8. Streak Daily Click
    const streakCard = document.querySelector('.streak-card');
    if(streakCard) {
        streakCard.addEventListener('click', () => {
            showToast('Streak harianmu: 14 Hari! Jangan menyerah!', 'success');
        });
        streakCard.style.cursor = 'pointer';
    }
});
