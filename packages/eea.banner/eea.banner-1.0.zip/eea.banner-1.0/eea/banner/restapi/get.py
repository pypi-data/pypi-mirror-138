"""RestAPI enpoint @banner GET"""
import json
from contextlib import closing
from six.moves import urllib
from plone import api
from plone.restapi.services import Service
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

# from eea.cache import cache
from eea.banner.interfaces import IBannerSettings, IEeaBannerLayer

TIMEOUT = 15
RANCHER_METADATA = "http://rancher-metadata/latest"
MEMCACHE_AGE = 300


@implementer(IPublishTraverse)
class BannerGet(Service):
    """Banner GET"""

    def get_rancher_metadata(self, url):
        """Returns Rancher metadata API"""
        try:
            req = urllib.request.Request(
                url, headers={"Accept": "application/json"})
            with closing(urllib.request.urlopen(req, timeout=TIMEOUT)) as conn:
                result = json.loads(conn.read())
        except Exception:
            result = []
        return result

    def get_stacks(self):
        """Returns all Rancher stacks from the current environment"""
        url = "%s/stacks" % RANCHER_METADATA
        return self.get_rancher_metadata(url)

    # @cache(lambda *args: "rancher-status", lifetime=MEMCACHE_AGE)
    def get_stacks_status(self, stacks):
        """Returns status of required stacks"""
        status = None
        rancher_stacks = self.get_stacks()
        for stack in rancher_stacks:
            if stack.get("system") or stack.get("name") not in stacks:
                continue
            services = stack.get("services", [])
            if not services:
                continue
            for service in services:
                if not status and service.get("state") != "active":
                    status = service.get("state")
                    break
        return status

    def reply(self):
        """Reply"""
        development = self.request.form.get("development")
        if not IEeaBannerLayer.providedBy(self.request):
            return {
                "static_banner": {"enabled": False},
                "dynamic_banner": {"enabled": False},
            }
        return {
            "static_banner": {
                "enabled": api.portal.get_registry_record(
                    "static_banner_enabled",
                    interface=IBannerSettings,
                    default=False,
                ),
                "visible_to_all": api.portal.get_registry_record(
                    "static_banner_visible_to_all",
                    interface=IBannerSettings,
                    default="",
                ),
                "type": api.portal.get_registry_record(
                    "static_banner_type", interface=IBannerSettings, default=""
                ),
                "title": api.portal.get_registry_record(
                    "static_banner_title",
                    interface=IBannerSettings,
                    default="",
                ),
                "message": api.portal.get_registry_record(
                    "static_banner_message",
                    interface=IBannerSettings,
                    default="",
                ),
            },
            "dynamic_banner": {
                "enabled": api.portal.get_registry_record(
                    "dynamic_banner_enabled",
                    interface=IBannerSettings,
                    default="",
                ),
                "visible_to_all": api.portal.get_registry_record(
                    "dynamic_banner_visible_to_all",
                    interface=IBannerSettings,
                    default="",
                ),
                "title": api.portal.get_registry_record(
                    "dynamic_banner_title",
                    interface=IBannerSettings,
                    default="",
                ),
                "message": api.portal.get_registry_record(
                    "dynamic_banner_message",
                    interface=IBannerSettings,
                    default="",
                ),
                "rancher_stacks_status": None
                if development
                else self.get_stacks_status(
                    api.portal.get_registry_record(
                        "rancher_stacks", interface=IBannerSettings, default=""
                    )
                ),
            },
        }
