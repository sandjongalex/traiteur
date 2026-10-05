"""Temporary presentation data for the public site.

PROMPT 3 will progressively replace catalog-like entries with database-backed
content. Keeping them here prevents duplicated editorial data across templates.
"""

SERVICES = [
    {
        "title": "Mariages",
        "description": "Une prestation pensée pour accompagner votre réception avec élégance, de la table au service.",
        "icon": "rings",
    },
    {
        "title": "Anniversaires & cérémonies",
        "description": "Des formats chaleureux et adaptables pour célébrer les moments qui comptent.",
        "icon": "celebration",
    },
    {
        "title": "Buffets & cocktails",
        "description": "Des présentations conviviales et soignées pour recevoir avec fluidité.",
        "icon": "buffet",
    },
    {
        "title": "Événements d’entreprise",
        "description": "Une organisation professionnelle pour réunions, séminaires, conférences et réceptions.",
        "icon": "business",
    },
    {
        "title": "Livraison entreprise",
        "description": "Une solution pratique pour vos repas d’équipe et besoins professionnels planifiés.",
        "icon": "delivery",
    },
    {
        "title": "Prestations personnalisées",
        "description": "Un accompagnement construit autour de votre format, de vos invités et de vos priorités.",
        "icon": "tailored",
    },
]

CULINARY_CATEGORIES = [
    "Cuisine camerounaise",
    "Cuisine africaine",
    "Buffets",
    "Cocktails",
    "Grillades",
    "Desserts",
    "Boissons",
]

EVENT_TYPES = [
    "Mariage",
    "Anniversaire",
    "Baptême",
    "Réception privée",
    "Séminaire",
    "Conférence",
    "Cocktail",
    "Buffet",
    "Événement d’entreprise",
    "Cérémonie familiale",
]

PROCESS_STEPS = [
    ("01", "Parlez-nous de votre événement", "Partagez le type de réception, la date, le lieu et le nombre de personnes."),
    ("02", "Nous préparons votre proposition", "Nous analysons votre besoin avant de formuler une offre adaptée."),
    ("03", "Vous validez votre prestation", "Le devis final est confirmé avec vous avant toute exécution."),
    ("04", "DNP DECO prépare votre événement", "Cuisine, service et organisation sont coordonnés selon la prestation retenue."),
    ("05", "Profitez de votre réception", "Notre objectif : vous permettre de vivre le moment avec plus de sérénité."),
]

WHY_US = [
    ("Cuisine préparée avec soin", "Une attention portée aux saveurs, à la présentation et à la cohérence du service."),
    ("Organisation professionnelle", "Un déroulé structuré pour réduire les imprévus et mieux coordonner la prestation."),
    ("Accompagnement personnalisé", "Chaque demande est étudiée selon le contexte réel de votre événement."),
    ("Présentation élégante", "Une expérience visuelle sobre et soignée, pensée pour valoriser votre réception."),
]

GALLERY_ITEMS = [
    {"title": "Réception élégante", "category": "Réception", "image": "images/gallery-reception.svg"},
    {"title": "Buffet convivial", "category": "Buffet", "image": "images/gallery-buffet.svg"},
    {"title": "Table de cérémonie", "category": "Cérémonie", "image": "images/gallery-table.svg"},
    {"title": "Cocktail professionnel", "category": "Entreprise", "image": "images/gallery-cocktail.svg"},
    {"title": "Expérience culinaire", "category": "Cuisine", "image": "images/gallery-cuisine.svg"},
    {"title": "Mise en place événementielle", "category": "Événement", "image": "images/gallery-event.svg"},
]
