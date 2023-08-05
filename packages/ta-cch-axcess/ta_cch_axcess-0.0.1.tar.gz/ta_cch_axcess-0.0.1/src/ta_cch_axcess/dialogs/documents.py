from .cch_dialog import CchDialog
from ta_cch_axcess import logger


class Documents(CchDialog):
	def __init__(self, cch_app):
		super(Documents, self).__init__(cch_app, 'Document')

	def open_document_search(self):
		self.window.set_focus()
		self.window.child_window(
			class_name="RichTextBox", auto_id="txtSearch"
		).click_input()
		self.window.child_window(
			class_name="RichTextBox", auto_id="txtSearch"
		).type_keys('^a{BACKSPACE}')
		self.window.child_window(
			class_name="RichTextBox", auto_id="txtSearch"
		).type_keys("Document")
		self.window.child_window(
			auto_id="imgSearch", class_name="image"
		).click_input()
		logger.info("Waiting for the search to complete...")
		self.window.child_window(
			auto_id="txtblockProgress", class_name='TextBlock', title="Search Completed."
		).wait("enabled", timeout=30, retry_interval=1)
		logger.info("Complete!")

	def get_files_by_client_id(self, client_id, folder_name):
		logger.info(f'Getting files of client id: {client_id}')		
		self.window.child_window(
			auto_id="txtClientFilter", class_name='TextBox'
		).click_input()
		self.window.child_window(
			auto_id="txtClientFilter", class_name='TextBox'
		).wait('ready', timeout=5)
		self.window.child_window(
			auto_id="txtClientFilter", class_name='TextBox'
		).type_keys(client_id+'{ENTER}')
		self.window.child_window(
			auto_id="txtClientFilter", class_name='TextBox'
		).type_keys('{DOWN}{ENTER}')

		self.window.child_window(
			auto_id="cmbRecordsPerPage"
		).wait('ready', timeout=15)
		self.window.child_window(
			auto_id="cmbRecordsPerPage"
		).select("2000")

		self.window.child_window(
			title="Incoming files", class_name='TabItem'
		).click_input()

		files_table = self.window.child_window(
			best_match="Records", class_name='ViewableRecordCollection'
		).wrapper_object()

		cells = files_table.descendants(
			title="CCH.Document.UI.DocumentCentral.UIClasses.PendingApprovalEntityInfo"
		)

		row_counter = 0
		found_row = False

		for cell in cells:
			childrens = cell.children(class_name='Cell')
			records = cell.children(class_name='ViewableRecordCollection')
			for children in childrens:
				if client_id in children.legacy_properties()['Name']:
					found_row = True
				if found_row and ('Files' in children.legacy_properties()['Name']):
					files_number = children.legacy_properties()['Name'].replace('Files', '').strip()
					logger.info(files_number)

			if found_row:
				break

			row_counter = row_counter + 1

		for record in records:
			if 'Records' in record.legacy_properties()['Name']:
				results = record.children(class_name='Record')
				for result in results:
					if 'FileSearchResultList' in result.legacy_properties()['Name']:
						datagrids = result.children(
							class_name='ViewableRecordCollection')
						for datagrid in datagrids:
							if 'Records' in datagrid.legacy_properties()['Name']:
								list_data = datagrid.children(
									class_name='Record')
								cell_to_click = list_data[0].children(
									class_name='Cell')

		self.window.child_window(
			title="CCH.Document.UI.DocumentCentral.UIClasses.PendingApprovalEntityInfo", class_name="Record", found_index=0
		).click_input()
		for x in range(row_counter):
			self.window.type_keys('{DOWN}')
		self.window.type_keys('{RIGHT}')
		keys_to_press = ''

		for x in range(int(files_number)-1):
			keys_to_press = keys_to_press + "{DOWN}"

		self.window.type_keys('{DOWN}')
		self.window.type_keys('{VK_SHIFT down}{VK_CONTROL down}')
		self.window.type_keys(keys_to_press)
		self.window.type_keys('{VK_SHIFT up}{VK_CONTROL up}')

		cell_to_click[0].right_click_input()

		self.window.child_window(
			auto_id="mnuDownloadExistingCopy"
		).wait('exists', timeout=15)
		self.window.child_window(
			auto_id="mnuDownloadExistingCopy"
		).click_input()
		self.window.child_window(
			title=folder_name
		).wait('exists', timeout=15)
		self.window.child_window(
			title=folder_name
		).click_input()
		self.window.child_window(
			auto_id="1"
		).click_input()


	def process_files_in_document(self, tax_year, client_id):
		logger.info(f'Proccesing files of client id: {client_id}')
		self.window.child_window(
			auto_id="btnProcessPendingFiles"
		).wait('ready', timeout=5)
		self.window.child_window(
			auto_id="btnProcessPendingFiles"
		).click_input()
		self.window.child_window(
			auto_id="btnBrowseFolder"
		).wait('exits', timeout=5)
		self.window.child_window(
			auto_id="btnBrowseFolder"
		).click_input()
		self.window.child_window(
			title=tax_year, class_name='TextBlock'
		).wait('exists', timeout=5)
		self.window.child_window(
			title=tax_year, class_name='TextBlock'
		).double_click_input()
		self.window.child_window(
			auto_id="cmbClass"
		).click_input()
		self.window.child_window(
			title='Tax', class_name='ListBoxItem', found_index=0
		).wait('exists', timeout=5)
		self.window.child_window(
			title='Tax', class_name='ListBoxItem', found_index=0
		).click_input()
		self.window.child_window(
			auto_id="cmbSubclass"
		).click_input()
		self.window.child_window(
			title='Support Documents (PBC)', class_name='ListBoxItem', found_index=0
		).wait('exists', timeout=5)
		self.window.child_window(
			title='Support Documents (PBC)', class_name='ListBoxItem', found_index=0
		).click_input()
		checkbox_all = self.window.child_window(
			auto_id='pfxChkBoxSelectAll', class_name='CheckBox'
		).wrapper_object()

		checkbox_all_state = checkbox_all.get_toggle_state()

		if checkbox_all_state == 0:
			self.window.child_window(
				auto_id='pfxChkBoxSelectAll', class_name='CheckBox'
			).toggle()

		self.window.child_window(
			auto_id='btnApplyToSelectedFiles'
		).click_input()
		self.window.child_window(
			auto_id='btnApprove'
		).wait('ready', timeout=5)
		self.window.child_window(
			auto_id='btnApprove'
		).click_input()
		self.window.child_window(
			title="Files are approved successfully."
		).wait('exists', timeout=15)
		self.window.child_window(
			auto_id='PART_ThirdButton'
		).click_input()
		self.window.child_window(
			auto_id='btnCancel'
			).click_input()
		self.window.child_window(
			auto_id='PART_SecondButton'
		).click_input()
