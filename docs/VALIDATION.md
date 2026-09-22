# Validation avant une campagne

L'outil `scripts/verify_output.py` exécute une commande de confiance et compare sa sortie standard à un fichier de référence UTF-8. Les espaces et retours à la ligne séparent les tokens ; les nombres sont comparés avec les tolérances absolue et relative explicitement choisies, les autres tokens à l'identique. Ce mode ne convient pas à des sorties binaires ni à des formats dans lesquels les espaces sont significatifs. Le délai par défaut est de 60 secondes ; les sorties supérieures à 1 Mio sont refusées après exécution. La capture utilise un fichier temporaire sur disque.

Le rapport JSON indique la commande, le répertoire, la plateforme, les tolérances, le statut et les empreintes SHA-256 de la référence et de la sortie. Il ne constitue pas un manifeste expérimental complet : enregistrer aussi le commit, les entrées, les options de compilation, les versions des outils et les caractéristiques matérielles. Les commandes et chemins apparaissent dans le rapport : les relire avant publication.

Une référence produite par le programme testé n'est qu'un test de non-régression. Pour valider l'exactitude, utiliser une sortie publiée dont la provenance est vérifiée, un cas calculé indépendamment ou une implémentation de référence revue. Vérifier chaque configuration et chaque taille d'entrée avant de mesurer ; conserver le rapport avec la campagne. Le contrôle n'est pas encore intégré aux anciennes recettes `measure`.

## Compteurs et périmètre

La soustraction est effectuée modulo 2^32 avant la conversion en joules. Elle corrige un retour à zéro seulement si l'énergie consommée entre deux lectures est strictement inférieure à la plage complète du compteur. Elle ne rend pas les longues exécutions sûres : plusieurs tours sont indétectables sans lectures intermédiaires. Une acquisition périodique reste à développer et à valider matériellement.

Le backend conserve sa sélection historique du CPU logique 0. Il mesure le package correspondant, y compris les autres activités sur ce package ; il ne mesure pas l'énergie du processus seul, ne contraint pas son placement et n'additionne pas les packages. Les domaines disponibles et unités restent dépendants du matériel ; ne pas extrapoler la compatibilité à tous les processeurs Intel.

Références techniques : [compteurs Intel, manuel système](https://cdrdv2-public.intel.com/819715/253669-sdm-vol-3b.pdf), [implémentation RAPL du noyau Linux](https://github.com/torvalds/linux/blob/master/drivers/powercap/intel_rapl_common.c).

## Travaux encore nécessaires

1. Acquisition périodique, compatibilité des domaines et validation des unités sur une machine Linux/Intel identifiée.
2. Références indépendantes pour tous les benchmarks et contrôle obligatoire avant campagne.
3. Manifeste de campagne, échauffement, ordre randomisé et répétitions indépendantes.
4. Nouvelle campagne INR distincte des CSV historiques ; incertitude et sensibilité des conclusions aux filtres.
