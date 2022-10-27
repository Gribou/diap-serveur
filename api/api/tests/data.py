APPS = {
    'epeires': {
        "title": "Epeires²",
        "internal_url": "https://epeires2.crnan/epeires2/",
        "tablet": {
            "color": "#ffc107",
            "textColor": "#fff",
        },

    },
    'wikiff': {
        "title": "WikiFF",
        "internal_url": "https://wikiff.crnan/wikiff/index.php/",
        "external_url":
        "https://wikiff.crna-n.aviation-civile.gouv.fr/wikiff/index.php/",
        "tablet": {
            "color": "#37a9e1",
            "textColor": "#fff",
            "tablet_title": "MANEX",
        },
    },
    'reflex': {
        "title": "Fiches réflexes",
        "internal_url":
        "https://wikiff.crnan/wikiff/index.php/Fiches_r%C3%A9flexes_PC",
        "tablet": {
            "color": "#f44336",
            "textColor": "#fff",
        },
    },
    'meteo': {
        "title": "Météo France",
        "external_url": "https://pro.meteofrance.com",
        "tablet": {
            "color":  "#005891",
            "textColor": "#fff",
            "tablet_title": "Météo",
            "info": "<strong>Identifiant :</strong> CRNA-N<br/><strong>Mot de passe :</strong> LF-F91!"
        },
    },
    '4me': {
        "title": "4Me",
        "internal_url": "http://4mesvr0:3000/",
        "tablet": {
            "color": "#424242",
            "textColor": "#fff",
        }
    },
    'efne': {
        "title": "eFNE",
        "internal_url": "https://apps.crnan/efne/",
        "tablet": {
            "color": "#00bcd4",
            "textColor": "#fff",
        },
    },
    'coconuts': {
        "title": "Coconuts",
        "internal_url": "https://apps.crnan/coconuts/",
        "external_url":
        "https://apps.crna-n.aviation-civile.gouv.fr/coconuts/",
        "tablet": {
            "color": "#4caf50",
            "textColor": "#fff",
            "tablet_title": "Cartes",
        },

    },
    'enews': {
        "title": "eNews",
        "internal_url": "https://apps.crnan/enews/",
        "external_url": "https://apps.crna-n.aviation-civile.gouv.fr/enews/",
        "tablet": {
            "color": "#3f51b5",
            "tablet_title": "Consignes",
        },

    },
    'olaf': {
        "title": "OLAFATCO",
        "external_url": "https://olafatco.dsna.aviation-civile.gouv.fr",
    },
    "outlook": {
        "title": "Outlook",
        "external_url": "https://outlook.office.com/mail/inbox",

    },
    "sia": {
        "title": "SIA",
        "external_url": "https://www.sia.aviation-civile.gouv.fr/"
    }
}

GRID = [['reflex', 'meteo', 'efne'], ['wikiff', 'enews', 'coconuts']]
DEFAULT_PROFILE = 'atco'

SEARCH_ENGINES = [
    {
        'name': 'eNews',
        'template_url': '{root_url}docs?search={search_query}'
    }, {
        'name': 'Coconuts',
        'template_url': '{root_url}maps?search={search_query}'
    }, {
        'name': 'WikiFF',
        'template_url': '{root_url}?search={search_query}&title=Sp%C3%A9cial%3ARecherche&go='
    }
]
