# -*- coding: gb18030 -*-
#

"""
"""

import KBEngine
from KBEDebug import *

import KST

from interfaces.GameObject import GameObject
from SrvDef import eObjectType

class NPC( GameObject):
	"""
	����Ҷ��������
	"""
	def __init__(self):
		"""
		���캯����
		"""
		GameObject.__init__(self)
		self.objectType = eObjectType.ActNPC						

