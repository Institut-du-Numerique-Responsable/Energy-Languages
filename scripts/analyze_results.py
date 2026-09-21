#!/usr/bin/env python3
"""Reproduce a descriptive analysis of the inherited CSV snapshot (no benchmarks run)."""
import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import math
from pathlib import Path
import re
import statistics as stats

FIELDS = ('package_j', 'cpu_j', 'gpu_j', 'dram_j', 'time_ms')
SHORT_MS = 10
SHIFT_RATIO = 2
MIN_SAMPLES = 5


def parse_row(text, source, line, block):
    fields = [field.strip() for field in re.split('[;,]', text)]
    if len(fields) != 6 or not fields[0]:
        raise ValueError('expected benchmark and five numeric fields')
    values = [float(field) if field else None for field in fields[1:]]
    row = dict(zip(FIELDS, values))
    row.update(source=source, line=line, block=block, language=Path(source).parent.name,
               benchmark=fields[0], variant=Path(source).name.startswith('x'))
    issues = []
    if any(value is not None and not math.isfinite(value) for value in values):
        issues.append('nonfinite')
    if any(value is not None and value < 0 for value in values[:4]):
        issues.append('negative_energy')
    if values[0] is None or values[0] <= 0:
        issues.append('invalid_package')
    if values[-1] is None or values[-1] <= 0:
        issues.append('invalid_time')
    row['numeric_valid'] = not issues
    if values[-1] is not None and 0 < values[-1] < SHORT_MS:
        issues.append('short_time')
    row['issues'] = issues
    row['time_s'] = values[-1] / 1000 if values[-1] is not None else None
    return row


def row_key(row):
    return (row['language'], row['benchmark'], *(row[field] for field in FIELDS))


def load_sources(root):
    rows, inventory, rejected = [], [], []
    for path in sorted(root.glob('*/*.csv')):
        source = path.relative_to(root).as_posix()
        info = dict(source=source, sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                    variant=path.name.startswith('x'), data_rows=0, header_rows=0,
                    blank_rows=0, malformed_rows=0, duplicate_primary_rows=0)
        previous, block = None, 0
        for line, text in enumerate(path.read_text().splitlines(), 1):
            if not text.strip():
                info['blank_rows'] += 1
                continue
            if text.lstrip().lower().startswith('benchmark-name'):
                info['header_rows'] += 1
                continue
            try:
                row = parse_row(text, source, line, block)
            except ValueError as error:
                info['malformed_rows'] += 1
                rejected.append(dict(source=source, line=line, reason=str(error)))
                continue
            if row['benchmark'] != previous:
                block += 1
                previous = row['benchmark']
            row['block'] = block
            rows.append(row)
            info['data_rows'] += 1
        inventory.append(info)
    primary = {row_key(row) for row in rows if not row['variant']}
    for info in inventory:
        if info['variant']:
            info['duplicate_primary_rows'] = sum(row_key(row) in primary for row in rows
                                                  if row['source'] == info['source'])
    return rows, inventory, rejected


def percentile(values, fraction):
    ordered = sorted(values)
    index = (len(ordered) - 1) * fraction
    lower = math.floor(index)
    upper = math.ceil(index)
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (index - lower)


