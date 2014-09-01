"""
Returns a Speech-To-Text engine.

Currently, the supported implementations are the default Pocket Sphinx and
the Google Speech API

Arguments:
    engine_type - one of "sphinx" or "google"
    kwargs - keyword arguments passed to the constructor of the STT engine
"""
import logging
logger = logging.getLogger(__name__)

from jasperplugin import JasperPluginManagerSingleton as pluginmanager
from plugintypes import STTPlugin

def newSTTEngine(slug=None, fallback=True):
    stt_engine = None
    
    if slug:
        plugin = pluginmanager.getPluginBySlug(slug, category=STTPlugin.CATEGORY)
        if plugin:
            logger.info("Using '%s' as STT plugin", plugin.name)
            stt_engine = plugin.plugin_object
        if not fallback:
            logger.critical("STT Plugin '%s' not found.", plugin.name)
            raise RuntimeError("No STT Plugin found!")
        else:
            logger.warning("STT Plugin '%s' not found, using fallback...")

    if not stt_engine:
        available_plugins = pluginmanager.getPluginsOfCategory(STTPlugin.CATEGORY):
        if len(available_plugins) == 0:
            logger.critical("No STT Plugins found.")
            raise RuntimeError("No STT Plugins found.")
        else:
            plugin = available_plugins[0]
            logger.info("Using '%s' as STT plugin", plugin.name)
            stt_engine = plugin.plugin_object

    return stt_engine
