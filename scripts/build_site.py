#!/usr/bin/env python3
"""Build a dependency-free static project site from the published analysis exports."""
import argparse
import csv
from html import escape
import json
from pathlib import Path
import shutil
from string import Template

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://institut-du-numerique-responsable.github.io/Energy-Languages/'
REPO = 'https://github.com/Institut-du-Numerique-Responsable/Energy-Languages'
UPSTREAM = 'https://github.com/greensoftwarelab/Energy-Languages'
FLAG_NAMES = {'invalid_rows_removed': 'Lignes invalides retirées',
              'short_time': 'Durée < 10 ms', 'insufficient_samples': 'Moins de 5 lignes valides',
              'block_shift': 'Écart entre blocs > 2×'}


def read_csv(name):
    with (ROOT / 'docs/results' / name).open(newline='') as stream:
        return list(csv.DictReader(stream))


def number(value, digits=3):
    if value is None or value == '':
        return '—'
    return f'{float(value):,.{digits}f}'.replace(',', '\u202f').replace('.', ',')


def schema(page, description, base):
    organization = {'@type': 'Organization', '@id': base+'#inr',
                    'name': 'Institut du Numérique Responsable', 'url': 'https://institutnr.org'}
    nodes = [organization, {'@type': 'WebSite', '@id': base+'#site', 'name': 'Energy Languages — édition INR',
                            'url': base, 'inLanguage': 'fr', 'publisher': {'@id': base+'#inr'}},
             {'@type': 'WebPage', '@id': base+page, 'url': base+page, 'inLanguage': 'fr',
              'description': description, 'isPartOf': {'@id': base+'#site'}}]
    if page == '':
        nodes.append({'@type': 'SoftwareSourceCode', 'name': 'Energy Languages — édition INR',
                      'description': description, 'codeRepository': REPO, 'url': base,
                      'license': REPO+'/blob/main/LICENSE', 'isBasedOn': UPSTREAM,
                      'maintainer': {'@id': base+'#inr'},
                      'creator': {'@type': 'Organization', 'name': 'Green Software Lab', 'url': UPSTREAM}})
    if page == 'resultats.html':
        nodes.append({'@type': 'Dataset', '@id': base+'resultats.html#dataset',
                      'name': 'Energy Languages — observations historiques et analyse INR',
                      'description': 'Observations historiques de consommation énergétique PKG, CPU et DRAM, '
                      'durée et analyses descriptives. Données héritées à métadonnées expérimentales incomplètes, '
                      'variantes séparées et anomalies signalées. Aucune nouvelle campagne INR.',
                      'url': base+page, 'isBasedOn': UPSTREAM, 'isAccessibleForFree': True,
                      'license': REPO+'/blob/main/LICENSE', 'inLanguage': 'fr',
                      'creator': {'@type': 'Organization', 'name': 'Green Software Lab', 'url': UPSTREAM},
                      'publisher': {'@id': base+'#inr'},
                      'variableMeasured': ['Énergie PKG (J)', 'Énergie CPU (J)', 'Énergie DRAM (J)', 'Temps (ms)'],
                      'distribution': [{'@type': 'DataDownload', 'encodingFormat': 'text/csv',
                                        'contentUrl': base+'data/'+name, 'name': name}
                                       for name in ['observations.csv', 'series.csv', 'blocks.csv', 'sources.csv']]})
    return json.dumps({'@context': 'https://schema.org', '@graph': nodes}, ensure_ascii=False).replace('<', '\\u003c')


