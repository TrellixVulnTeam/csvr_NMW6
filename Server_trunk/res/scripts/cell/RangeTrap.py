# -*- coding: gb18030 -*-
#

"""
"""

import KBEngine
from KBEDebug import *

import KST
from interfaces.GameObject import GameObject
from SrvDef import eObjectType
from Extra.CellConfig import g_triggerEConfig
import GloballyConst as GC
import Math 
import math
import Vector
from Traps.TrapBase import TrapBase

class RangeTrap( GameObject ): 
	"""
	����Ҷ��������
	"""
	def __init__(self):
		"""
		���캯����
		"""
		self.objectType = eObjectType.RangeTrap	
		self.config = g_triggerEConfig[self.eMetaClass]
		self.trapEntity = []
		self.trap = TrapBase()

	def onEnterTrap( self, exposed, enterID ):
		if not self.openTrap:
			return
	
		enterEntity = KBEngine.entities[enterID]
		self.trap.enter(self, enterEntity)
	
	def onLeaveTrap( self, exposed, enterID ):
		
		if enterID not in self.trapEntity:
			return
		
		if not self.openTrap:
			return
		
		enterEntity = KBEngine.entities[enterID]
		self.trap.leave(self, enterEntity)
	