def summarize_series(rows):
    good = [row for row in rows if row['numeric_valid']]
    result = {key: rows[0][key] for key in ('source', 'language', 'benchmark', 'variant')}
    result.update(n_raw=len(rows), n_valid=len(good), n_invalid=len(rows) - len(good),
                  n_short=sum('short_time' in row['issues'] for row in rows),
                  blocks=len({row['block'] for row in rows}),
                  line_first=min(row['line'] for row in rows),
                  line_last=max(row['line'] for row in rows))
    metrics = {
        'package_j': [row['package_j'] for row in good],
        'time_s': [row['time_s'] for row in good],
        'power_w': [row['package_j'] / row['time_s'] for row in good],
        'edp_js': [row['package_j'] * row['time_s'] for row in good],
        'cpu_share': [row['cpu_j'] / row['package_j'] for row in good if row['cpu_j'] is not None],
        'dram_j': [row['dram_j'] for row in good if row['dram_j'] is not None],
    }
    for key, values in metrics.items():
        result[key + '_median'] = stats.median(values) if values else None
        if key in ('package_j', 'time_s'):
            result[key + '_q25'] = percentile(values, .25) if values else None
            result[key + '_q75'] = percentile(values, .75) if values else None
            result[key + '_iqr_pct'] = (100 * (percentile(values, .75) - percentile(values, .25))
                                       / stats.median(values)) if values else None
    by_block = defaultdict(list)
    for row in good:
        by_block[row['block']].append(row['time_s'])
    medians = [stats.median(times) for times in by_block.values()]
    result['block_time_ratio'] = max(medians) / min(medians) if medians else None
    flags = []
    if result['n_invalid']:
        flags.append('invalid_rows_removed')
    if result['n_short']:
        flags.append('short_time')
    if len(good) < MIN_SAMPLES:
        flags.append('insufficient_samples')
    if result['block_time_ratio'] is not None and result['block_time_ratio'] > SHIFT_RATIO:
        flags.append('block_shift')
    result['flags'] = flags
    result['exploratory_eligible'] = not any(flag in flags for flag in
                                            ('short_time', 'insufficient_samples', 'block_shift'))
    return result


def ranks(values):
    output = [0.] * len(values)
    ordered = sorted(range(len(values)), key=values.__getitem__)
    start = 0
    while start < len(values):
        stop = start + 1
        while stop < len(values) and values[ordered[stop]] == values[ordered[start]]:
            stop += 1
        for index in ordered[start:stop]:
            output[index] = (start + stop + 1) / 2
        start = stop
    return output


def spearman(x, y):
    if len(x) < 2:
        return None
    rx, ry = ranks(x), ranks(y)
    mx, my = stats.mean(rx), stats.mean(ry)
    numerator = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    denominator = math.sqrt(sum((a - mx)**2 for a in rx) * sum((b - my)**2 for b in ry))
    return numerator / denominator if denominator else None


def correlations(series):
    by_benchmark = defaultdict(list)
    for item in series:
        if item['exploratory_eligible']:
            by_benchmark[item['benchmark']].append(item)
    result = []
    for benchmark, group in sorted(by_benchmark.items()):
        result.append(dict(benchmark=benchmark, n_series=len(group),
                           spearman_energy_time=spearman([s['package_j_median'] for s in group],
                                                         [s['time_s_median'] for s in group]),
                           spearman_energy_power=spearman([s['package_j_median'] for s in group],
                                                          [s['power_w_median'] for s in group])))
    return result


def write_csv(path, rows):
    if not rows:
        path.write_text('')
        return
    with path.open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        for row in rows:
            writer.writerow({key: '|'.join(value) if isinstance(value, list) else value
                             for key, value in row.items()})


def fmt(value, digits=3):
    return '—' if value is None else f'{value:,.{digits}f}'.replace(',', ' ')


def make_tables(series, output):
    lines = ['# Tables détaillées des observations historiques', '',
             'Générées par `scripts/analyze_results.py`. Voir la [méthode et les limites](../BENCHMARK_RESULTS.md).', '',
             'Les valeurs sont des médianes après retrait des lignes numériquement invalides. '
             'Les séries signalées restent visibles ici, même lorsqu’elles sont exclues des croisements exploratoires. '
             'Un même langage peut regrouper plusieurs blocs de mesures non datés. Aucun classement global n’est calculé.', '']
    for benchmark in sorted({item['benchmark'] for item in series}):
        lines += [f'## {benchmark}', '',
                  '| Configuration | n valides/brut | PKG (J) | Temps (s) | Puissance PKG (W) | IQR énergie (%) | Signalements |',
                  '|---|---:|---:|---:|---:|---:|---|']
        for item in sorted((s for s in series if s['benchmark'] == benchmark), key=lambda s: s['language']):
            source = '../../' + item['source']
            lines.append(f"| [{item['language']}]({source}#L{item['line_first']}) | {item['n_valid']}/{item['n_raw']} | "
                         f"{fmt(item['package_j_median'])} | {fmt(item['time_s_median'])} | {fmt(item['power_w_median'])} | "
                         f"{fmt(item['package_j_iqr_pct'], 1)} | {', '.join(item['flags']) or 'aucun filtre déclenché'} |")
        lines.append('')
    (output / 'TABLES.md').write_text('\n'.join(lines))


