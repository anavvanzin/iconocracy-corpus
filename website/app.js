/* app.js — Ius Gentium Interactive Features */

(function () {
  'use strict';

  /* ========================================
     MOBILE MENU TOGGLE
     ======================================== */
  const hamburger = document.querySelector('.hamburger');
  const mobileNav = document.querySelector('.mobile-nav');

  if (hamburger && mobileNav) {
    hamburger.addEventListener('click', () => {
      hamburger.classList.toggle('active');
      mobileNav.classList.toggle('active');
      document.body.style.overflow = mobileNav.classList.contains('active') ? 'hidden' : '';
    });

    // Close on link click
    mobileNav.querySelectorAll('.mobile-nav__link').forEach(link => {
      link.addEventListener('click', () => {
        hamburger.classList.remove('active');
        mobileNav.classList.remove('active');
        document.body.style.overflow = '';
      });
    });
  }

  /* ========================================
     STICKY HEADER SHADOW ON SCROLL
     ======================================== */
  const header = document.querySelector('.header');
  if (header) {
    let lastScroll = 0;
    window.addEventListener('scroll', () => {
      const currentScroll = window.scrollY;
      if (currentScroll > 20) {
        header.classList.add('header--scrolled');
      } else {
        header.classList.remove('header--scrolled');
      }
      lastScroll = currentScroll;
    }, { passive: true });
  }

  /* ========================================
     SMOOTH SCROLL FOR ANCHOR LINKS
     ======================================== */
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const id = anchor.getAttribute('href');
      if (id === '#') return;
      const target = document.querySelector(id);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  /* ========================================
     SCROLL REVEAL ANIMATIONS
     ======================================== */
  const revealElements = document.querySelectorAll('.reveal, .reveal-stagger');
  if (revealElements.length > 0) {
    const revealObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          revealObserver.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.1,
      rootMargin: '0px 0px -40px 0px'
    });

    revealElements.forEach(el => revealObserver.observe(el));
  }

  /* ========================================
     BACK TO TOP BUTTON
     ======================================== */
  const backToTop = document.querySelector('.back-to-top');
  if (backToTop) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 500) {
        backToTop.classList.add('visible');
      } else {
        backToTop.classList.remove('visible');
      }
    }, { passive: true });

    backToTop.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* ========================================
     MEMBER FILTER (pessoas.html)
     ======================================== */
  const memberFilterBtns = document.querySelectorAll('.filter-btn[data-member-filter]');
  const memberCards = document.querySelectorAll('.member-card[data-category]');

  if (memberFilterBtns.length > 0 && memberCards.length > 0) {
    memberFilterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        // Update active state
        memberFilterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        const filter = btn.dataset.memberFilter;

        memberCards.forEach(card => {
          const categories = card.dataset.category.split(',').map(c => c.trim());
          if (filter === 'todos' || categories.includes(filter)) {
            card.style.display = '';
            card.style.opacity = '0';
            card.style.transform = 'translateY(12px)';
            requestAnimationFrame(() => {
              card.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
              card.style.opacity = '1';
              card.style.transform = 'translateY(0)';
            });
          } else {
            card.style.display = 'none';
          }
        });
      });
    });
  }

  /* ========================================
     STUDY GROUP FILTER (pesquisa.html)
     ======================================== */
  const groupFilterBtns = document.querySelectorAll('.filter-btn[data-group-year]');
  const groupSearch = document.querySelector('#group-search');
  const groupCards = document.querySelectorAll('.group-card[data-year]');

  function filterGroups() {
    const activeYear = document.querySelector('.filter-btn[data-group-year].active');
    const yearFilter = activeYear ? activeYear.dataset.groupYear : 'todos';
    const searchTerm = groupSearch ? groupSearch.value.toLowerCase() : '';

    groupCards.forEach(card => {
      const matchYear = yearFilter === 'todos' || card.dataset.year === yearFilter;
      const matchSearch = !searchTerm || card.textContent.toLowerCase().includes(searchTerm);
      card.style.display = (matchYear && matchSearch) ? '' : 'none';
    });
  }

  if (groupFilterBtns.length > 0) {
    groupFilterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        groupFilterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        filterGroups();
      });
    });
  }

  if (groupSearch) {
    groupSearch.addEventListener('input', filterGroups);
  }

  /* ========================================
     STUDY GROUP FILTER - SELECT DROPDOWN (pesquisa.html)
     ======================================== */
  const yearSelect = document.querySelector('#yearFilter');
  const searchInput = document.querySelector('#searchInput');
  const groupCardsAll = document.querySelectorAll('.group-card[data-year]');

  function filterGroupsDropdown() {
    const yearFilter = yearSelect ? yearSelect.value : 'todos';
    const searchTerm = searchInput ? searchInput.value.toLowerCase() : '';

    groupCardsAll.forEach(card => {
      const matchYear = yearFilter === 'todos' || card.dataset.year === yearFilter;
      const matchSearch = !searchTerm || card.textContent.toLowerCase().includes(searchTerm);
      card.style.display = (matchYear && matchSearch) ? '' : 'none';
    });
  }

  if (yearSelect) {
    yearSelect.addEventListener('change', filterGroupsDropdown);
  }

  if (searchInput) {
    searchInput.addEventListener('input', filterGroupsDropdown);
  }

  /* ========================================
     PUBLICATION FILTER (producao.html)
     ======================================== */
  const pubFilterBtns = document.querySelectorAll('.filter-btn[data-pub-type]');
  const pubYearBtns = document.querySelectorAll('.filter-btn[data-pub-year]');
  const pubSearch = document.querySelector('#pub-search');
  const pubRows = document.querySelectorAll('.pub-table tbody tr[data-type]');

  function filterPubs() {
    const activeType = document.querySelector('.filter-btn[data-pub-type].active');
    const activeYear = document.querySelector('.filter-btn[data-pub-year].active');
    const typeFilter = activeType ? activeType.dataset.pubType : 'todos';
    const yearFilter = activeYear ? activeYear.dataset.pubYear : 'todos';
    const searchTerm = pubSearch ? pubSearch.value.toLowerCase() : '';

    pubRows.forEach(row => {
      const matchType = typeFilter === 'todos' || row.dataset.type === typeFilter;
      const matchYear = yearFilter === 'todos' || row.dataset.year === yearFilter;
      const matchSearch = !searchTerm || row.textContent.toLowerCase().includes(searchTerm);
      row.style.display = (matchType && matchYear && matchSearch) ? '' : 'none';
    });
  }

  if (pubFilterBtns.length > 0) {
    pubFilterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        pubFilterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        filterPubs();
      });
    });
  }

  if (pubYearBtns.length > 0) {
    pubYearBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        pubYearBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        filterPubs();
      });
    });
  }

  if (pubSearch) {
    pubSearch.addEventListener('input', filterPubs);
  }

  /* ========================================
     MEMBER MODAL
     ======================================== */
  const modalOverlay = document.querySelector('.modal-overlay');
  const modal = document.querySelector('.modal');

  if (modalOverlay && modal) {
    const modalClose = modal.querySelector('.modal__close');
    const modalAvatar = modal.querySelector('.modal__avatar');
    const modalName = modal.querySelector('.modal__name');
    const modalRole = modal.querySelector('.modal__role');
    const modalBio = modal.querySelector('.modal__bio');
    const modalInterests = modal.querySelector('.modal__interests');
    const modalLattes = modal.querySelector('.modal__lattes');

    // Open modal
    document.querySelectorAll('.member-card[data-member]').forEach(card => {
      card.addEventListener('click', () => {
        const data = JSON.parse(card.dataset.member);

        if (modalAvatar) {
          modalAvatar.textContent = data.initials;
          modalAvatar.style.background = data.color;
        }
        if (modalName) modalName.textContent = data.name;
        if (modalRole) modalRole.textContent = data.role;
        if (modalBio) modalBio.textContent = data.bio;

        if (modalInterests) {
          modalInterests.innerHTML = '';
          (data.interests || []).forEach(interest => {
            const tag = document.createElement('span');
            tag.className = 'modal__interest-tag';
            tag.textContent = interest;
            modalInterests.appendChild(tag);
          });
        }

        if (modalLattes) {
          if (data.lattes) {
            modalLattes.href = data.lattes;
            modalLattes.style.display = 'inline-flex';
          } else {
            modalLattes.style.display = 'none';
          }
        }

        modalOverlay.classList.add('active');
        document.body.style.overflow = 'hidden';
      });
    });

    // Close modal
    function closeModal() {
      modalOverlay.classList.remove('active');
      document.body.style.overflow = '';
    }

    if (modalClose) modalClose.addEventListener('click', closeModal);
    modalOverlay.addEventListener('click', (e) => {
      if (e.target === modalOverlay) closeModal();
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modalOverlay.classList.contains('active')) closeModal();
    });
  }

  /* ========================================
     BIBLIOTECA DIGITAL — Sidebar, Search, Scroll Tracking
     ======================================== */

  // Sidebar toggle (mobile)
  const bibSidebarToggle = document.getElementById('bibliotecaSidebarToggle');
  const bibSidebar = document.getElementById('bibliotecaSidebar');
  const bibOverlay = document.getElementById('bibliotecaSidebarOverlay');

  function openBibSidebar() {
    if (bibSidebar) bibSidebar.classList.add('open');
    if (bibOverlay) bibOverlay.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeBibSidebar() {
    if (bibSidebar) bibSidebar.classList.remove('open');
    if (bibOverlay) bibOverlay.classList.remove('active');
    document.body.style.overflow = '';
  }

  if (bibSidebarToggle) {
    bibSidebarToggle.addEventListener('click', () => {
      if (bibSidebar && bibSidebar.classList.contains('open')) {
        closeBibSidebar();
      } else {
        openBibSidebar();
      }
    });
  }

  if (bibOverlay) {
    bibOverlay.addEventListener('click', closeBibSidebar);
  }

  // Close sidebar on link click (mobile)
  const bibSidebarLinks = document.querySelectorAll('.sidebar-section-link');
  bibSidebarLinks.forEach(link => {
    link.addEventListener('click', () => {
      if (window.innerWidth <= 1024) {
        closeBibSidebar();
      }
    });
  });

  // Search filter for resources
  const bibSearchInput = document.getElementById('bibliotecaSearch');
  const bibSearchCount = document.getElementById('bibliotecaSearchCount');
  const bibResourceCards = document.querySelectorAll('.resource-card[data-searchable]');

  if (bibSearchInput && bibResourceCards.length > 0) {
    bibSearchInput.addEventListener('input', () => {
      const term = bibSearchInput.value.toLowerCase().trim();
      let visibleCount = 0;

      bibResourceCards.forEach(card => {
        const searchable = (card.dataset.searchable || '').toLowerCase();
        const textContent = card.textContent.toLowerCase();
        const match = !term || searchable.includes(term) || textContent.includes(term);
        card.classList.toggle('hidden', !match);
        if (match) visibleCount++;
      });

      if (bibSearchCount) {
        if (term) {
          bibSearchCount.textContent = visibleCount + ' recurso' + (visibleCount !== 1 ? 's' : '') + ' encontrado' + (visibleCount !== 1 ? 's' : '');
        } else {
          bibSearchCount.textContent = '';
        }
      }
    });
  }

  // Active section tracking on scroll (IntersectionObserver)
  const bibSections = document.querySelectorAll('.biblioteca-section[id]');
  const bibNavLinks = document.querySelectorAll('.sidebar-section-link[data-section]');

  if (bibSections.length > 0 && bibNavLinks.length > 0) {
    const sectionObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const id = entry.target.id;
          bibNavLinks.forEach(link => {
            link.classList.toggle('active', link.dataset.section === id);
          });
        }
      });
    }, {
      threshold: 0.15,
      rootMargin: '-80px 0px -50% 0px'
    });

    bibSections.forEach(section => sectionObserver.observe(section));
  }

  // Smooth scroll for sidebar links
  bibNavLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const targetId = link.getAttribute('href');
      const target = document.querySelector(targetId);
      if (target) {
        const headerOffset = 80;
        const elementPosition = target.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.scrollY - headerOffset;
        window.scrollTo({ top: offsetPosition, behavior: 'smooth' });
      }
    });
  });

})();
