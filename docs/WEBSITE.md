# Site public et référencement

Site : https://institut-du-numerique-responsable.github.io/Energy-Languages/

## Maintenance

```sh
python3 scripts/analyze_results.py
python3 scripts/build_site.py
python3 -m unittest discover -s tests -v
python3 -m http.server 8765 --directory _site
```

Les modèles sont dans `site/`. Le générateur utilise les CSV de `docs/results/` pour les chiffres, tableaux et conclusions. Le README partage ces conclusions via un bloc généré par l'analyse. Ne pas modifier ce bloc manuellement. Aucun framework, police externe, traceur ou service tiers n'est nécessaire à la consultation.

Le workflow `.github/workflows/runner-tests.yml` teste le projet et la reproductibilité des exports avant de publier `_site` sur GitHub Pages depuis `main`. Pages doit utiliser la source **GitHub Actions** dans les paramètres du dépôt. En cas de changement de domaine, modifier `BASE` dans `scripts/build_site.py`, les liens documentaires et les tests des URL canoniques.

## Découverte et indexation

Chaque page possède un titre, une description, une URL canonique et des métadonnées de partage. Les données structurées décrivent le logiciel, le jeu de données, ses auteurs et ses téléchargements. Les 253 séries sont lisibles dans le HTML sans exécuter JavaScript. Les conclusions renvoient aux sources et exposent leur périmètre historique.

Sitemap : https://institut-du-numerique-responsable.github.io/Energy-Languages/sitemap.xml

Pour demander l'indexation Google, valider la propriété du site dans Search Console, puis y soumettre ce sitemap. La publication ne garantit ni l'indexation, ni un classement, ni une citation par une IA. Les bonnes pratiques SEO habituelles restent pertinentes pour les fonctionnalités de recherche avec IA ; aucun fichier spécial ne garantit leur inclusion.

Un fichier `robots.txt` doit se trouver à la racine du domaine : un fichier placé dans `/Energy-Languages/` ne contrôle pas les robots. Toute modification des règles de la racine doit être coordonnée avec les responsables du site de l'organisation. OAI-SearchBot concerne la recherche OpenAI et se distingue de GPTBot.

Références : [Google et recherche IA](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide), [jeux de données](https://developers.google.com/search/docs/appearance/structured-data/dataset), [robots.txt](https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec), [robots OpenAI](https://developers.openai.com/api/docs/bots), [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

## Signalement IndexNow

`site/indexnow-key.txt` contient le jeton public de vérification du site, sans droit d'accès au dépôt. Le générateur publie le fichier de vérification correspondant à la racine du projet Pages. Les trois URL canoniques peuvent être signalées à `https://api.indexnow.org/indexnow` avec les champs `host`, `key`, `keyLocation` et `urlList`. La portée reste limitée à `/Energy-Languages/`. Un code 200 indique la réception ; 202 indique que la vérification de la clé est en attente. Aucun des deux ne prouve l'indexation. Ce signalement ne remplace pas Search Console. Voir la [documentation IndexNow](https://www.indexnow.org/documentation).

## Maintenance GitHub

Les modifications passent par une pull request vers `main`, avec le contrôle `runner` réussi sur une branche à jour et les conversations résolues. La protection s'applique aussi aux administrateurs ; force-push et suppression de `main` sont désactivés. Aucune approbation humaine supplémentaire n'est imposée pour permettre la maintenance avec un seul mainteneur ; une relecture reste recommandée. Les badges du README indiquent la CI, la licence, le site et le périmètre historique des données, sans prétendre à une certification scientifique.
