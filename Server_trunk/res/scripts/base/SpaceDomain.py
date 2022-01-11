# -*- coding: gb18030 -*-
#

"""
Space domain class
"""

import KBEngine
from KBEDebug import *

from Functor import Functor
import GloballyDefine as GD
from Extra.SpaceItem import SpaceItem
from interfaces.SpaceDomainBase import SpaceDomainBase

# ������
class SpaceDomain(SpaceDomainBase):
	"""
	ֻ����һ��space������ڵĿռ�����
	"""
	def __init__( self ):
		SpaceDomainBase.__init__(self)
		
		self.__spaceItem = None
		
		# ����õ�ͼ��Ҫ�ڷ���������ʱ�ͼ��أ���ô�ʹ���һ����ͼ����
		if self.config_.loadOnStart:
			self.createSpace()
	
	def onSpaceLoseCell( self, spaceEntityID ):
		"""
		define method.
		space entity ʧȥ��cell���ݺ��ͨ�棻
		��Ҫ����δ���п��ܴ��ڵĿɴ洢����������������̫��ʱ���ܻῼ����û����ҵ�ʱ��ֻ����base���ݣ���ʱ����Ҫ����ͨ�棻
		@param 	key: int; ����space��entity��entity id
		"""
		INFO_MSG("%s space %d lose cell."%( self.eMetaClass, spaceEntityID ))
		self.__spaceItem.onLoseCell()
		
	def onSpaceGetCell( self, spaceEntityID ):
		"""
		define method.
		ĳ��space��cell���ݴ�����ɻص����˻ص������ڱ�������space��onGetCell()������ʱ���á�
		���ǿ��ڴ˻ص���ִ��һЩ���飬��ѵȴ������space����Ҵ��ͽ���space�ȵȡ�
		@param 	key: int; ����space��entity��entity id
		"""
		INFO_MSG("%s space %d create cell Complete"%( self.eMetaClass, spaceEntityID ))
		self.__spaceItem.onGetCell()
		
	def onSpaceCloseNotify( self, spaceEntityID ):
		"""
		define method.
		�ռ�رգ�space entity����֪ͨ��
		@param 	key: int; ����space��entity��entity id
		"""
		INFO_MSG("%s space close : %d"%( self.eMetaClass, spaceEntityID ))
		self.__spaceItem = None

	def onEntityEnterSpace( self, spaceBaseMailbox, entityBaseMailbox ):
		"""
		��ҽ�����ĳ��space��֪ͨ������space domain��������������һЩ����
		"""
		pass

	def onEntityLeaveSpace( self, spaceBaseMailbox, entityBaseMailbox ):
		"""
		����뿪��ĳ��space��֪ͨ������space domain��������������һЩ����
		"""
		pass

	def teleportEntity( self, position, direction, baseMailbox, params ):
		"""
		define method.
		����һ��entity��ָ����space��
		@type position : VECTOR3, 
		@type direction : VECTOR3, 
		@param baseMailbox: entity ��base mailbox
		@type baseMailbox : MAILBOX, 
		@param params: һЩ���ڸ�entity����space�Ķ�������� (domain����)
		@type params : PY_DICT = None
		"""
		self.__spaceItem.enter( baseMailbox, position, direction )
			
	def teleportEntitys( self, position, direction, baseMailboxs, params ):
		"""
		define method.
		ͬʱ���Ͷ��entity��ָ����space�С��ṩ�˽ӿ���Ҫ�����ڷ���һЩ����������������жϺ�һ���Դ��ͣ��Ӷ��򻯴��롣
		@type position : VECTOR3, 
		@type direction : VECTOR3, 
		@param baseMailboxs: entity ��base array of mailbox
		@type baseMailboxs : ARRAY OF MAILBOX, 
		@param params: һЩ���ڸ�entity����space�Ķ�������� (domain����)
		@type params : PY_DICT = None
		"""
		for mb in baseMailboxs:
			self.__spaceItem.enter( baseMailbox, position, direction )
		
	def teleportEntityOnLogin( self, baseMailbox, defaultPos, defaultDir, prevSpace, prevPos, params ):
		"""
		define method.
		��������µ�¼��ʱ�򱻵��ã������������ָ����space�г��֣�һ�������Ϊ���������ߵĵ�ͼ����
		@param baseMailbox: entity ��base mailbox
		@param defaultPos: Vector3��Ĭ�ϵ���������
		@param defaultDir: Vector3��Ĭ�ϵ����߳���
		@param prevSpace: string����һ����ͼ�ı�ʶ
		@param prevPos: Vector3����һ����ͼ��λ��
		@param params: PY_DICT��һЩ���ڸ�entity����space�Ķ��������(domain����)
		"""
		self.__spaceItem.logon( baseMailbox, defaultPos, defaultDir )

	def createSpace( self ):
		"""
		virtual method.
		����һ��ָ����space
		"""
		if self.__spaceItem is not None:
			ERROR_MSG("space item instance is max count. %s" % ( self.eMetaClass ))
			return

		def _onCreateBase( base, spaceItem ):
			"""
			����base��ɻص�����
			"""
			INFO_MSG("space base created, create cell now.", self.eMetaClass)
			self.__spaceItem.createCell()

		self.__spaceItem = SpaceItem( "Space", self, self.eMetaClass, {} )
		self.__spaceItem.createBase( _onCreateBase )


