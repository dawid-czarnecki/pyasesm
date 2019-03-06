__version__ = '1.0'
try:
	from .activelists import ActiveLists
except ImportError as e:
	logger.warning('Unable to load pyasesm properly: {}'.format(e))