def make_report(rows, inventory, rejected, series, correlation, output):
    primary = [row for row in rows if not row['variant']]
    valid = [row for row in primary if row['numeric_valid']]
    negative = sum('negative_energy' in row['issues'] for row in primary)
    short = sum('short_time' in row['issues'] for row in primary)
    excluded = [item for item in series if not item['exploratory_eligible']]
    nbody = sorted((item for item in series if item['benchmark'] == 'n-body'), key=lambda s: s['language'])
    eligible_nbody = {item['language']: item for item in nbody if item['exploratory_eligible']}
    lines = [
        '# Résultats historiques et analyses croisées', '',
        '**Ces résultats proviennent des CSV hérités du projet Energy-Languages. '
        'Ils ne constituent ni une nouvelle campagne INR, ni une reproduction validée du classement de l’article de 2017.**', '',
        'Cette page est générée à partir des fichiers locaux. Le matériel, les versions des compilateurs, '
        'les paramètres et les codes de sortie de chaque observation ne sont pas enregistrés dans les CSV. '
        'Les Makefiles actuels ne permettent pas de les reconstituer avec certitude. '
        'Les corrections INR du programme de mesure ne valident pas rétroactivement ces données.', '',
        '## Ce que contient le dépôt', '',
        f'- **{len(inventory)} fichiers CSV**, soit **{len(rows)} observations lisibles**.',
        f'- **{sum(not item["variant"] for item in inventory)} fichiers principaux**, **{len(primary)} observations** et '
        f'**{len(series)} séries configuration × benchmark**.',
        f'- **{len({item["benchmark"] for item in series})} benchmarks représentés** ; leur couverture varie selon la configuration.',
        f'- **{sum(item["variant"] for item in inventory)} variantes `x*.csv`**, conservées séparément : '
        f'{sum(row["variant"] for row in rows)} lignes, dont {sum(item["duplicate_primary_rows"] for item in inventory)} '
        'ont exactement les mêmes valeurs qu’une ligne du fichier principal du même langage.',
        '- Le dossier Java ne contient pas de CSV ; `Java-GraalVM/GraalVM.csv` est une configuration distincte.', '',
        '![Couverture des données principales](results/coverage.png)', '',
        'Les nombres dans la matrice comptent les lignes brutes, y compris les valeurs signalées. '
        'Une cellule vide signifie absence de données, et non consommation nulle.', '',
        '## Qualité des données et règles de traitement', '',
        f'- **{negative} lignes principales contiennent au moins une énergie négative**. '
        'Cela peut notamment être compatible avec un débordement de compteur, mais la cause ne peut pas être établie ici. '
        'Elles ne sont ni ramenées à zéro ni corrigées par une constante supposée.',
        f'- **{len(primary) - len(valid)} lignes principales numériquement invalides** sont retirées des statistiques '
        '(énergie négative, valeur non finie, PKG absent/non positif ou temps absent/non positif).',
        f'- **{short} lignes principales durent moins de {SHORT_MS} ms**. '
        'Ce seuil de dépistage ne prouve pas un échec ; il signale des observations à vérifier avec les sorties du programme.',
        f'- **{len(excluded)} séries** sont écartées des corrélations et du nuage exploratoire : '
        f'au moins une durée < {SHORT_MS} ms, moins de {MIN_SAMPLES} lignes valides, '
        f'ou rapport > {SHIFT_RATIO} entre les médianes temporelles de blocs contigus du même benchmark.',
        '- Un « bloc » désigne uniquement une séquence contiguë de lignes portant le même nom de benchmark. '
        'Ce n’est pas un identifiant de session expérimental. Des changements internes à un bloc peuvent donc rester indétectables.',
        '- Les variantes `x*.csv` ne sont pas ajoutées aux fichiers principaux : leur statut expérimental est inconnu. '
        'Le choix du fichier non préfixé est une convention de cette analyse, pas une preuve de meilleure qualité.',
        f'- {sum(item["header_rows"] for item in inventory)} en-tête reconnu et '
        f'{sum(item["blank_rows"] for item in inventory)} lignes vides ignorés ; {len(rejected)} lignes malformées. '
        'L’en-tête GraalVM annonce cinq champs mais les lignes en comportent six : les positions effectives '
        '`benchmark, PKG, CPU, GPU, DRAM, temps` sont utilisées, conformément au code du programme de mesure.', '',
        'Les séries écartées restent dans les [tables détaillées](results/TABLES.md) et les exports. '
        '« Aucun filtre déclenché » ne signifie pas « mesure validée ». Les filtres peuvent introduire un biais de sélection ; '
        'ils servent à une exploration prudente, pas à reconstruire des données scientifiques manquantes.', '',
        '### Séries écartées des croisements', '',
        '| Configuration | Benchmark | Durées < 10 ms (lignes) | Rapport des médianes de blocs | Signalements |',
        '|---|---|---:|---:|---|',
    ]
    for item in excluded:
        lines.append(f"| {item['language']} | {item['benchmark']} | {item['n_short']} | {fmt(item['block_time_ratio'], 1)} | {', '.join(item['flags'])} |")
    lines += ['', '## Exemple lisible : n-body', '',
              'Valeurs descriptives par configuration, triées alphabétiquement. Les séries exclues restent affichées '
              'pour rendre les anomalies visibles. Les comparaisons supposeraient des charges et conditions identiques, '
              'ce que ces CSV ne prouvent pas.', '',
              '| Configuration | n valides/brut | Énergie PKG médiane (J) | Temps médian (s) | Puissance médiane (W) | Croisements exploratoires |',
              '|---|---:|---:|---:|---:|---|']
    for item in nbody:
        lines.append(f"| {item['language']} | {item['n_valid']}/{item['n_raw']} | {fmt(item['package_j_median'])} | "
                     f"{fmt(item['time_s_median'])} | {fmt(item['power_w_median'])} | {'retenue' if item['exploratory_eligible'] else 'écartée'} |")
    lines += ['', '![Énergie et durée observées pour n-body](results/nbody_energy_time.png)', '',
              'Axes logarithmiques ; chaque point représente une série retenue par les filtres. '
              'Les barres montrent les quartiles 25–75 %, pas des intervalles de confiance. '
              'Les traits obliques sont des puissances constantes `E = P × t`.', '',
              '## Analyses croisées calculées', '',
              '### 1. Énergie × temps, à benchmark fixé', '',
              'Corrélation de Spearman entre médianes de séries retenues, calculée séparément par benchmark. '
              'Les répétitions ne sont pas traitées comme des langages indépendants. Les ex æquo reçoivent le rang moyen. '
              'Une forte corrélation décrit une association ; elle n’établit pas que le langage en est la cause.', '',
              '| Benchmark | Séries retenues | ρ énergie–temps | ρ énergie–puissance |',
              '|---|---:|---:|---:|']
    for item in correlation:
        lines.append(f"| {item['benchmark']} | {item['n_series']} | {fmt(item['spearman_energy_time'])} | {fmt(item['spearman_energy_power'])} |")
    lines += ['', 'Aucune corrélation globale ne mélange les charges de travail. '
              'Les corrélations énergie–puissance ne sont pas indépendantes : la puissance est calculée à partir de l’énergie.', '',
              '### 2. Énergie × puissance : distinguer consommation et durée', '',
              '`Pᵢ = E_PKG,ᵢ / (temps_ms,ᵢ / 1000)` en watts ; le tableau donne la médiane des rapports ligne par ligne. '
              'Ce n’est pas le rapport de deux médianes, ni une mesure de la puissance totale à la prise.', '']
    if 'C' in eligible_nbody and 'Python' in eligible_nbody:
        c, py = eligible_nbody['C'], eligible_nbody['Python']
        lines += [f"Sur les séries n-body disponibles, Python/C vaut **{fmt(py['package_j_median']/c['package_j_median'], 1)}×** "
                  f"pour l’énergie médiane, **{fmt(py['time_s_median']/c['time_s_median'], 1)}×** pour le temps médian "
                  f"et **{fmt(py['power_w_median']/c['power_w_median'], 2)}×** pour la puissance médiane. "
                  'Ces rapports illustrent le rôle de la durée dans cet échantillon ; ils ne sont pas des facteurs universels applicables aux langages.', '']
    lines += ['### 3. Énergie × régularité des mesures', '',
              'Les exports donnent la médiane, les quartiles et `IQR / médiane × 100` pour l’énergie et le temps. '
              'Une forte dispersion ou un déplacement entre blocs motive une inspection des exécutions et du protocole, '
              'plutôt qu’une moyenne unique. Les quartiles utilisent une interpolation linéaire au rang `(n−1) × p`.', '',
              '### 4. PKG × CPU × DRAM', '',
              'L’export contient la médiane de `CPU/PKG` et l’énergie DRAM médiane lorsque le domaine est renseigné. '
              'Le domaine CPU est une composante du package : **ne pas additionner PKG et CPU**. '
              'Les domaines disponibles dépendent du matériel ; une valeur manquante reste manquante. '
              '**DRAM (J) mesure une énergie, pas la quantité de mémoire utilisée.**', '',
              '### 5. Énergie × latence : produit énergie–délai', '',
              'L’export donne la médiane des produits par exécution `EDPᵢ = E_PKG,ᵢ × temps_s,ᵢ`, en J·s. '
              'Cet indicateur peut servir à explorer un compromis sur une même charge. Il impose implicitement un choix '
              'de pondération et ne constitue pas un score environnemental général. Aucun classement inter-benchmarks n’en est dérivé.', '',
              '## Analyses à mener lors d’une campagne contrôlée', '',
              '| Croisement | Question | Données ou contrôles supplémentaires |',
              '|---|---|---|',
              '| Langage × benchmark | Les écarts changent-ils selon la charge ? | Même entrée, sorties vérifiées, versions et options figées ; ratios à une référence par benchmark, puis moyenne géométrique sur une couverture commune seulement. |',
              '| Temps × énergie : front de Pareto | Quels choix évitent un compromis défavorable ? | Même machine et mêmes entrées ; incertitude par répétition et seuil de latence métier. Ne pas déclarer un gagnant sur des différences inférieures à la variabilité. |',
              '| Mémoire maximale × énergie × durée | Une baisse de mémoire réduit-elle l’énergie ? | Ajouter le pic RSS en octets. Il est absent des CSV actuels ; DRAM J ne le remplace pas. |',
              '| Taille d’entrée × langage | Comment les coûts évoluent-ils avec la charge ? | Plusieurs tailles explicitement enregistrées, checksum des entrées et validation des sorties. |',
              '| Parallélisme × puissance × durée | Le gain de temps compense-t-il la hausse de puissance ? | Nombre de threads, affinité CPU, sockets, fréquence et charge de fond contrôlés. |',
              '| Runtime × échauffement | Quelle différence entre démarrage et régime établi ? | Séparer exécutions à froid et à chaud ; versions JVM/JIT, compilateurs et GC ; ordre randomisé. |',
              '| Énergie machine × carbone | Quel impact pour une charge et un lieu donnés ? | Mesure du système complet, périmètre, durée, facteur électrique daté/localisé et émissions incorporées si pertinentes ; aucune conversion fiable depuis les seuls PKG J. |', '',
              'Les fichiers actuels ne permettent pas de répondre honnêtement aux croisements mémoire ou carbone, '
              'ni de distinguer les effets du langage, de l’algorithme, de la version et du matériel.', '',
              '## Reproduire et réutiliser', '',
              'Depuis la racine du dépôt :', '', '```sh',
              'python3 scripts/analyze_results.py',
              '# Optionnel : régénérer aussi les graphiques (Matplotlib requis).',
              'python3 scripts/analyze_results.py --plots',
              'python3 -m unittest discover -s tests -v', '```', '',
              'Les calculs et tableaux utilisent uniquement la bibliothèque standard Python. '
              'Les graphiques utilisent Matplotlib ; ils sont publiés ici pour être consultables sans installation.', '',
              '- [Toutes les séries par benchmark](results/TABLES.md)',
              '- [Observations normalisées, provenance et signalements](results/observations.csv)',
              '- [Statistiques des séries principales](results/series.csv)',
              '- [Statistiques par bloc contigu](results/blocks.csv)',
              '- [Corrélations descriptives](results/correlations.csv)',
              '- [Inventaire des sources et empreintes SHA-256](results/sources.csv)',
              '- [Lignes malformées](results/rejected.csv)',
              '- [Limites générales du projet](KNOWN_LIMITATIONS.md)', '',
              'Sources : CSV conservés dans chaque dossier de langage, [programme de mesure](../RAPL/rapl.c), '
              '[projet original Green Software Lab](https://github.com/greensoftwarelab/Energy-Languages). '
              'Les auteurs originaux et la licence sont indiqués dans le [README](../README.md).', '']
    # Put a compact, readable subset of the derived metrics next to the method;
    # the full precision data for every series remains in series.csv.
    position = lines.index('## Analyses à mener lors d’une campagne contrôlée')
    derived = ['### Exemples de métriques dérivées pour n-body', '',
               'Configurations choisies pour illustrer la lecture des indicateurs, sans classement. '
               'Chaque colonne est une médiane calculée ligne par ligne sur les observations valides.', '',
               '| Configuration | CPU/PKG (%) | DRAM (J) | EDP (J·s) | IQR énergie / médiane (%) |',
               '|---|---:|---:|---:|---:|']
    for language in ['C', 'Rust', 'Java-GraalVM', 'JavaScript', 'Python']:
        item = eligible_nbody.get(language)
        if item:
            share = item['cpu_share_median']
            derived.append(f"| {language} | {fmt(100 * share if share is not None else None, 1)} | "
                           f"{fmt(item['dram_j_median'])} | {fmt(item['edp_js_median'])} | {fmt(item['package_j_iqr_pct'], 1)} |")
    derived += ['', 'Un tiret indique un domaine non renseigné, pas une énergie nulle. '
                'L’IQR décrit la dispersion du fichier agrégé ; il ne sépare pas automatiquement les sessions.', '']
    lines[position:position] = derived
    (output.parent / 'BENCHMARK_RESULTS.md').write_text('\n'.join(lines))


