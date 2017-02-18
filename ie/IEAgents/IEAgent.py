import abc

class IEAgent(object):
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def refresh(self):
		"""refresh the database"""
		return


if __name__ == "__main__":
	raise NotImplementedError
