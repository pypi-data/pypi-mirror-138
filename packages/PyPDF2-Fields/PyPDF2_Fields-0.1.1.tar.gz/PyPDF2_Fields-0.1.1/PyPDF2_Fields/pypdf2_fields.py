from PyPDF2 import PdfFileWriter
from PyPDF2.generic import BooleanObject,\
	IndirectObject, NameObject, TextStringObject

from .field_types import\
	PdfFieldType,\
	get_field_type


_KEY_ACROFORM = "/AcroForm"
_KEY_ANNOTS = "/Annots"
_KEY_AS = "/AS"
_KEY_KIDS = "/Kids"
_KEY_NEED_APPEARANCES = "/NeedAppearances"
_KEY_PARENT = "/Parent"
_KEY_T = "/T"
_KEY_V = "/V"


def _make_radio_btn_group_dict(radio_btn_groups):
	"""
	Creates a dictionary that associates each given radio button group with
	its name. The name is a property of class RadioBtnGroup.

	Args:
		radio_btn_groups: a list, set or tuple that contains instances of
			RadioBtnGroup

	Returns:
		dict: Its keys are the groups' names; its values are the groups.
	"""
	btn_groups = dict()

	for group in radio_btn_groups:
		btn_groups[group.name] = group

	return btn_groups


def make_writer_from_reader(pdf_reader, editable):
	"""
	Creates a PdfFileWriter instance from the content of a PdfFileReader
	instance. Depending on parameter editable, it will be possible to modify
	the fields of the file produced by the returned writer.

	Args:
		pdf_reader (PdfFileReader): an instance of PdfFileReader
		editable (bool): If True, the fields in the file created by the
			returned writer can be modified.

	Returns:
		PdfFileWriter: an instance that contains the pages of pdf_reader
	"""
	pdf_writer = PdfFileWriter()

	if editable:
		for page in pdf_reader.pages:
			pdf_writer.addPage(page)

	else:
		pdf_writer.cloneDocumentFromReader(pdf_reader)

	return pdf_writer


def pair_fields_name_and_val(pdf_fields, filter_none):
	"""
	Creates a dictionary that maps the name of a PDF file's fields to their
	value.

	Args:
		pdf_fields (dict): It maps the name of the file's fields to an object
			of type PyPDF2.generic.Field. It is obtained through
			PdfFileReader's method getFields.
		filter_none (bool): If this argument is True, None values are excluded
			from the returned dictionary.

	Returns:
		dict: It maps the fields' name to their value.
	"""
	name_val_dict = dict()

	for mapping_name, field in pdf_fields.items():
		field_val = field.value

		if not filter_none or field_val is not None:
			name_val_dict[mapping_name] = field_val

	return name_val_dict


def set_need_appearances(pdf_writer, bool_val):
	"""
	Sets property _root_object["/AcroForm"]["/NeedAppearances"] of the given
	PdfFileWriter instance to a Boolean value. Setting it to True can be
	necessary to make the text fields' content visible in the file produced
	by pdf_writer.

	Args:
		bool_val (bool): the Boolean value to which /NeedAppearances will be
			set
	"""
	# https://stackoverflow.com/questions/47288578/pdf-form-filled-with-pypdf2-does-not-show-in-print
	catalog = pdf_writer._root_object

	# Get the AcroForm tree and add /NeedAppearances attribute
	if _KEY_ACROFORM not in catalog:
		pdf_writer._root_object.update({NameObject(_KEY_ACROFORM):
			IndirectObject(len(pdf_writer._objects), 0, pdf_writer)})

	need_appearances = NameObject(_KEY_NEED_APPEARANCES)
	pdf_writer._root_object[_KEY_ACROFORM][need_appearances]\
		= BooleanObject(bool_val)


def update_page_fields(page, field_content, *radio_btn_groups):
	"""
	Sets the fields in the given PdfFileWriter page to the values contained in
	argument field_content. Every key in this dictionary must be the name of a
	field in page. Text fields can be set to any object, which will be
	converted to a string. Checkboxes must be set to a string that represents
	their checked or unchecked state. For a radio button group, the value must
	be the index of the selected button. The index must correspond to a button
	name contained in the RadioBtnGroup instance in argument *radio_btn_groups
	that bears the group's name. This function ignores fields of type action
	button.

	Args:
		page (PyPDF2.pdf.PageObject): a page from a PdfFileWriter instance
		field_content (dict): Its keys are field names; its values are the data
			to put in the fields.
		*radio_btn_groups: RadioBtnGroup instances that represent the radio
			button groups in page. This argument is optional if no radio button
			group is being set.

	Raises:
		IndexError: if argument field_content sets a radio button group to an
			incorrect index
	"""
	# This function is based on PdfFileWriter.updatePageFormFieldValues and an answer to this question:
	# https://stackoverflow.com/questions/35538851/how-to-check-uncheck-checkboxes-in-a-pdf-with-python-preferably-pypdf2
	if len(radio_btn_groups) > 0:
		radio_buttons = True
		btn_group_dict = _make_radio_btn_group_dict(radio_btn_groups)

	else:
		radio_buttons = False

	page_annots = page[_KEY_ANNOTS]

	for writer_annot in page_annots:
		writer_annot = writer_annot.getObject()
		annot_name = writer_annot.get(_KEY_T)
		field_type = get_field_type(writer_annot)

		# Set text fields and checkboxes
		if annot_name in field_content:
			field_value = field_content[annot_name]

			if field_type == PdfFieldType.TEXT_FIELD:
				writer_annot.update({
					NameObject(_KEY_V): TextStringObject(field_value)
				})

			elif field_type == PdfFieldType.CHECKBOX:
				writer_annot.update({
					NameObject(_KEY_AS): NameObject(field_value),
					NameObject(_KEY_V): NameObject(field_value)
				})

		# Set radio buttons
		elif radio_buttons and annot_name is None:
			annot_parent = writer_annot.get(_KEY_PARENT).getObject()

			if annot_parent is not None:
				annot_parent_name = annot_parent.get(_KEY_T).getObject()
				annot_parent_type = get_field_type(annot_parent)

				if annot_parent_name in field_content\
						and annot_parent_type == PdfFieldType.RADIO_BTN_GROUP:
					button_index = field_content[annot_parent_name]
					button_group = btn_group_dict.get(annot_parent_name)

					if button_group is not None:
						# This instruction can raise an IndexError.
						button_name = button_group[button_index]

						# This function needs the RadioBtnGroup instances
						# because the index of the selected button is
						# required here.
						annot_parent[NameObject(_KEY_KIDS)].getObject()\
							[button_index].getObject()[NameObject(_KEY_AS)]\
							= NameObject(button_name)

						annot_parent[NameObject(_KEY_V)]\
							= NameObject(button_name)
