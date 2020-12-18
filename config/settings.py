import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'handlers': {
		'file': {
			'level': 'WARNING',
			'class': 'logging.FileHandler',
			'filename': '/Users/khabarovatatiana/Desktop/botnos/bot1520log.log',
		},
	},
	'loggers': {
		'botnos': {
			'handlers': ['file'],
			'level': 'WARNING',
			'propagate': True,
		},
	},
}
