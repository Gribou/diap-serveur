from django.contrib.staticfiles import finders
from .models import Profile, ProfileMapping, LayoutCell
from search.models import SearchApiEndpoint, SearchEngine
from nav.models import AppItem, TabletAppConfig


def save_icon(icon_name, conf):
    icon_path = finders.find("diapason_icons/{}".format(icon_name))
    if icon_path:
        with open(icon_path, 'r') as icon:
            conf.icon.save(icon_name, icon)
            conf.save()


def add_coconuts(profile, i):
    coconuts = AppItem.objects.create(
        title="Coconuts", external_url="/coconuts/")
    conf = TabletAppConfig.objects.create(
        parent_app=coconuts, color="#4caf50", textColor="#fff")
    save_icon("coconuts.svg", conf)
    LayoutCell.objects.create(
        profile=profile, element=conf.element, row=i // 3, col=i % 3)
    search = SearchEngine.objects.create(
        parent_app=conf, name="Coconuts", template_url="{root_url}search?search={search_query}")
    SearchApiEndpoint.objects.create(
        search_engine=search, api_type="DIAPASON", label="Aérodromes", template_url="{root_url}api/airfields/airfield/")
    SearchApiEndpoint.objects.create(
        search_engine=search, api_type="DIAPASON", label="Secteurs", template_url="{root_url}api/acc/sector/?")
    SearchApiEndpoint.objects.create(
        search_engine=search, api_type="DIAPASON", label="Annuaire", template_url="{root_url}api/phones/phone/}")
    SearchApiEndpoint.objects.create(
        search_engine=search, api_type="DIAPASON", label="Moyen radionav", template_url="{root_url}api/radionav/station/")
    SearchApiEndpoint.objects.create(
        search_engine=search, api_type="DIAPASON", label="Autres cartes", template_url="{root_url}api/files/file/")
    SearchApiEndpoint.objects.create(
        search_engine=search, api_type="DIAPASON", label="Cartes AIP", template_url="{root_url}api/airfields/map/")
    profile.search_engines.add(search)


def add_perfos(profile, i):
    perfos = AppItem.objects.create(
        title="Perfos", external_url="/perfos/")
    conf = TabletAppConfig.objects.create(
        parent_app=perfos, color="#272727", textColor="#fff")
    save_icon("perfos.svg", conf)
    LayoutCell.objects.create(
        profile=profile, element=conf.element, row=i // 3, col=i % 3)
    search = SearchEngine.objects.create(
        parent_app=conf, name="Perfos", template_url="{root_url}results?search={search_query}")
    SearchApiEndpoint.objects.create(
        search_engine=search, api_type="DIAPASON", label="Types d'aéronefs", template_url="{root_url}api/aircrafts/")
    profile.search_engines.add(search)


def add_efne(profile, i):
    efne = AppItem.objects.create(
        title="eFNE", internal_url="/efne/")
    conf = TabletAppConfig.objects.create(
        parent_app=efne, color="#00bcd4", textColor="#fff")
    save_icon("efne.svg", conf)
    LayoutCell.objects.create(
        profile=profile, element=conf.element, row=i // 3, col=i % 3)


def add_enews(profile, i):
    enews = AppItem.objects.create(
        title="eNews", external_url="/enews/")
    conf = TabletAppConfig.objects.create(
        parent_app=enews, color="#3f51b5", textColor="#fff")
    save_icon("enews.svg", conf)
    LayoutCell.objects.create(
        profile=profile, element=conf.element, row=i // 3, col=i % 3)
    search = SearchEngine.objects.create(
        parent_app=conf, name="eNews", template_url="{root_url}docs?search={search_query}")
    SearchApiEndpoint.objects.create(
        search_engine=search, api_type="DIAPASON", label="Publications", template_url="{root_url}api/doc/")
    profile.search_engines.add(search)


def add_meteo(profile, i):
    meteo = AppItem.objects.create(
        title="Météo France", external_url="https://pro.meteofrance.com")
    conf = TabletAppConfig.objects.create(
        parent_app=meteo, color="#005891", textColor="#fff")
    save_icon("meteo.svg", conf)
    LayoutCell.objects.create(
        profile=profile, element=conf.element, row=i // 3, col=i % 3)


def populate():
    if not Profile.objects.exists():
        p = Profile.objects.create(
            title="Démo", url="demo", dark_theme=True, show_search_field=True, show_photo_button=True,)
        add_efne(p, 0)
        add_enews(p, 1)
        add_coconuts(p, 2)
        add_perfos(p, 3)
        add_meteo(p, 4)

        if not ProfileMapping.objects.filter(ip_address="*").exists():
            ProfileMapping.objects.create(
                ip_address="*", profile=p)
