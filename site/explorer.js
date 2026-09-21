'use strict';
const controls = document.querySelector('.filters');
if (controls) {
  const benchmark = document.querySelector('#benchmark-filter');
  const language = document.querySelector('#language-filter');
  const status = document.querySelector('#filter-status');
  const empty = document.querySelector('#empty-state');
  const sections = [...document.querySelectorAll('.benchmark-section')];
  const update = () => {
    let visible = 0;
    sections.forEach(section => {
      let count = 0;
      section.querySelectorAll('[data-series]').forEach(row => {
        const matches = (benchmark.value === 'all' || benchmark.value === section.id) &&
          (language.value === 'all' || language.value === row.dataset.language);
        row.hidden = !matches;
        if (matches) count += 1;
      });
      section.hidden = count === 0;
      visible += count;
    });
    status.textContent = `${visible} série${visible > 1 ? 's' : ''} affichée${visible > 1 ? 's' : ''}.`;
    empty.hidden = visible !== 0;
  };
  const followAnchor = () => {
    const hash = location.hash.slice(1);
    if (sections.some(section => section.id === hash)) {
      benchmark.value = hash;
      language.value = 'all';
      update();
    }
  };
  controls.hidden = false;
  benchmark.addEventListener('change', update);
  language.addEventListener('change', update);
  document.querySelector('#reset-filters').addEventListener('click', () => {
    benchmark.value = 'all';
    language.value = 'all';
    update();
  });
  document.querySelectorAll('.benchmark-index a').forEach(link => {
    link.addEventListener('click', () => {
      benchmark.value = link.hash.slice(1);
      language.value = 'all';
      update();
    });
  });
  window.addEventListener('hashchange', followAnchor);
  update();
  followAnchor();
}
