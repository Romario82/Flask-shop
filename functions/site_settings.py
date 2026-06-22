from db.connect_db import db
from db.models import SiteSettings

DEFAULTS = {
    'site_name': 'Shop',
    'default_title': 'Online Store',
    'default_description': 'Buy quality products in our online store.',
    'default_keywords': 'shop, store, products, online',
    'home_title': 'Home — Online Store',
    'home_description': 'Welcome to our online store. Best deals and fast delivery.',
    'robots': 'index, follow',
}


def get_site_settings():
    settings = SiteSettings.query.get(1)
    if not settings:
        settings = SiteSettings(id=1, **DEFAULTS)
        db.session.add(settings)
        db.session.commit()
    return settings


def settings_to_dict(settings):
    return {
        'site_name': settings.site_name or DEFAULTS['site_name'],
        'default_title': settings.default_title or DEFAULTS['default_title'],
        'default_description': settings.default_description or DEFAULTS['default_description'],
        'default_keywords': settings.default_keywords or DEFAULTS['default_keywords'],
        'home_title': settings.home_title or DEFAULTS['home_title'],
        'home_description': settings.home_description or DEFAULTS['home_description'],
        'robots': settings.robots or DEFAULTS['robots'],
    }
