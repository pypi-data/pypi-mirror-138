from pywinauto import Application
from ta_cch_axcess import logger


class CCHDialogNames:
	DASHBOARD = 'Dashboard'
	RETURN_MANAGER = 'Return Manager'
	DOCUMENTS = 'Documents'


class CchDialog:
	def __init__(self, cch_app, dialog_name):
		logger.info(f'getting CMS dialog title {dialog_name}')
		self.app = cch_app
		self.window = self.app.window(
			title_re=dialog_name, visible_only=False
		)
		while not self.window.exists():
			logger.info(f'waiting for {dialog_name}')
		logger.info(
			f'Connected {dialog_name} {self.window}'
		)
		super(CchDialog, self).__init__()
