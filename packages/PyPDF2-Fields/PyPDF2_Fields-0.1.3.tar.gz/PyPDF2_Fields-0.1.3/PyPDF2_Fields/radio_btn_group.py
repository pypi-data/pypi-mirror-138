class RadioBtnGroup:
	"""
	This class contains the names of the radio buttons that make a radio
	button group in a PDF file. It also contains the group's name, which should
	be the name of the field that corresponds to the group in the PDF file. The
	buttons' names can be accessed through an index between brackets or this
	class's iterator.
	"""

	def __init__(self, group_name, *btn_names):
		"""
		The constructor needs this group's name followed by the buttons'
		names. At least one button name must be provided.

		Args:
			group_name (str): the name of this radio button group. It should be
				the name of the field that corresponds to the group in the PDF
				file.
			*btn_names: the names of the buttons in this group, as strings. At
				least one must be provided.

		Raises:
			ValueError: if no button name is provided
		"""
		if len(btn_names) < 1:
			raise ValueError("At least one button name must be provided.")

		self._name = group_name
		self._btn_names = btn_names

	def __eq__(self, other):
		if not isinstance(other, self.__class__):
			return False

		return self._name == other._name\
			and self._btn_names == other._btn_names

	def __getitem__(self, index):
		try:
			return self._btn_names[index]

		except IndexError:
			raise IndexError("Radio button group " + self._name
				+ " does not have index " + str(index) + ".")

	def has_index(self, index):
		"""
		Determines whether this group has the given index. If it does not,
		using that number as an index will raise an IndexError.

		Args:
			index (int): an integer that could be an index of this radio
				button group

		Returns:
			bool: True if this group has the given index, False otherwise
		"""
		size = len(self)
		return -size <= index and index < size

	def index(self, btn_name):
		"""
		Indicates the index of the given button name in this radio button
		group. An exception is raised if the button name is not found.

		Args:
			btn_name (str): a radio button name in this group

		Returns:
			int: the index of the wanted button name

		Raises:
			ValueError: if btn_name is not found
		"""
		try:
			return self._btn_names.index(btn_name)

		except ValueError:
			# btn_name can unknowingly be set to None.
			raise ValueError("Radio button group " + self._name
				+ " does not have button " + str(btn_name) + ".")

	def __iter__(self):
		return iter(self._btn_names)

	def __len__(self):
		return len(self._btn_names)

	@property
	def name(self):
		"""
		str: the name of this radio button group
		"""
		return self._name

	def __repr__(self):
		return self.__class__.__name__ + "('"\
			+ self._name + "', " + str(self._btn_names)[1:]