def make_plots(rows, series, output):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    languages = sorted({item['language'] for item in series})
    benchmarks = sorted({item['benchmark'] for item in series})
    counts = Counter((row['language'], row['benchmark']) for row in rows if not row['variant'])
    matrix = [[counts[(language, benchmark)] for benchmark in benchmarks] for language in languages]
    plt.rcParams.update({'font.size': 10})
    fig, ax = plt.subplots(figsize=(12, 11), layout='constrained')
    ax.imshow(matrix, cmap=ListedColormap(['#f3f4f6', '#dceaf4', '#a9cce3', '#609ec4', '#23658c']), vmin=0, vmax=40)
    ax.set_xticks(range(len(benchmarks)), benchmarks, rotation=40, ha='right')
    ax.set_yticks(range(len(languages)), languages)
    for y, language in enumerate(languages):
        for x, benchmark in enumerate(benchmarks):
            count = counts[(language, benchmark)]
            if count:
                ax.text(x, y, str(count), ha='center', va='center', color='white' if count >= 30 else '#172a38')
    ax.set_title('Couverture des CSV principaux — nombre de lignes brutes\nValeurs signalées incluses ; absence de donnée ≠ zéro énergie', pad=18)
    fig.savefig(output / 'coverage.png', dpi=150)
    plt.close(fig)
    chosen = [item for item in series if item['benchmark'] == 'n-body' and item['exploratory_eligible']]
    fig, ax = plt.subplots(figsize=(11, 7), layout='constrained')
    labels = {'C', 'C++', 'Fortran', 'Rust', 'Java-GraalVM', 'JavaScript', 'Python', 'Lua', 'Racket', 'Ruby'}
    offsets = {'C': (8, -20), 'C++': (-44, 12), 'Fortran': (-60, -18), 'Rust': (-38, -30),
               'Java-GraalVM': (8, 16), 'JavaScript': (8, 6), 'Python': (-48, 10),
               'Lua': (8, 6), 'Racket': (8, 8), 'Ruby': (8, -18)}
    for item in chosen:
        x, y = item['time_s_median'], item['package_j_median']
        ax.errorbar(x, y, xerr=[[x-item['time_s_q25']], [item['time_s_q75']-x]],
                    yerr=[[y-item['package_j_q25']], [item['package_j_q75']-y]],
                    fmt='o', color='#176b87', ecolor='#829aa7', alpha=.85, markersize=5, capsize=2)
        if item['language'] in labels:
            ax.annotate(item['language'], (x, y), xytext=offsets[item['language']],
                        textcoords='offset points', fontsize=9,
                        arrowprops=dict(arrowstyle='-', color='#829aa7', lw=.6))
    if chosen:
        minimum = min(item['time_s_median'] for item in chosen) * .65
        maximum = max(item['time_s_median'] for item in chosen) * 1.35
        for power in [10, 20, 40]:
            ax.plot([minimum, maximum], [minimum*power, maximum*power], '--', lw=.8, alpha=.5, label=f'{power} W')
    ax.set(xscale='log', yscale='log', xlabel='Temps médian (s) — échelle logarithmique',
           ylabel='Énergie PKG médiane (J) — échelle logarithmique')
    ax.set_title('n-body : énergie × temps, données historiques exploratoires\nQuartiles 25–75 % ; conditions expérimentales non vérifiées', pad=15)
    ax.grid(alpha=.15, which='both')
    ax.legend(title='Puissance constante', loc='upper left')
    fig.savefig(output / 'nbody_energy_time.png', dpi=160)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--plots', action='store_true')
    args = parser.parse_args()
    rows, inventory, rejected = load_sources(args.root)
    if not rows:
        parser.error('No readable source observations found')
    grouped, blocks = defaultdict(list), defaultdict(list)
    for row in rows:
        if not row['variant']:
            grouped[(row['source'], row['benchmark'])].append(row)
            blocks[(row['source'], row['benchmark'], row['block'])].append(row)
    series = [summarize_series(group) for _, group in sorted(grouped.items())]
    block_summaries = [dict(block=key[2], **summarize_series(group)) for key, group in sorted(blocks.items())]
    correlation = correlations(series)
    output = args.root / 'docs/results'
    output.mkdir(parents=True, exist_ok=True)
    write_csv(output / 'observations.csv', rows)
    write_csv(output / 'sources.csv', inventory)
    write_csv(output / 'series.csv', series)
    write_csv(output / 'blocks.csv', block_summaries)
    write_csv(output / 'correlations.csv', correlation)
    # Keep a header even when there are no malformed lines.
    if rejected:
        write_csv(output / 'rejected.csv', rejected)
    else:
        (output / 'rejected.csv').write_text('source,line,reason\n')
    make_tables(series, output)
    make_report(rows, inventory, rejected, series, correlation, output)
    if args.plots:
        make_plots(rows, series, output)
    print(f'{len(rows)} observations; {len(series)} primary series; outputs: {output}')


if __name__ == '__main__':
    main()