def build(output, base=BASE):
    series = read_csv('series.csv')
    sources = read_csv('sources.csv')
    correlation = read_csv('correlations.csv')
    raw = read_csv('observations.csv')
    primary = [row for row in raw if row['variant'] == 'False']
    nbody = {row['language']: row for row in series if row['benchmark'] == 'n-body'}
    c, python = nbody['C'], nbody['Python']
    if any(row['exploratory_eligible'] != 'True' for row in (c, python)):
        raise ValueError('The highlighted n-body comparison requires eligible C and Python series')
    coefficients = [float(row['spearman_energy_time']) for row in correlation if row['spearman_energy_time']]
    benchmarks = sorted({row['benchmark'] for row in series})
    languages = sorted({row['language'] for row in series})
    values = dict(base=base, repo=REPO, energy_ratio=number(float(python['package_j_median'])/float(c['package_j_median']), 1),
                  duration_ratio=number(float(python['time_s_median'])/float(c['time_s_median']), 1),
                  power_ratio=number(float(python['power_w_median'])/float(c['power_w_median']), 2),
                  rho_min=number(min(coefficients)), rho_max=number(max(coefficients)),
                  series_count=len(series), raw_rows=number(len(raw), 0), primary_rows=number(len(primary), 0),
                  config_count=len(languages), benchmark_count=len(benchmarks), source_count=len(sources),
                  invalid_rows=sum(row['numeric_valid'] == 'False' for row in primary),
                  excluded_series=sum(row['exploratory_eligible'] == 'False' for row in series),
                  duplicate_rows=sum(int(row['duplicate_primary_rows']) for row in sources))
    tables = []
    for benchmark in benchmarks:
        body = []
        for row in series:
            if row['benchmark'] != benchmark:
                continue
            flags = [FLAG_NAMES[flag] for flag in row['flags'].split('|') if flag]
            status = '; '.join(flags) if flags else 'Aucun filtre déclenché'
            if row['exploratory_eligible'] == 'False':
                status += ' ; écartée des croisements'
            body.append(f'<tr data-series="{escape(benchmark+":"+row["language"], quote=True)}" '
                        f'data-language="{escape(row["language"], quote=True)}" class="{"flagged" if flags else ""}">'
                        f'<th scope="row"><a href="{REPO}/blob/main/{escape(row["source"], quote=True)}#L{row["line_first"]}">{escape(row["language"])}</a></th>'
                        f'<td>{row["n_valid"]}/{row["n_raw"]}</td><td>{number(row["package_j_median"])}</td>'
                        f'<td>{number(row["time_s_median"])}</td><td>{number(row["power_w_median"])}</td>'
                        f'<td>{number(row["package_j_iqr_pct"], 1)}</td><td class="status-cell">{escape(status)}</td></tr>')
        tables.append(f'<section class="benchmark-section" id="{escape(benchmark)}"><h3>{escape(benchmark)}</h3>'
                      f'<div class="table-scroll" role="region" aria-label="Résultats {escape(benchmark)}" tabindex="0"><table>'
                      '<thead><tr><th scope="col">Configuration</th><th scope="col">n valides/brut</th>'
                      '<th scope="col">PKG (J)</th><th scope="col">Temps (s)</th><th scope="col">Puissance (W)</th>'
                      '<th scope="col">IQR énergie (%)</th><th scope="col">Signalements</th></tr></thead>'
                      '<tbody>'+''.join(body)+'</tbody></table></div></section>')
    values['tables'] = ''.join(tables)
    values['benchmark_options'] = ''.join(f'<option value="{escape(b)}">{escape(b)}</option>' for b in benchmarks)
    values['language_options'] = ''.join(f'<option value="{escape(language)}">{escape(language)}</option>' for language in languages)
    values['benchmark_links'] = ''.join(f'<a href="#{escape(b)}">{escape(b)}</a>' for b in benchmarks)
    values['correlation_table'] = ('<div class="table-scroll" role="region" aria-label="Corrélations par benchmark" tabindex="0"><table>'
                                  '<thead><tr><th scope="col">Benchmark</th><th scope="col">Séries retenues</th>'
                                  '<th scope="col">ρ énergie–temps</th><th scope="col">ρ énergie–puissance</th></tr></thead><tbody>' +
                                  ''.join(f'<tr><th scope="row">{escape(row["benchmark"])}</th><td>{row["n_series"]}</td>'
                                          f'<td>{number(row["spearman_energy_time"])}</td><td>{number(row["spearman_energy_power"])}</td></tr>'
                                          for row in correlation) + '</tbody></table></div>')
    output.mkdir(parents=True, exist_ok=True)
    (output/'assets').mkdir(exist_ok=True)
    (output/'data').mkdir(exist_ok=True)
    for name in ['style.css', 'explorer.js', 'favicon.svg']:
        shutil.copyfile(ROOT/'site'/name, output/'assets'/name)
    for name in ['nbody_energy_time.png', 'coverage.png']:
        shutil.copyfile(ROOT/'docs/results'/name, output/'assets'/name)
    for path in (ROOT/'docs/results').glob('*.csv'):
        shutil.copyfile(path, output/'data'/path.name)
    pages = [('', 'index.html', 'Consommation énergétique des langages : résultats et méthode | INR',
              'Explorez les benchmarks Energy Languages : énergie, temps, puissance et analyses croisées. Édition INR, données historiques ouvertes et limites documentées.'),
             ('resultats.html', 'resultats.html', 'Résultats des benchmarks énergie et langages de programmation | INR',
              'Consultez les résultats historiques par benchmark : énergie PKG, durée, puissance et dispersion. Tableaux complets, sources et exports CSV ouverts.'),
             ('methode.html', 'methode.html', 'Méthode, sources et limites des benchmarks Energy Languages | INR',
              'Comprendre les mesures RAPL, les filtres, les calculs énergie–temps et la provenance des données Energy Languages. Scripts reproductibles et sources ouvertes.')]
    layout = Template((ROOT/'site/layout.html').read_text())
    for canonical_path, name, title, description in pages:
        body = Template((ROOT/'site'/name).read_text()).substitute(values)
        page = layout.substitute(values, title=title, description=description,
                                 canonical=base+canonical_path, body=body,
                                 schema=schema(canonical_path, description, base),
                                 home_current='aria-current="page"' if name == 'index.html' else '',
                                 results_current='aria-current="page"' if name == 'resultats.html' else '',
                                 method_current='aria-current="page"' if name == 'methode.html' else '')
        (output/name).write_text(page)
    (output/'.nojekyll').write_text('')
    (output/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n'
                                    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
                                    ''.join(f'<url><loc>{escape(base+path)}</loc></url>\n' for path, *_ in pages) + '</urlset>\n')
    print(f'Built {len(pages)} pages and {len(series)} static result rows in {output}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'_site')
    args = parser.parse_args()
    build(args.output)
