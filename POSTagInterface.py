import abc

class POSTag(object, metaclass = abc.ABCMeta):
	@abc.abstractmethod
	def getPOSTag(self, question):
		raise NotImplementedError('getPOSTag() method not implemented')
