#-*- coding: Cp1251 -*-
#################################################################
# Program: Toolib
"""
AbstractConfigurable is an abstract superclass that provides configuration
functionality for subclasses, but have abstract _saveConfig and _loadConfig methods

FileConfigurable is file config implementation
RegistryConfigurable is registry config implementation
Configurable uses Registry on win32 and File on other oses

Subclasses should override:

	* getDefaultConfig()  to return a dictionary of default settings
					   such as { 'Frequency': 5 }

	* getDefaultUserConfig()  to return a dictionary of default settings

	* getCore()			to return core object with methods
							getDomain()        for both
							getProjectPath()   for FileConfigurable

OR getCore() is not required if overrided

	* getDomain()			to return domain, i.e. 'Rata' or 'Sula', for both
	* getProjectPath()		(windows only) to return project root path, for FileConfigurable

Subclasses typically use the getSetting() method, for example:

	time.sleep(self.getSetting('Frequency'))

They might also use the printConfig() method, for example:

	self.printConfig()		# or
	self.printConfig(file)

They might also use the printConfig() method, for example:

	self.saveLocalConfig()
	self.saveUserConfig()
	self.saveConfig()		# to save both

Users of your software can create a file with the same name as
configFilename() and selectively override settings. The format of
the file is a Python dictionary.

Subclasses can also override _loadConfig() and _saveConfig() in order to use
configuration settings from another source.

TODO:
	FileConfigurable.saveConfig should return value, not raise errors
"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2013/03/29 12:55:50 $"
__version__ = "$Revision: 1.12 $"
# $Source: D:/HOME/cvs/toolib/util/Configurable.py,v $
#
#################################################################

import os
import sys
import types

from toolib.event.Event		import Event
from ForkDict				import ForkDict
from toolib					import debug

NotAssigned = NotImplemented

__all__ = [
	'ConfigurationError',
	'Configurable',
	'FileConfigurable',
	# RegistryConfigurable will be added only on win32
]


def getUserProfilePath():
	"""
	returns place to store user dependent configs
	NOTE: not tested on unix
	"""
	if os.name == 'nt':
		# try USERPROFILE
		return os.environ.get('USERPROFILE')
	elif os.name in ('posix', 'unix'):
		return os.environ.get('HOME')
	else:
		raise NotImplementedError, 'OS: ' + os.name


class ConfigurationError(Exception):
	pass


class AbstractConfigurable(object):

	def invalidateConfig(self):
		self._config = None

	def getConfig(self):
		""" Returns the configuration of the object as a dictionary.
		This is a combination of getDefaultConfig() and loadConfig().
		This method caches the config. """
		if not hasattr(self, '_config') or self._config is None:
			localConfig = {}
			localConfig.update(self.getDefaultLocalConfig())
			
			#rint "Default Local conf:", localConfig
			#rint "Stored  Local conf:", self.loadLocalConfig()

			localConfig.update(self.loadLocalConfig())

			userConfig = {}
			userConfig.update(self.getDefaultUserConfig())
			userConfig.update(self.loadUserConfig())
##			userConfig.update(self.commandLineConfig())

			#rint "Default User conf:", userConfig
			#rint "Stored  User conf:", self.loadUserConfig()

			self._config = ForkDict([userConfig, localConfig])
		return self._config

	def getLocalConfig(self):
		return self.getConfig().dictAt(1)

	def getUserConfig(self):
		return self.getConfig().dictAt(0)

	def getSetting(self, name, default=NotAssigned):
		"""
		Returns the value of a particular setting in the configuration.
		Looks in user config first, than in local config
		"""
		if default is NotAssigned:
			return self.getConfig()[name]
		else:
			return self.getConfig().get(name, default)

	def setSetting(self, name, value):
		oldValue = self.getConfig().get(name, NotImplemented)
		if oldValue != value:
			self.getConfig()[name] = value
			self._fireConfigValueChanged(key=name, oldValue=oldValue, newValue=value)

	def hasSetting(self, name):
		return self.getConfig().has_key(name)

	def getDefaultLocalConfig(self):
		"""
		local mashine defaults
		Returns a dictionary containing all the default values for the settings.
		This implementation returns {}.
		Subclasses should override.
		"""
		return {}

	def getDefaultUserConfig(self):
		"""
		User specific defaults
		Returns a dictionary containing all the default values for the settings.
		This implementation returns {}.
		Subclasses should override. """
		return {}

	def getOrganization(self):
		try:
			from toolib.config.const import ORGANIZATION
			return ORGANIZATION
		except ImportError:
			debug.warning("ORGANIZATION expected in toolib.config.const")
			return "Unknown Organization"

	def getDomain(self):
		return self.getCore().getDomain()

	def getConfigName(self):
		"""
		Returns the name of the configuration file.
		This is used on the command-line.
		"""
		return self.__class__.__name__

	def printConfig(self, dest=None):
		""" Prints the configuration to the given destination, which defaults to stdout. A fixed with font is assumed for aligning the values to start at the same column. """
		if dest is None:
			dest = sys.stdout
		keys = self.getConfig().keys()
		keys.sort()
		width = max(map(lambda key: len(key), keys))
		for key in keys:
			dest.write("%s = %s\n" % (key.ljust(width), self.getSetting(key)))
		dest.write('\n')

##  def commandLineConfig(self):
##		"""
##		Settings that came from the command line (via
##		addCommandLineSetting).
##		"""
##		return _settings.get(self.getConfigName(), {})

	def getLocalConfigPath(self):
		raise NotImplementedError

	def getUserConfigPath(self):
		raise NotImplementedError

	def _loadConfig(self, path):
		raise NotImplementedError

	def loadLocalConfig(self):
		""" Returns the default local mashine config overrides  """
		return self._loadConfig(self.getLocalConfigPath())

	def loadUserConfig(self):
		""" Returns the default user config overrides """
		return self._loadConfig(self.getUserConfigPath())

	def _saveConfig(self, conf, defaults, path):
		raise NotImplementedError, 'abstract'

	def saveLocalConfig(self):
		return self._saveConfig(self.getLocalConfig(), self.getDefaultLocalConfig(), self.getLocalConfigPath())

	def saveUserConfig(self):
		return self._saveConfig(self.getUserConfig(), self.getDefaultUserConfig(), self.getUserConfigPath())

	def saveConfig(self):
		a = self.saveLocalConfig()
		b = self.saveUserConfig()
		return a and b

	def addConfigListener(self, l):
		if not hasattr(self, "_AbstractConfigurable__listeners"):
			self.__listeners = []
		self.__listeners.append(l)
		
	def removeConfigListener(self, l):
		if hasattr(self, "_AbstractConfigurable__listeners"):
			self.__listeners.remove(l)

	def _fireConfigValueChanged(self, **args):
		if not hasattr(self, "_AbstractConfigurable__event"):
			self.__event = Event(self, "configValueChanged")
		self.__event._init(**args)
		self.__event._send(getattr(self, '_AbstractConfigurable__listeners', None))

		
