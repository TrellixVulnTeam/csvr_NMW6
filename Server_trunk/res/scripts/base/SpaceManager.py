# -*- coding: gb18030 -*-
#

"""
Space Manager class
"""

import KBEngine
from KBEDebug import *

import GloballyDefine as GD
import MapDataConfig

# ����������
class SpaceManager( KBEngine.Base ):
	"""
	����������
	������ͨ�ռ�͸���
	"""
	def __init__( self ):
		KBEngine.Base.__init__(self)
		
		# �����з�����(baseapp��cellapp)�㲥�Լ�
		#KBEngine.globalData["SpaceManager"] = self
		self.isInit = False
		self.initProgress = 0

	def init( self ):
		"""
		��ʼ�����еĵ�ͼ����
		@type	spaceDatas : dict
		@param	spaceDatas : from MapDataConfig import MapDataConfig
		"""
		if self.isInit:
			return
			
		datas = MapDataConfig.getAllDatas()
		relatedDatas = MapDataConfig.getAllRelatedDatas()

		for key in datas.keys():
			# ������ͼ����
			INFO_MSG( "creating space domain:", key )
			
			if datas[key].relatedID == 0:
				KBEngine.createBaseAnywhere(datas[key].domainType, {"eMetaClass" : key, "spaceType" : datas[key].spaceType})
			
		for key in relatedDatas.keys():	
			if len(relatedDatas[key]) == 0:
				continue
			
			id = relatedDatas[key][0]
			data = datas[id]
			KBEngine.createBaseAnywhere(data.domainType, {"eMetaClass" : key, "spaceType" : data.spaceType})
		
		self.initProgress = 1
		self.isInit = True
		

