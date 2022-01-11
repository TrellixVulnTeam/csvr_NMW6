# -*- coding: gb18030 -*-

"""
"""
import KBEngine
from KBEDebug import *

from Extra import ECBExtend
from Extra.EntityEvent import EntityEvent
from Extra.CellConfig import g_entityConfig
import GloballyDefine as GD
import Math
import math

class GameObject( KBEngine.Entity, ECBExtend.ECBExtend, EntityEvent  ):
	"""
	"""
	def __init__( self ):
		"""
		"""
		KBEngine.Entity.__init__( self )
		EntityEvent.__init__(self)

	def onSpaceGone( self ):
		"""
		space�ر�
		"""
		INFO_MSG( "GameObject %s has gone!" % ( self.eMetaClass ) )
		self.destroy()		
		
	def getName( self ):
		"""
		virtual method.
		@return: the name of entity
		@rtype:  STRING
		"""
		return ""

	def getConfig(self):
		return g_entityConfig.get(self.eMetaClass)

	def getCurrentSpaceBase( self ):
		"""
		ȡ��entity��ǰ���ڵ�space��space entity base
		@return: ����ҵ����򷵻���Ӧ��base���Ҳ����򷵻�None.
				�Ҳ�����ԭ��ͨ������Ϊspace����destoryed�У����Լ���û���յ�ת��֪ͨ��destroy.
		"""
		try:
			return KBEngine.cellAppData[GD.GLOBALDATAPREFIX_SPACE + str(self.spaceID)]
		except KeyError:
			return None

	def forward(self):
		return Math.Vector3(math.sin(self.direction.z),0, math.cos(self.direction.z))
	
	# -------------------------------------------------
	# flags about
	# -------------------------------------------------
	def setFlag( self, flag ):
		"""
		�������ñ�־

		@param flag: ENTITY_FLAG_* ���ƺ���ϵ�ֵ
		@type  flag: INT
		"""
		self.flags = flag

	def addFlag( self, flag ):
		"""
		�������ñ�־

		@param flag: ENTITY_FLAG_*
		@type  flag: INT
		"""
		self.flags |= 1 << flag

	def removeFlag( self, flag ):
		"""
		�������ñ�־

		@param flag: ENTITY_FLAG_*
		@type  flag: INT
		"""
		# ��32λ��ʹ�ã����Ǳ�־λ�����ʹ���������Ҫ��UINT32����ǰ�õ���INT32
		# ��ʹ��UINT32������һ��ԭ�������ǿ��ܲ�������ô���־��
		# ��һ��ԭ�������ʹ��UINT32��python��ʹ����INT64���������ֵ
		self.flags &= ~(1 << flag)

	def hasFlag( self, flag ):
		"""
		�ж�һ��entity�Ƿ���ָ���ı�־

		@param flag: ENTITY_FLAG_*
		@type  flag: INT
		@return: BOOL
		"""
		flag = 1 << flag
		return ( self.flags & flag ) == flag

	# -------------------------------------------------
	# mapping about
	# -------------------------------------------------
	def getMapping( self ):
		return self.persistentMapping

	def getTempMapping( self ):
		return self.tempMapping

	def mappingQuery( self, key, default = None ):
		"""
		���ݹؼ��ֲ�ѯmapping����֮��Ӧ��ֵ

		@return: ����ؼ��ֲ������򷵻�defaultֵ
		"""
		try:
			return self.persistentMapping[key]
		except KeyError:
			return default

	def mappingSet( self, key, value ):
		"""
		��һ��key��дһ��ֵ

		@param   key: �κ�PYTHONԭ����(����ʹ���ַ���)
		@param value: �κ�PYTHONԭ����(����ʹ�����ֻ��ַ���)
		"""
		self.persistentMapping[key] = value

	def mappingPop( self, key, default = None ):
		"""
		�Ƴ�������һ����key���Ӧ��ֵ
		"""
		return self.persistentMapping.pop( key, default )

	def mappingRemove( self, key ):
		"""
		�Ƴ�һ����key���Ӧ��ֵ
		"""
		self.persistentMapping.pop( key, None )

	def mappingAdd( self, key, value ):
		"""
		��һ��key���Ӧ��ֵ���һ��ֵ��
		ע�⣺�˷����������Դ��Ŀ���ֵ�Ƿ�ƥ�����ȷ
		"""
		v = self.mappingQuery( key, 0 )
		self.set( key, value + v )

	def tempMappingQuery( self, key, default = None ):
		"""
		���ݹؼ��ֲ�ѯ��ʱmapping����֮��Ӧ��ֵ

		@return: ����ؼ��ֲ������򷵻�defaultֵ
		"""
		try:
			return self.tempMapping[key]
		except KeyError:
			return default

	def tempMappingSet( self, key, value ):
		"""
		��һ��key��дһ��ֵ

		@param   key: �κ�PYTHONԭ����(����ʹ���ַ���)
		@param value: �κ�PYTHONԭ����(����ʹ�����ֻ��ַ���)
		"""
		self.tempMapping[key] = value

	def tempMappingPop( self, key, default = None ):
		"""
		�Ƴ�������һ����key���Ӧ��ֵ
		"""
		return self.tempMapping.pop( key, default )

	def tempMappingRemove( self, key ):
		"""
		�Ƴ�һ����key���Ӧ��ֵ
		"""
		self.tempMapping.pop( key, None )

	def tempMappingAdd( self, key, value ):
		"""
		��һ��key���Ӧ��ֵ���һ��ֵ��
		ע�⣺�˷����������Դ��Ŀ���ֵ�Ƿ�ƥ�����ȷ
		"""
		v = self.tempMappingQuery( key, 0 )
		self.setTemp( key, value + v )

	# ------------------------------------------------
	# think about
	# ------------------------------------------------
	def onThink( self ):
		"""
		virtual method.
		AI˼��
		"""
		pass

	def think( self, delay = 0.0 ):
		"""
		����������
		@param delay:	�ȴ��´δ���think��ʱ�䣬���delayΪ0����������
		@type  delay:	FLOAT
		"""
		if delay > 0.0:
			if self.thinkControlID < 0:	# ��thinkControlIDֵС��0ʱ��ʾ����think�����Ǵ�ֵ����С��0
				return
			t = KBEngine.time()
			if self.thinkControlID != 0:
				if self.thinkWaitTime - t <= delay:
					return	# ��ǰʣ��ʱ�����С���µĴ����ȴ�ʱ�䣬��ʹ�õ�ǰtimer��
				self.delTimer( self.thinkControlID )
			self.thinkWaitTime = t + delay
			self.thinkControlID = self.addTimer( delay, 0.0, ECBExtend.TIMER_ON_THINKING )
		else:
			# stop if we waiting think
			if self.thinkControlID > 0:
				self.delTimer( self.thinkControlID )
				self.thinkControlID = 0
			elif self.thinkControlID < 0:	# ��thinkControlIDֵС��0ʱ��ʾ����think�����Ǵ�ֵ����С��0
				return
			self.onThink()

	def pauseThink( self, stop = True ):
		"""
		��ֹ/����think��Ϊ��
		think��Ϊ����ֹ�Ժ�����ٴο������������ж�think�ĵ�����Ϊ���ᱻ���ԡ�
		"""
		if stop:
			if self.thinkControlID > 0:
				self.delTimer( self.thinkControlID )
			self.thinkControlID = -1
		else:
			self.thinkControlID = 0

	def onTimer_think( self, timerID, cbID ):
		"""
		ECBExtend timer callback.
		"""
		self.think( 0 )	
	
	def onRawTimer(self, timerID, cbID):
		"""
		�����޺����Ķ�ʱ��
		"""
		pass
	
	def navigate_( self, destination, velocity, distance, maxMoveDistance, maxSearchDistance, faceMovement, layer, userData ):
		"""
		����
		"""
		flags = KBEngine.getSpaceData(self.spaceID, GD.SPACEDATA_NAV_FLAGS)
		return KBEngine.Entity.navigate( self, destination, velocity, distance, maxMoveDistance, maxSearchDistance, faceMovement, layer, int(flags), userData )
	
	def navigatePathPoints_( self, destination, maxSearchDistance, layer ):
		"""
		����·����
		"""
		flags = KBEngine.getSpaceData(self.spaceID, GD.SPACEDATA_NAV_FLAGS)
		return KBEngine.Entity.navigatePathPoints( self, destination, maxSearchDistance, layer, int(flags) )
		
# ע��timer�Ȼص�����ӿ�
ECBExtend.register_entity_callback( ECBExtend.TIMER_ON_THINKING, GameObject.onTimer_think )


# GameObject.py