class FileConfigurable(AbstractConfigurable):

	def getProjectPath(self):
		return self.getCore().getProjectPath()

	def getLocalConfigPath(self):
		# project/conf/configName.conf
		if os.name == 'nt':
			return os.path.join(self.getProjectPath(), 'conf', self.getConfigFileName())
		else:
			return os.path.join('/etc', self.getDomain())

	def getUserConfigPath(self):
		# ~/.domain/configName.conf
		return os.path.join(getUserProfilePath(), '.' + self.getDomain(), self.getConfigFileName())

	def getConfigFileName(self):
		""" Returns the filename by which users can override the configuration. Subclasses must override to specify a name. Returning None is valid, in which case no user config file will be loaded. """
		return self.getConfigName() + ".conf.py"

	def _loadConfig(self, path):
		""" Returns the user config overrides found in the optional config file, or {} if there is no such file. The config filename is taken from configFilename(). """
		try:
			file = open(path)
		except IOError:
			return {}
		else:
			contents = file.read()
			file.close()
			try:
				config = eval(contents, {})
			except:
				raise ConfigurationError, 'Invalid configuration file, %s.' % path
			if type(config) is not types.DictType:
				raise ConfigurationError, 'Invalid type of configuration. Expecting dictionary, but got %s.'  % type(config)
			return config

	def saveUserConfig(self):
		userConfPath = self.getUserConfigPath()
		if userConfPath:
			return self._saveConfig(self.getUserConfig(), self.getDefaultUserConfig(), userConfPath)
		else:
			raise ConfigurationError, "No place to save user configs"

	def _saveConfig(self, conf, defaults, path):
		""" Returns the user config overrides found in the optional config file, or {} if there is no such file. The config filename is taken from configFilename(). """
		if conf != defaults:
			try:
				d = os.path.split(path)[0]
				if d and not os.path.exists(d):
					os.makedirs(d)
			except OSError, e:
				raise ConfigurationError, "Can't save config. OsError: %s" % (e,)

			try:
				file = open(path, 'wt')

				keys = conf.keys()
				keys.sort()

				file.write('{\n')
				for key in keys:
					value = conf[key]
					if value is not None and value != defaults.get(key, NotAssigned):
						file.write('\t%-16s: %s,\t# default is %s\n' % (repr(key), repr(value), repr(defaults.get(key, NotAssigned))))
				file.write('}\n')
				file.close()
			except IOError, e:
				raise ConfigurationError, "Can't save config. IOError: %s" % (e,)

