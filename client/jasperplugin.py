import imp
import logging
from distutils.spawn import find_executable
import ConfigParser as configparser
logger = logging.getLogger(__name__)

import plugintypes
from yapsy.PluginManager import PluginManager
from yapsy.PluginInfo import PluginInfo
from yapsy.FilteredPluginManager import FilteredPluginManager

# FIXME: These Two values should not be hardcoded
CURRENT_JASPERVERSION = (2,0,0)
NETWORK_AVAILABLE = True

class JasperPluginInfo(PluginInfo):

    def __init__(self, plugin_name, plugin_path):
        super(JasperPluginInfo, self).__init__(plugin_name, plugin_path)

    @property
    def priority(self):
        try:
            value = self.details.getinteger('Documentation','Priority')
        except (configparser.NoSectionError, configparser.NoOptionError):
            value = 0
        return value
        
    @property
    def depends_jasperversion(self):
        try:
            versionstr = self.details.get('Dependencies','JasperVersion')
        except (configparser.NoSectionError, configparser.NoOptionError):
            value = (2,0,0)
        else:
            value = tuple(int(n) for n in versionstr.split('.'))
        return value
    
    @property
    def depends_network(self):
        try:
            value = self.details.getboolean('Dependencies','Network')
        except (configparser.NoSectionError, configparser.NoOptionError):
            value = False
        return value
    
    @property
    def depends_executables(self):
        try:
            csvlst = self.details.get('Dependencies','Binaries')
        except (configparser.NoSectionError, configparser.NoOptionError):
            value = []
        else:
            value = [item.strip() for item in csvlst.split(',')]
        return value
    
    @property
    def depends_modules(self):
        try:
            csvlst = self.details.get('Dependencies','Modules')
        except (configparser.NoSectionError, configparser.NoOptionError):
            value = []
        else:
            value = [item.strip() for item in csvlst.split(',')]
        return value
    
    @property
    def depends_plugins(self):
        try:
            csvlst = self.details.get('Dependencies','Plugins')
        except (configparser.NoSectionError, configparser.NoOptionError):
            value = []
        else:
            value = [item.strip() for item in csvlst.split(',')]
        return value
    
    @property
    def is_available(self):
        # Check Jasperversion
        if self.depends_jasperversion > CURRENT_JASPERVERSION:
            needed_version_str = '.'.join(str(n) for n in self.depends_jasperversion)
            current_version_str = '.'.join(str(n) for n in CURRENT_JASPERVERSION)
            logger.info("Plugin '%s' rejected: Needs newer Jasper version (%s > %s)",self.name, needed_version_str, current_version_str)
            return False
        
        # Check Network
        if self.depends_network and not NETWORK_AVAILABLE:
            logger.info("Plugin '%s' rejected: Needs network connection", self.name)
            return False
        
        # Check executables
        for executable_name in self.depends_executables:
            if not find_executable(executable_name):
                logger.info("Plugin '%s' rejected: Needs executable '%s'", self.name, executable_name)
                return False
        
        # Check modules
        for module_name in self.depends_modules:
            try:
                imp.find_module(module_name)
            except ImportError:
                logger.info("Plugin '%s' rejected: Needs module '%s'", self.name, module_name)
                return False

        # Everything worked, this module is available
        return True

class JasperPluginManager(PluginManager):
    PLUGIN_INFO_EXT = 'jasperplugin'
    PLUGIN_DIRS = ["../plugins"]
    PLUGIN_CATS = {
                   plugintypes.SpeechHandlerPlugin.CATEGORY: plugintypes.SpeechHandlerPlugin,
                   plugintypes.EventHandlerPlugin.CATEGORY: plugintypes.EventHandlerPlugin,
                   plugintypes.TTSPlugin.CATEGORY: plugintypes.TTSPlugin,
                   plugintypes.STTPlugin.CATEGORY: plugintypes.STTPlugin
                  }

    def __init__(self):
        super(JasperPluginManager, self).__init__(categories_filter=self.PLUGIN_CATS, directories_list=self.PLUGIN_DIRS, plugin_info_ext=self.PLUGIN_INFO_EXT)
        locator = self.getPluginLocator()
        locator.setPluginInfoClass(JasperPluginInfo)
    
    def getPluginBySlug(self, slug, category="Default"):
        """
        Get the plugin correspoding to a given category and slug
        """
        for item in self.getPluginsOfCategory(category):
            if item.slug == slug:
                return item
        return None

    def getPluginsOfCategory(self, category_name):
        available_plugins = super(JasperPluginManager, self).getPluginsOfCategory(category_name)
        available_plugins.sort(key=attrgetter('slug'))                   # sort on secondary key
        available_plugins.sort(key=attrgetter('priority'), reverse=True) # now sort on primary key, descending
        return available_plugins

class JasperFilteredPluginManager(FilteredPluginManager):
    def isPluginOk(self, info):
        return info.is_available

# Singleton
PluginManagerSingleton = JasperFilteredPluginManager(JasperPluginManager())
PluginManagerSingleton.collectPlugins()

if __name__ == "__main__":
    for plugin in PluginManagerSingleton.getAllPlugins():
        print(plugin.name)
        print("  (%s)" % plugin.description)