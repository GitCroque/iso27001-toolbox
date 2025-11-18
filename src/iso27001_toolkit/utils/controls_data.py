"""
Données des 114 contrôles ISO 27001:2022 (Annexe A)
"""

from typing import Dict, List, Optional


# Définition complète des 114 contrôles ISO 27001:2022
ISO27001_CONTROLS = [
    # A.5 - Contrôles organisationnels (37 contrôles)
    {
        "id": "A.5.1",
        "category": "A.5",
        "category_name": "Contrôles organisationnels",
        "name": "Politiques de sécurité de l'information",
        "type": "Organizational",
        "description": "Une politique de sécurité de l'information et des politiques spécifiques aux sujets doivent être définies, approuvées par la direction, publiées, communiquées et reconnues par le personnel et les parties concernées pertinentes, et revues à intervalles planifiés et en cas de changements significatifs.",
        "purpose": "Fournir l'orientation et le soutien de la direction pour la sécurité de l'information conformément aux exigences métier et aux lois et réglementations pertinentes."
    },
    {
        "id": "A.5.2",
        "category": "A.5",
        "category_name": "Contrôles organisationnels",
        "name": "Rôles et responsabilités en matière de sécurité de l'information",
        "type": "Organizational",
        "description": "Les rôles et responsabilités en matière de sécurité de l'information doivent être définis et attribués conformément aux besoins de l'organisation.",
        "purpose": "Établir et communiquer les rôles et responsabilités en matière de sécurité de l'information dans toute l'organisation."
    },
    {
        "id": "A.5.3",
        "category": "A.5",
        "category_name": "Contrôles organisationnels",
        "name": "Séparation des tâches",
        "type": "Organizational",
        "description": "Les tâches et les domaines de responsabilité en conflit doivent être séparés.",
        "purpose": "Réduire les opportunités de modification non autorisée ou non intentionnelle ou de mauvais usage des actifs de l'organisation."
    },
    {
        "id": "A.5.4",
        "category": "A.5",
        "category_name": "Contrôles organisationnels",
        "name": "Responsabilités de la direction",
        "type": "Organizational",
        "description": "La direction doit exiger que tout le personnel et les contractants appliquent la sécurité de l'information conformément aux politiques, procédures et contrôles établis de l'organisation.",
        "purpose": "Assigner la responsabilité de la sécurité de l'information conformément aux politiques de l'organisation."
    },
    {
        "id": "A.5.5",
        "category": "A.5",
        "category_name": "Contrôles organisationnels",
        "name": "Contact avec les autorités",
        "type": "Organizational",
        "description": "L'organisation doit établir et maintenir un contact avec les autorités pertinentes.",
        "purpose": "Assurer que l'organisation dispose d'un point de contact approprié avec les autorités pertinentes."
    },
    {
        "id": "A.5.6",
        "category": "A.5",
        "category_name": "Contrôles organisationnels",
        "name": "Contact avec les groupes d'intérêt spéciaux",
        "type": "Organizational",
        "description": "L'organisation doit établir et maintenir un contact avec les groupes d'intérêt spéciaux ou d'autres forums de spécialistes en sécurité et associations professionnelles.",
        "purpose": "Maintenir la connaissance de l'organisation des meilleures pratiques en sécurité de l'information et se tenir au courant des informations pertinentes."
    },
    {
        "id": "A.5.7",
        "category": "A.5",
        "category_name": "Contrôles organisationnels",
        "name": "Threat intelligence",
        "type": "Organizational",
        "description": "Les informations relatives aux menaces de sécurité de l'information doivent être collectées et analysées pour produire de la threat intelligence.",
        "purpose": "Assurer que l'organisation est au courant des menaces de sécurité de l'information."
    },
    {
        "id": "A.5.8",
        "category": "A.5",
        "category_name": "Contrôles organisationnels",
        "name": "Sécurité de l'information dans la gestion de projet",
        "type": "Organizational",
        "description": "La sécurité de l'information doit être intégrée dans la gestion de projet.",
        "purpose": "Assurer que la sécurité de l'information fait partie de la gestion de projet indépendamment du type de projet."
    },
    {
        "id": "A.5.9",
        "category": "A.5",
        "category_name": "Contrôles organisationnels",
        "name": "Inventaire des informations et autres actifs associés",
        "type": "Organizational",
        "description": "Un inventaire des informations et autres actifs associés, y compris les propriétaires, doit être développé et maintenu.",
        "purpose": "Identifier les actifs de l'organisation afin d'assurer une protection appropriée."
    },
    {
        "id": "A.5.10",
        "category": "A.5",
        "category_name": "Contrôles organisationnels",
        "name": "Usage acceptable des informations et autres actifs associés",
        "type": "Organizational",
        "description": "Des règles d'usage acceptable des informations et autres actifs associés doivent être identifiées, documentées et mises en œuvre.",
        "purpose": "Assurer que les informations et autres actifs associés sont utilisés uniquement à des fins autorisées."
    },
    {
        "id": "A.5.11",
        "category": "A.5",
        "category_name": "Contrôles organisationnels",
        "name": "Restitution des actifs",
        "type": "Organizational",
        "description": "Le personnel et les autres parties intéressées doivent restituer tous les actifs de l'organisation en leur possession à la fin de leur emploi, contrat ou accord.",
        "purpose": "Protéger les actifs de l'organisation après la cessation d'emploi, de contrat ou d'accord."
    },
    {
        "id": "A.5.12",
        "category": "A.5",
        "category_name": "Contrôles organisationnels",
        "name": "Classification de l'information",
        "type": "Organizational",
        "description": "L'information doit être classifiée selon les besoins de sécurité de l'information de l'organisation sur la base de la confidentialité, de l'intégrité, de la disponibilité et des exigences des parties intéressées pertinentes.",
        "purpose": "Assurer que l'information reçoit un niveau approprié de protection conformément à son importance pour l'organisation."
    },
    {
        "id": "A.5.13",
        "category": "A.5",
        "category_name": "Contrôles organisationnels",
        "name": "Étiquetage de l'information",
        "type": "Organizational",
        "description": "Un ensemble approprié d'étiquettes pour l'information doit être développé et mis en œuvre conformément au schéma de classification de l'information adopté par l'organisation.",
        "purpose": "Assurer que l'importance de l'information est connue et comprise."
    },
    {
        "id": "A.5.14",
        "category": "A.5",
        "category_name": "Contrôles organisationnels",
        "name": "Transfert d'information",
        "type": "Organizational",
        "description": "Des règles, procédures ou accords de transfert d'information doivent être en place pour tous les types d'installations de transfert au sein de l'organisation et entre l'organisation et les autres parties.",
        "purpose": "Maintenir la sécurité de l'information transférée au sein d'une organisation et avec toute entité externe."
    },
    {
        "id": "A.5.15",
        "category": "A.5",
        "category_name": "Contrôles organisationnels",
        "name": "Contrôle d'accès",
        "type": "Organizational",
        "description": "Des règles pour contrôler l'accès physique et logique aux informations et autres actifs associés doivent être établies et mises en œuvre sur la base des exigences métier et de sécurité de l'information.",
        "purpose": "Limiter l'accès aux informations et autres actifs associés."
    },
    {
        "id": "A.5.16",
        "category": "A.5",
        "category_name": "Contrôles organisationnels",
        "name": "Gestion des identités",
        "type": "Organizational",
        "description": "Le cycle de vie complet des identités doit être géré.",
        "purpose": "Gérer le cycle de vie des identités d'utilisateurs ayant accès aux informations et autres actifs associés."
    },
    {
        "id": "A.5.17",
        "category": "A.5",
        "category_name": "Contrôles organisationnels",
        "name": "Informations d'authentification",
        "type": "Organizational",
        "description": "L'allocation et la gestion des informations d'authentification doivent être contrôlées par un processus de gestion, y compris l'avis au personnel sur la gestion appropriée des informations d'authentification.",
        "purpose": "Assurer que les informations d'authentification sont gérées de manière sécurisée."
    },
    {
        "id": "A.5.18",
        "category": "A.5",
        "category_name": "Contrôles organisationnels",
        "name": "Droits d'accès",
        "type": "Organizational",
        "description": "Les droits d'accès aux informations et autres actifs associés doivent être provisionnés, revus, modifiés et supprimés conformément aux règles de contrôle d'accès spécifiques aux sujets de l'organisation et aux règles d'accès.",
        "purpose": "Assurer que l'accès autorisé est accordé et que l'accès non autorisé est empêché."
    },
    {
        "id": "A.5.19",
        "category": "A.5",
        "category_name": "Contrôles organisationnels",
        "name": "Sécurité de l'information dans les relations avec les fournisseurs",
        "type": "Organizational",
        "description": "Des processus et procédures doivent être définis et mis en œuvre pour gérer les risques de sécurité de l'information associés à l'utilisation de produits ou services des fournisseurs.",
        "purpose": "Maintenir un niveau approprié de sécurité de l'information et de prestation de service aligné avec les accords fournisseurs."
    },
    {
        "id": "A.5.20",
        "category": "A.5",
        "category_name": "Contrôles organisationnels",
        "name": "Traitement de la sécurité de l'information dans les accords fournisseurs",
        "type": "Organizational",
        "description": "Les exigences pertinentes de sécurité de l'information doivent être établies et convenues avec chaque fournisseur en fonction du type de relation fournisseur.",
        "purpose": "Assurer que les exigences de sécurité de l'information de l'organisation sont convenues et respectées par les fournisseurs."
    },
    {
        "id": "A.5.21",
        "category": "A.5",
        "category_name": "Contrôles organisationnels",
        "name": "Gestion de la sécurité de l'information dans la chaîne d'approvisionnement des TIC",
        "type": "Organizational",
        "description": "Des processus et procédures doivent être définis et mis en œuvre pour gérer les risques de sécurité de l'information associés à la chaîne d'approvisionnement des produits et services TIC.",
        "purpose": "Réduire les risques de sécurité de l'information associés à la chaîne d'approvisionnement des produits et services TIC de l'organisation."
    },
    {
        "id": "A.5.22",
        "category": "A.5",
        "category_name": "Contrôles organisationnels",
        "name": "Surveillance, revue et gestion du changement des services fournisseurs",
        "type": "Organizational",
        "description": "L'organisation doit surveiller, revoir, évaluer et gérer régulièrement les changements dans les pratiques de sécurité de l'information des fournisseurs et la prestation de services.",
        "purpose": "Maintenir le niveau convenu de sécurité de l'information et de prestation de service par les fournisseurs."
    },
    {
        "id": "A.5.23",
        "category": "A.5",
        "category_name": "Contrôles organisationnels",
        "name": "Sécurité de l'information pour l'utilisation de services cloud",
        "type": "Organizational",
        "description": "Les processus d'acquisition, d'utilisation, de gestion et de sortie de services cloud doivent être établis conformément aux exigences de sécurité de l'information de l'organisation.",
        "purpose": "Gérer les risques de sécurité de l'information associés à l'utilisation de services cloud."
    },
    {
        "id": "A.5.24",
        "category": "A.5",
        "category_name": "Contrôles organisationnels",
        "name": "Planification et préparation de la gestion des incidents de sécurité de l'information",
        "type": "Organizational",
        "description": "L'organisation doit planifier et préparer la gestion des incidents de sécurité de l'information en définissant, établissant et communiquant des processus, rôles et responsabilités de gestion des incidents de sécurité de l'information.",
        "purpose": "Assurer une approche rapide, efficace et ordonnée pour gérer les incidents de sécurité de l'information."
    },
    {
        "id": "A.5.25",
        "category": "A.5",
        "category_name": "Contrôles organisationnels",
        "name": "Évaluation et décision des événements de sécurité de l'information",
        "type": "Organizational",
        "description": "L'organisation doit évaluer les événements de sécurité de l'information et décider s'ils doivent être catégorisés comme incidents de sécurité de l'information.",
        "purpose": "Assurer que les événements de sécurité de l'information sont évalués de manière cohérente et efficace."
    },
    {
        "id": "A.5.26",
        "category": "A.5",
        "category_name": "Contrôles organisationnels",
        "name": "Réponse aux incidents de sécurité de l'information",
        "type": "Organizational",
        "description": "Les incidents de sécurité de l'information doivent être traités conformément aux procédures documentées.",
        "purpose": "Assurer une réponse efficace et rapide aux incidents de sécurité de l'information."
    },
    {
        "id": "A.5.27",
        "category": "A.5",
        "category_name": "Contrôles organisationnels",
        "name": "Apprentissage des incidents de sécurité de l'information",
        "type": "Organizational",
        "description": "Les connaissances acquises de l'analyse et de la résolution des incidents de sécurité de l'information doivent être utilisées pour réduire la probabilité ou l'impact d'incidents futurs.",
        "purpose": "Améliorer continuellement les mesures de sécurité de l'information."
    },
    {
        "id": "A.5.28",
        "category": "A.5",
        "category_name": "Contrôles organisationnels",
        "name": "Collection de preuves",
        "type": "Organizational",
        "description": "L'organisation doit établir et mettre en œuvre des procédures pour l'identification, la collecte, l'acquisition et la préservation de preuves relatives aux événements de sécurité de l'information.",
        "purpose": "Assurer que l'organisation peut fournir des preuves conformément aux lois et réglementations applicables."
    },
    {
        "id": "A.5.29",
        "category": "A.5",
        "category_name": "Contrôles organisationnels",
        "name": "Sécurité de l'information pendant la perturbation",
        "type": "Organizational",
        "description": "L'organisation doit planifier comment maintenir la sécurité de l'information à un niveau approprié pendant une perturbation.",
        "purpose": "Assurer la disponibilité de la sécurité de l'information pendant les situations adverses."
    },
    {
        "id": "A.5.30",
        "category": "A.5",
        "category_name": "Contrôles organisationnels",
        "name": "Préparation des TIC pour la continuité d'activité",
        "type": "Organizational",
        "description": "La préparation des TIC doit être planifiée, mise en œuvre, maintenue et testée sur la base des objectifs de continuité d'activité et des exigences de continuité des TIC.",
        "purpose": "Assurer la disponibilité des installations de traitement de l'information."
    },
    {
        "id": "A.5.31",
        "category": "A.5",
        "category_name": "Contrôles organisationnels",
        "name": "Exigences légales, statutaires, réglementaires et contractuelles",
        "type": "Organizational",
        "description": "Les exigences légales, statutaires, réglementaires et contractuelles pertinentes pour la sécurité de l'information et l'approche de l'organisation pour répondre à ces exigences doivent être identifiées, documentées et tenues à jour.",
        "purpose": "Éviter les violations des obligations légales, statutaires, réglementaires ou contractuelles liées à la sécurité de l'information."
    },
    {
        "id": "A.5.32",
        "category": "A.5",
        "category_name": "Contrôles organisationnels",
        "name": "Droits de propriété intellectuelle",
        "type": "Organizational",
        "description": "L'organisation doit mettre en œuvre des procédures appropriées pour protéger les droits de propriété intellectuelle.",
        "purpose": "Assurer la conformité avec les exigences légales, statutaires, réglementaires et contractuelles liées aux droits de propriété intellectuelle et à l'utilisation de produits logiciels propriétaires."
    },
    {
        "id": "A.5.33",
        "category": "A.5",
        "category_name": "Contrôles organisationnels",
        "name": "Protection des enregistrements",
        "type": "Organizational",
        "description": "Les enregistrements doivent être protégés contre la perte, la destruction, la falsification, l'accès non autorisé et la divulgation non autorisée.",
        "purpose": "Assurer que les enregistrements sont protégés conformément aux exigences légales, réglementaires, contractuelles et métier."
    },
    {
        "id": "A.5.34",
        "category": "A.5",
        "category_name": "Contrôles organisationnels",
        "name": "Vie privée et protection des PII",
        "type": "Organizational",
        "description": "L'organisation doit identifier et satisfaire aux exigences concernant la préservation de la vie privée et la protection des informations personnellement identifiables (PII) selon les lois et réglementations applicables et les exigences contractuelles.",
        "purpose": "Assurer la conformité avec les exigences légales et contractuelles concernant la vie privée et la protection des PII."
    },
    {
        "id": "A.5.35",
        "category": "A.5",
        "category_name": "Contrôles organisationnels",
        "name": "Revue indépendante de la sécurité de l'information",
        "type": "Organizational",
        "description": "L'approche de l'organisation pour gérer la sécurité de l'information et sa mise en œuvre, y compris les personnes, les processus et les technologies, doit être revue indépendamment à intervalles planifiés ou lorsque des changements significatifs se produisent.",
        "purpose": "Assurer que l'approche de l'organisation pour gérer la sécurité de l'information et sa mise en œuvre reste appropriée et efficace."
    },
    {
        "id": "A.5.36",
        "category": "A.5",
        "category_name": "Contrôles organisationnels",
        "name": "Conformité aux politiques, règles et normes de sécurité de l'information",
        "type": "Organizational",
        "description": "La conformité aux politiques, règles et normes de sécurité de l'information de l'organisation doit être revue régulièrement.",
        "purpose": "Assurer que la sécurité de l'information est mise en œuvre et opérée conformément aux politiques, règles et normes de l'organisation."
    },
    {
        "id": "A.5.37",
        "category": "A.5",
        "category_name": "Contrôles organisationnels",
        "name": "Procédures opérationnelles documentées",
        "type": "Organizational",
        "description": "Les procédures opérationnelles pour les installations de traitement de l'information doivent être documentées et mises à disposition de tout le personnel qui en a besoin.",
        "purpose": "Assurer l'opération correcte et sécurisée des installations de traitement de l'information."
    },

    # A.6 - Contrôles relatifs aux personnes (8 contrôles)
    {
        "id": "A.6.1",
        "category": "A.6",
        "category_name": "Contrôles relatifs aux personnes",
        "name": "Filtrage",
        "type": "People",
        "description": "Des vérifications préalables sur tous les candidats à l'emploi doivent être effectuées conformément aux lois, réglementations et éthique pertinentes et proportionnellement aux exigences métier, à la classification des informations auxquelles ils auront accès et aux risques perçus.",
        "purpose": "Assurer que le personnel et les contractants comprennent leurs responsabilités et sont appropriés pour les rôles pour lesquels ils sont considérés."
    },
    {
        "id": "A.6.2",
        "category": "A.6",
        "category_name": "Contrôles relatifs aux personnes",
        "name": "Termes et conditions d'emploi",
        "type": "People",
        "description": "Les accords contractuels avec le personnel et les contractants doivent stipuler leurs responsabilités et celles de l'organisation en matière de sécurité de l'information.",
        "purpose": "Assurer que le personnel et les contractants comprennent leurs responsabilités en matière de sécurité de l'information."
    },
    {
        "id": "A.6.3",
        "category": "A.6",
        "category_name": "Contrôles relatifs aux personnes",
        "name": "Sensibilisation, éducation et formation à la sécurité de l'information",
        "type": "People",
        "description": "Le personnel de l'organisation et les parties concernées pertinentes doivent recevoir une sensibilisation, une éducation et une formation appropriées en matière de sécurité de l'information et des mises à jour régulières des politiques et procédures de l'organisation, selon leur fonction professionnelle.",
        "purpose": "Assurer que le personnel et les parties concernées pertinentes comprennent leur responsabilité en matière de sécurité de l'information."
    },
    {
        "id": "A.6.4",
        "category": "A.6",
        "category_name": "Contrôles relatifs aux personnes",
        "name": "Processus disciplinaire",
        "type": "People",
        "description": "Un processus disciplinaire formel doit être en place pour prendre des mesures contre le personnel et les autres parties concernées pertinentes qui ont commis une violation de la sécurité de l'information.",
        "purpose": "Assurer que le personnel et les autres parties concernées pertinentes comprennent les conséquences des violations de sécurité de l'information."
    },
    {
        "id": "A.6.5",
        "category": "A.6",
        "category_name": "Contrôles relatifs aux personnes",
        "name": "Responsabilités après la fin de l'emploi ou du changement d'emploi",
        "type": "People",
        "description": "Les responsabilités et devoirs de sécurité de l'information qui restent valides après la fin ou le changement d'emploi doivent être définis, communiqués au personnel ou autre partie concernée et appliqués.",
        "purpose": "Protéger les intérêts de l'organisation dans le cadre du processus de changement ou de fin d'emploi."
    },
    {
        "id": "A.6.6",
        "category": "A.6",
        "category_name": "Contrôles relatifs aux personnes",
        "name": "Accords de confidentialité ou de non-divulgation",
        "type": "People",
        "description": "Des accords de confidentialité ou de non-divulgation reflétant les besoins de l'organisation pour la protection de l'information doivent être identifiés, documentés, régulièrement revus et signés par le personnel et les autres parties concernées pertinentes.",
        "purpose": "Protéger l'information confidentielle en utilisant des accords de confidentialité ou de non-divulgation."
    },
    {
        "id": "A.6.7",
        "category": "A.6",
        "category_name": "Contrôles relatifs aux personnes",
        "name": "Travail à distance",
        "type": "People",
        "description": "Des mesures de sécurité doivent être mises en œuvre lorsque le personnel travaille à distance pour protéger les informations auxquelles on accède, les informations traitées ou stockées en dehors des locaux de l'organisation.",
        "purpose": "Assurer la sécurité de l'information lorsque le personnel travaille à distance."
    },
    {
        "id": "A.6.8",
        "category": "A.6",
        "category_name": "Contrôles relatifs aux personnes",
        "name": "Signalement des événements de sécurité de l'information",
        "type": "People",
        "description": "L'organisation doit fournir un mécanisme permettant au personnel de signaler les événements de sécurité de l'information observés ou suspectés par un canal disponible, accessible et défini.",
        "purpose": "Assurer que les événements de sécurité de l'information affectant l'organisation sont signalés rapidement."
    },

    # A.7 - Contrôles physiques (14 contrôles)
    {
        "id": "A.7.1",
        "category": "A.7",
        "category_name": "Contrôles physiques",
        "name": "Périmètres de sécurité physique",
        "type": "Physical",
        "description": "Des périmètres de sécurité doivent être définis et utilisés pour protéger les zones qui contiennent des informations et autres actifs associés.",
        "purpose": "Prévenir l'accès physique non autorisé, les dommages et les interférences aux locaux et informations de l'organisation."
    },
    {
        "id": "A.7.2",
        "category": "A.7",
        "category_name": "Contrôles physiques",
        "name": "Entrée physique",
        "type": "Physical",
        "description": "Les zones sécurisées doivent être protégées par des contrôles d'entrée appropriés et des points d'accès.",
        "purpose": "Assurer que seul le personnel autorisé a accès aux zones sécurisées."
    },
    {
        "id": "A.7.3",
        "category": "A.7",
        "category_name": "Contrôles physiques",
        "name": "Sécurisation des bureaux, salles et installations",
        "type": "Physical",
        "description": "La sécurité physique des bureaux, salles et installations doit être conçue et mise en œuvre.",
        "purpose": "Prévenir l'accès physique non autorisé, les dommages et les interférences aux informations et autres actifs associés de l'organisation."
    },
    {
        "id": "A.7.4",
        "category": "A.7",
        "category_name": "Contrôles physiques",
        "name": "Surveillance de la sécurité physique",
        "type": "Physical",
        "description": "Les locaux doivent être continuellement surveillés pour détecter les accès physiques non autorisés.",
        "purpose": "Détecter et dissuader les accès physiques non autorisés."
    },
    {
        "id": "A.7.5",
        "category": "A.7",
        "category_name": "Contrôles physiques",
        "name": "Protection contre les menaces physiques et environnementales",
        "type": "Physical",
        "description": "Une protection contre les menaces physiques et environnementales, telles que les catastrophes naturelles et les attaques physiques délibérées ou accidentelles, doit être conçue et mise en œuvre.",
        "purpose": "Prévenir la perte, les dommages, le vol ou la compromission d'actifs et l'interruption des opérations de l'organisation."
    },
    {
        "id": "A.7.6",
        "category": "A.7",
        "category_name": "Contrôles physiques",
        "name": "Travail dans des zones sécurisées",
        "type": "Physical",
        "description": "Des mesures de sécurité pour le travail dans des zones sécurisées doivent être conçues et mises en œuvre.",
        "purpose": "Prévenir l'accès non autorisé, les dommages et les interférences aux informations et autres actifs associés dans les zones sécurisées."
    },
    {
        "id": "A.7.7",
        "category": "A.7",
        "category_name": "Contrôles physiques",
        "name": "Bureau propre et écran propre",
        "type": "Physical",
        "description": "Des règles de bureau propre pour les papiers et supports de stockage amovibles et des règles d'écran propre pour les installations de traitement de l'information doivent être définies et appliquées de manière appropriée.",
        "purpose": "Réduire les risques d'accès non autorisé, de perte et de destruction d'informations pendant et en dehors des heures de travail normales."
    },
    {
        "id": "A.7.8",
        "category": "A.7",
        "category_name": "Contrôles physiques",
        "name": "Emplacement et protection des équipements",
        "type": "Physical",
        "description": "Les équipements doivent être situés de manière sécurisée et protégés.",
        "purpose": "Prévenir la perte, les dommages, le vol ou la compromission d'actifs et l'interruption des opérations de l'organisation."
    },
    {
        "id": "A.7.9",
        "category": "A.7",
        "category_name": "Contrôles physiques",
        "name": "Sécurité des actifs hors des locaux",
        "type": "Physical",
        "description": "Les actifs hors site doivent être protégés.",
        "purpose": "Prévenir la perte, les dommages, le vol ou la compromission d'actifs et l'interruption des opérations de l'organisation."
    },
    {
        "id": "A.7.10",
        "category": "A.7",
        "category_name": "Contrôles physiques",
        "name": "Supports de stockage",
        "type": "Physical",
        "description": "Les supports de stockage doivent être gérés tout au long de leur cycle de vie d'acquisition, d'utilisation, de transport et d'élimination conformément au schéma de classification de l'organisation et aux exigences de manipulation.",
        "purpose": "Prévenir la divulgation, la modification, la suppression ou la destruction non autorisée d'informations stockées sur des supports."
    },
    {
        "id": "A.7.11",
        "category": "A.7",
        "category_name": "Contrôles physiques",
        "name": "Services de support",
        "type": "Physical",
        "description": "Les installations de traitement de l'information doivent être protégées contre les pannes d'alimentation et autres perturbations causées par des défaillances des services de support.",
        "purpose": "Assurer la disponibilité des installations de traitement de l'information."
    },
    {
        "id": "A.7.12",
        "category": "A.7",
        "category_name": "Contrôles physiques",
        "name": "Sécurité du câblage",
        "type": "Physical",
        "description": "Les câbles transportant de l'énergie, des données ou supportant des services d'information doivent être protégés contre l'interception, l'interférence ou les dommages.",
        "purpose": "Prévenir la perte, les dommages ou la compromission d'actifs et l'interruption des opérations de l'organisation."
    },
    {
        "id": "A.7.13",
        "category": "A.7",
        "category_name": "Contrôles physiques",
        "name": "Maintenance des équipements",
        "type": "Physical",
        "description": "Les équipements doivent être maintenus correctement pour assurer la disponibilité, l'intégrité et la confidentialité des informations.",
        "purpose": "Assurer le fonctionnement continu correct et sécurisé des équipements pour supporter la disponibilité, l'intégrité et la confidentialité des informations."
    },
    {
        "id": "A.7.14",
        "category": "A.7",
        "category_name": "Contrôles physiques",
        "name": "Élimination ou réutilisation sécurisée des équipements",
        "type": "Physical",
        "description": "Les éléments d'équipement contenant des supports de stockage doivent être vérifiés pour s'assurer que toutes les données sensibles et logiciels sous licence ont été supprimés ou écrasés de manière sécurisée avant l'élimination ou la réutilisation.",
        "purpose": "Prévenir les fuites d'informations ou la perte d'intégrité des informations."
    },

    # A.8 - Contrôles technologiques (34 contrôles)
    {
        "id": "A.8.1",
        "category": "A.8",
        "category_name": "Contrôles technologiques",
        "name": "Dispositifs d'extrémité utilisateur",
        "type": "Technological",
        "description": "Les informations stockées sur, traitées par ou accessibles via des dispositifs d'extrémité utilisateur doivent être protégées.",
        "purpose": "Assurer la protection des informations sur les dispositifs d'extrémité utilisateur."
    },
    {
        "id": "A.8.2",
        "category": "A.8",
        "category_name": "Contrôles technologiques",
        "name": "Droits d'accès privilégiés",
        "type": "Technological",
        "description": "L'allocation et l'utilisation des droits d'accès privilégiés doivent être restreintes et gérées.",
        "purpose": "Prévenir la compromission des systèmes et applications."
    },
    {
        "id": "A.8.3",
        "category": "A.8",
        "category_name": "Contrôles technologiques",
        "name": "Restriction d'accès à l'information",
        "type": "Technological",
        "description": "L'accès aux informations et autres actifs associés doit être restreint conformément à la politique de contrôle d'accès établie.",
        "purpose": "Assurer que l'accès aux informations et autres actifs associés est limité conformément aux besoins de l'organisation."
    },
    {
        "id": "A.8.4",
        "category": "A.8",
        "category_name": "Contrôles technologiques",
        "name": "Accès au code source",
        "type": "Technological",
        "description": "L'accès en lecture et en écriture au code source, aux outils de développement et aux bibliothèques logicielles doit être géré de manière appropriée.",
        "purpose": "Prévenir l'introduction de fonctionnalités non autorisées, éviter les modifications non intentionnelles et maintenir la confidentialité de la propriété intellectuelle."
    },
    {
        "id": "A.8.5",
        "category": "A.8",
        "category_name": "Contrôles technologiques",
        "name": "Authentification sécurisée",
        "type": "Technological",
        "description": "Des technologies et procédures d'authentification sécurisées doivent être mises en œuvre sur la base des restrictions d'accès à l'information et de la politique de contrôle d'accès spécifique au sujet.",
        "purpose": "Assurer que l'accès aux systèmes et applications est limité aux utilisateurs autorisés."
    },
    {
        "id": "A.8.6",
        "category": "A.8",
        "category_name": "Contrôles technologiques",
        "name": "Gestion des capacités",
        "type": "Technological",
        "description": "L'utilisation des ressources doit être surveillée et ajustée en ligne avec les exigences de capacité actuelles et prévues.",
        "purpose": "Assurer les performances requises du système."
    },
    {
        "id": "A.8.7",
        "category": "A.8",
        "category_name": "Contrôles technologiques",
        "name": "Protection contre les logiciels malveillants",
        "type": "Technological",
        "description": "Une protection contre les logiciels malveillants doit être mise en œuvre et supportée par une sensibilisation appropriée des utilisateurs.",
        "purpose": "Assurer que l'information et les installations de traitement de l'information sont protégées contre les logiciels malveillants."
    },
    {
        "id": "A.8.8",
        "category": "A.8",
        "category_name": "Contrôles technologiques",
        "name": "Gestion des vulnérabilités techniques",
        "type": "Technological",
        "description": "Les informations sur les vulnérabilités techniques des systèmes d'information utilisés doivent être obtenues, l'exposition de l'organisation à ces vulnérabilités doit être évaluée et des mesures appropriées doivent être prises.",
        "purpose": "Prévenir l'exploitation des vulnérabilités techniques."
    },
    {
        "id": "A.8.9",
        "category": "A.8",
        "category_name": "Contrôles technologiques",
        "name": "Gestion de la configuration",
        "type": "Technological",
        "description": "Des configurations, y compris des configurations de sécurité, doivent être établies, documentées, mises en œuvre, surveillées et revues pour le matériel, les logiciels, les services et les réseaux.",
        "purpose": "Assurer que les systèmes sont configurés de manière cohérente et sécurisée."
    },
    {
        "id": "A.8.10",
        "category": "A.8",
        "category_name": "Contrôles technologiques",
        "name": "Suppression de l'information",
        "type": "Technological",
        "description": "Les informations stockées dans des systèmes d'information, dispositifs ou autres supports de stockage doivent être supprimées lorsqu'elles ne sont plus nécessaires.",
        "purpose": "Prévenir l'exposition ou la divulgation non nécessaire d'informations."
    },
    {
        "id": "A.8.11",
        "category": "A.8",
        "category_name": "Contrôles technologiques",
        "name": "Masquage de données",
        "type": "Technological",
        "description": "Le masquage de données doit être utilisé conformément à la politique de contrôle d'accès spécifique au sujet de l'organisation et aux exigences métier et légales applicables.",
        "purpose": "Limiter l'exposition de données sensibles."
    },
    {
        "id": "A.8.12",
        "category": "A.8",
        "category_name": "Contrôles technologiques",
        "name": "Prévention des fuites de données",
        "type": "Technological",
        "description": "Des mesures de prévention des fuites de données doivent être appliquées aux systèmes, réseaux et autres dispositifs qui traitent, stockent ou transmettent des informations sensibles.",
        "purpose": "Détecter et prévenir la divulgation et l'extraction non autorisées d'informations."
    },
    {
        "id": "A.8.13",
        "category": "A.8",
        "category_name": "Contrôles technologiques",
        "name": "Sauvegarde de l'information",
        "type": "Technological",
        "description": "Des copies de sauvegarde des informations, logiciels et systèmes doivent être maintenues et testées régulièrement conformément à la politique de sauvegarde convenue.",
        "purpose": "Protéger contre la perte de données."
    },
    {
        "id": "A.8.14",
        "category": "A.8",
        "category_name": "Contrôles technologiques",
        "name": "Redondance des installations de traitement de l'information",
        "type": "Technological",
        "description": "Les installations de traitement de l'information doivent être mises en œuvre avec une redondance suffisante pour répondre aux exigences de disponibilité.",
        "purpose": "Assurer la disponibilité des installations de traitement de l'information."
    },
    {
        "id": "A.8.15",
        "category": "A.8",
        "category_name": "Contrôles technologiques",
        "name": "Journalisation",
        "type": "Technological",
        "description": "Des journaux qui enregistrent les activités, exceptions, fautes et autres événements pertinents doivent être produits, stockés, protégés et analysés.",
        "purpose": "Enregistrer les événements et générer des preuves."
    },
    {
        "id": "A.8.16",
        "category": "A.8",
        "category_name": "Contrôles technologiques",
        "name": "Activités de surveillance",
        "type": "Technological",
        "description": "Les réseaux, systèmes et applications doivent être surveillés pour détecter les comportements anormaux et les actions appropriées doivent être prises pour évaluer les incidents de sécurité de l'information potentiels.",
        "purpose": "Détecter les comportements anormaux et les incidents de sécurité de l'information potentiels."
    },
    {
        "id": "A.8.17",
        "category": "A.8",
        "category_name": "Contrôles technologiques",
        "name": "Synchronisation d'horloge",
        "type": "Technological",
        "description": "Les horloges des systèmes de traitement de l'information utilisés par l'organisation doivent être synchronisées avec des sources de temps approuvées.",
        "purpose": "Assurer l'exactitude des horodatages dans les enregistrements d'activité."
    },
    {
        "id": "A.8.18",
        "category": "A.8",
        "category_name": "Contrôles technologiques",
        "name": "Utilisation de programmes utilitaires privilégiés",
        "type": "Technological",
        "description": "L'utilisation de programmes utilitaires qui peuvent être capables de contourner les contrôles du système et de l'application doit être restreinte et étroitement contrôlée.",
        "purpose": "Prévenir le contournement des contrôles du système et de l'application."
    },
    {
        "id": "A.8.19",
        "category": "A.8",
        "category_name": "Contrôles technologiques",
        "name": "Installation de logiciels sur les systèmes opérationnels",
        "type": "Technological",
        "description": "Des procédures et mesures doivent être mises en œuvre pour gérer de manière sécurisée l'installation de logiciels sur les systèmes opérationnels.",
        "purpose": "Assurer l'intégrité des systèmes opérationnels."
    },
    {
        "id": "A.8.20",
        "category": "A.8",
        "category_name": "Contrôles technologiques",
        "name": "Sécurité des réseaux",
        "type": "Technological",
        "description": "Les réseaux et les dispositifs de réseau doivent être sécurisés, gérés et contrôlés pour protéger les informations dans les systèmes et applications.",
        "purpose": "Assurer la protection des informations dans les réseaux et la protection des installations de support."
    },
    {
        "id": "A.8.21",
        "category": "A.8",
        "category_name": "Contrôles technologiques",
        "name": "Sécurité des services de réseau",
        "type": "Technological",
        "description": "Les mécanismes de sécurité, niveaux de service et exigences de service des services de réseau doivent être identifiés, mis en œuvre et surveillés.",
        "purpose": "Assurer la sécurité des services de réseau."
    },
    {
        "id": "A.8.22",
        "category": "A.8",
        "category_name": "Contrôles technologiques",
        "name": "Ségrégation des réseaux",
        "type": "Technological",
        "description": "Des groupes de services d'information, utilisateurs et systèmes d'information doivent être ségrégués sur les réseaux de l'organisation.",
        "purpose": "Assurer la sécurité dans les réseaux."
    },
    {
        "id": "A.8.23",
        "category": "A.8",
        "category_name": "Contrôles technologiques",
        "name": "Filtrage Web",
        "type": "Technological",
        "description": "L'accès à des sites Web externes doit être géré pour réduire l'exposition aux contenus malveillants.",
        "purpose": "Réduire l'exposition aux contenus malveillants."
    },
    {
        "id": "A.8.24",
        "category": "A.8",
        "category_name": "Contrôles technologiques",
        "name": "Utilisation de la cryptographie",
        "type": "Technological",
        "description": "Des règles pour l'utilisation efficace de la cryptographie, y compris la gestion des clés cryptographiques, doivent être définies et mises en œuvre.",
        "purpose": "Assurer une utilisation correcte et efficace de la cryptographie pour protéger la confidentialité, l'authenticité et/ou l'intégrité de l'information."
    },
    {
        "id": "A.8.25",
        "category": "A.8",
        "category_name": "Contrôles technologiques",
        "name": "Cycle de vie de développement sécurisé",
        "type": "Technological",
        "description": "Des règles pour le développement sécurisé de logiciels et de systèmes doivent être établies et appliquées.",
        "purpose": "Assurer que la sécurité de l'information est conçue et mise en œuvre dans le cycle de vie de développement des systèmes d'information."
    },
    {
        "id": "A.8.26",
        "category": "A.8",
        "category_name": "Contrôles technologiques",
        "name": "Exigences de sécurité des applications",
        "type": "Technological",
        "description": "Les exigences de sécurité de l'information doivent être identifiées, spécifiées et approuvées lors du développement ou de l'acquisition d'applications.",
        "purpose": "Assurer que les applications sont conçues et mises en œuvre de manière sécurisée."
    },
    {
        "id": "A.8.27",
        "category": "A.8",
        "category_name": "Contrôles technologiques",
        "name": "Architecture système sécurisée et principes d'ingénierie",
        "type": "Technological",
        "description": "Des principes pour concevoir des systèmes sécurisés doivent être établis, documentés, maintenus et appliqués à toutes les activités de développement de systèmes d'information.",
        "purpose": "Assurer que la sécurité de l'information est intégrée dans les systèmes d'information."
    },
    {
        "id": "A.8.28",
        "category": "A.8",
        "category_name": "Contrôles technologiques",
        "name": "Codage sécurisé",
        "type": "Technological",
        "description": "Des principes de codage sécurisé doivent être appliqués au développement de logiciels.",
        "purpose": "Prévenir les vulnérabilités de sécurité dans les applications."
    },
    {
        "id": "A.8.29",
        "category": "A.8",
        "category_name": "Contrôles technologiques",
        "name": "Tests de sécurité en développement et en acceptation",
        "type": "Technological",
        "description": "Des processus de tests de sécurité doivent être définis et mis en œuvre dans le cycle de vie de développement.",
        "purpose": "Assurer que les contrôles de sécurité fonctionnent comme prévu."
    },
    {
        "id": "A.8.30",
        "category": "A.8",
        "category_name": "Contrôles technologiques",
        "name": "Développement externalisé",
        "type": "Technological",
        "description": "L'organisation doit diriger, surveiller et revoir les activités liées au développement de systèmes externalisé.",
        "purpose": "Maintenir la sécurité du développement de systèmes d'information externalisé."
    },
    {
        "id": "A.8.31",
        "category": "A.8",
        "category_name": "Contrôles technologiques",
        "name": "Séparation des environnements de développement, test et production",
        "type": "Technological",
        "description": "Les environnements de développement, test et production doivent être séparés et sécurisés.",
        "purpose": "Réduire les risques d'accès ou de changements non autorisés aux systèmes de production."
    },
    {
        "id": "A.8.32",
        "category": "A.8",
        "category_name": "Contrôles technologiques",
        "name": "Gestion des changements",
        "type": "Technological",
        "description": "Les changements aux installations de traitement de l'information et aux systèmes d'information doivent être soumis à des procédures de gestion des changements.",
        "purpose": "Assurer que la sécurité est maintenue lors des changements."
    },
    {
        "id": "A.8.33",
        "category": "A.8",
        "category_name": "Contrôles technologiques",
        "name": "Information de test",
        "type": "Technological",
        "description": "Les données de test doivent être sélectionnées, protégées et contrôlées de manière appropriée.",
        "purpose": "Assurer la protection des données opérationnelles utilisées pour les tests."
    },
    {
        "id": "A.8.34",
        "category": "A.8",
        "category_name": "Contrôles technologiques",
        "name": "Protection des systèmes d'information lors des tests d'audit",
        "type": "Technological",
        "description": "Les tests d'audit et autres activités d'assurance impliquant l'évaluation des systèmes de production doivent être planifiés et convenus entre le testeur et la direction appropriée.",
        "purpose": "Minimiser l'impact des tests d'audit sur les systèmes de production."
    }
]


def get_all_controls() -> List[Dict]:
    """Retourne tous les contrôles ISO 27001:2022"""
    return ISO27001_CONTROLS


def get_control_by_id(control_id: str) -> Optional[Dict]:
    """Retourne un contrôle spécifique par son ID"""
    for control in ISO27001_CONTROLS:
        if control['id'] == control_id.upper():
            return control
    return None


def get_controls_by_category(category: str) -> List[Dict]:
    """Retourne tous les contrôles d'une catégorie"""
    return [c for c in ISO27001_CONTROLS if c['category'] == category.upper()]


def get_controls_by_type(control_type: str) -> List[Dict]:
    """Retourne tous les contrôles d'un type"""
    return [c for c in ISO27001_CONTROLS if c['type'] == control_type]