## TODO: Deal with it
##_settings = {}
##def addCommandLineSetting(name, value):
##  """
##  Take a setting, like --AppServer.Verbose=0, and call
##  addCommandLineSetting('AppServer.Verbose', '0'), and
##  it will override any settings in AppServer.config
##  """
##  configName, settingName = name.split('.', 1)
##  value = valueForString(value)
##  if not _settings.has_key(configName):
##		_settings[configName] = {}
##  _settings[configName][settingName] = value
##
##def commandLineSetting(configName, settingName, default=NotAssigned):
##  """
##  Retrieve a command-line setting.  You can use this with
##  non-existent classes, like --Context.Root=/WK, and then
##  fetch it back with commandLineSetting('Context', 'Root').
##  """
##  if default is NotAssigned:
##		return _settings[configName][settingName]
##  else:
##		return _settings.get(configName, {}).get(settingName, default)

try:
	import win32api
	import toolib.win32.registry as registry

	class RegistryConfigurable(AbstractConfigurable):

		def getLocalConfigPath(self):
			return "\\".join(("HKEY_LOCAL_MACHINE\\Software", self.getOrganization(), self.getDomain(), self.getConfigName()))

		def getUserConfigPath(self):
			return "\\".join(("HKEY_CURRENT_USER\\Software", self.getOrganization(), self.getDomain(), self.getConfigName()))

		def _loadConfig(self, path):
			conf = {}
			try:
				key = registry.RegKey(None, path)
			except win32api.error, e:
				if e[0] == registry.KEY_ACCESS_DENIED: # access denied
					pass
			except KeyError:
				pass
			else:
				for value in key.iterValues():
					conf[value.getName()] = value.getValue()
			return conf

		def _saveConfig(self, conf, defaults, path):
			try:
				key = registry.RegKey(path=path, create=1)
				for name in conf.keys():
					value = conf[name]
					defvalue = defaults.get(name, NotAssigned)
					if value is not None and value != defvalue:
						key.value(name).setValueIfChanged(value)
						assert debug.trace("set %s = %s" % (name, repr(value)))
					else:
						assert debug.trace("remove %s" % (name,))
						key.value(name).remove()	# no error if not exist
				return True
			except win32api.error, e:
				if e[0] == registry.KEY_ACCESS_DENIED: # access denied
					debug.error('Access denied to modify registry: %s' % path)
					return False
				else:
					raise


	__all__.append('RegistryConfigurable')

	Configurable = RegistryConfigurable
except ImportError:
	Configurable = FileConfigurable

if __name__ == '__main__':

	class TestObject(RegistryConfigurable):

		def getDefaultLocalConfig(self):
			return {
				#'userSetting_1' : "d11",
				#'userSetting_2' : "d22",
				#'userSetting_3' : 333,
				u'настройка'   : u'юзердефолт',
			}

		def getDefaultUserConfig(self):
			return {
				#'localSetting_1'	: "u11",
				#'localSetting_2'	: "u22",
				#'localSetting_3'	: 33333,
				u'настройка'      : u'локалдефолт',
			}

		def getDomain(self):
			return "testConfigurable"

		def getProjectPath(self):
			return "z:\\rata"

	from toolib.startup import hookStd
	hookStd()

	to = TestObject()

	for k, v in to.getConfig().iteritems():
		print k, v
		
	to.setSetting(u'настройка', u'шопоставим2')	

	for k, v in to.getConfig().iteritems():
		print k, v

	to.saveConfig()


