# -*- coding: gb18030 -*-
#

"""
Space domain class
"""

import KBEngine
from KBEDebug import *

from Functor import Functor
from Extra.SpaceItem import SpaceItem
from interfaces.SpaceDomainBase import SpaceDomainBase
from SrvDef import eSpaceLoginAction
from MapConfigMgr import g_mapConfigMgr

class SpaceDomainSinglePlayer(SpaceDomainBase):
	"""
	���˵��ߵ�ͼ�Ŀռ�����
	"""
	def __init__( self ):
		SpaceDomainBase.__init__(self)
		
		# ����ҵ�dbid��ӳ��SpaceItemʵ��������߸���ͬһ�����Ľ����ж��ٶȣ�
		# ��ҵ�dbidҲ��ʶ����֮���Ӧ��SpaceItemʵ����ӵ���ߣ�
		# ʹ����ҵ�dbid����ʹ��entityID��ԭ����Ϊ�˷�ֹ����£��ϣ��ߺ�����ʱ�Ҳ���ԭ��������space��
		# Ҳ��Ϊ�˷�ֹ������£��ϣ��ߵķ�ʽ�ƹ�������ʱ���ڿɽ���Ĵ���
		# �˱���self.spaceItems_��Ӧ�������self.spaceItems_ɾ��һ�ҲӦ��������ɾ����������Ȼ
		
		# key = player's dbid, value = instance of SpaceItem
		self._dbid2spaceItem = {}
		
		# key = space entity id, value = player's dbid
		self._spaceID2dbid = {}

	def onSpaceLoseCell( self, spaceEntityID ):
		"""
		define method.
		space entity ʧȥ��cell���ݺ��ͨ�棻
		��Ҫ����δ���п��ܴ��ڵĿɴ洢����������������̫��ʱ���ܻῼ����û����ҵ�ʱ��ֻ����base���ݣ���ʱ����Ҫ����ͨ�棻
		@param 	key: int; ����space��entity��entity id
		"""
		INFO_MSG("%s space %d lose cell."%( self.eMetaClass, spaceEntityID ))
		playerDBID = self._spaceID2dbid[spaceEntityID]
		spaceItem = self._dbid2spaceItem[playerDBID]
		spaceItem.onLoseCell()
		
	def onSpaceGetCell( self, spaceEntityID ):
		"""
		define method.
		ĳ��space��cell���ݴ�����ɻص����˻ص������ڱ�������space��onGetCell()������ʱ���á�
		���ǿ��ڴ˻ص���ִ��һЩ���飬��ѵȴ������space����Ҵ��ͽ���space�ȵȡ�
		@param 	key: int; ����space��entity��entity id
		"""
		INFO_MSG("%s space %d create cell Complete"%( self.eMetaClass, spaceEntityID ))
		playerDBID = self._spaceID2dbid[spaceEntityID]
		spaceItem = self._dbid2spaceItem[playerDBID]
		spaceItem.onGetCell()
		
	def onSpaceCloseNotify( self, spaceEntityID ):
		"""
		define method.
		�ռ�رգ�space entity����֪ͨ��
		@param 	key: int; ����space��entity��entity id
		"""
		INFO_MSG("%s space close : %d"%( self.eMetaClass, spaceEntityID ))
		dbid = self._spaceID2dbid.pop( spaceEntityID )
		self._dbid2spaceItem.pop( dbid )

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
		spaceItem = self.findSpaceItem( params["dbID"], True )
		spaceItem.enter( baseMailbox, position, direction )
			
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
		pass  # ���˸���û�ж��˴��͹���
		
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
		DEBUG_MSG( "entity id: %s, prev space: '%s', prev pos: '%s', params: '%s'" % (baseMailbox.id, prevSpace, prevPos, params) )
		loginAct = self.config_.loginAction
		if loginAct == eSpaceLoginAction.Locale:                 # ԭ�����ߣ��������򴴽�
			spaceItem = self.findSpaceItem( params.get("dbID", 0), True )
			spaceItem.logon( baseMailbox, defaultPos, defaultDir )
		elif loginAct == eSpaceLoginAction.LocaleIfExisted:      # ������ԭ�����ߣ��������򷵻ص���һ��ͼ�������ͼʱ�ĵ�ͼ��
			spaceItem = self.findSpaceItem( params.get("dbID", 0), False )
			if spaceItem:
				spaceItem.logon( baseMailbox, defaultPos, defaultDir )
			else:
				self.gotoPrevSpace_(baseMailbox, prevSpace, prevPos, defaultDir, params)
		elif loginAct == eSpaceLoginAction.GotoPrev:             # ǿ�Ʒ��ص���һ��ͼ�������ͼʱ�ĵ�ͼ��
			self.gotoPrevSpace_(baseMailbox, prevSpace, prevPos, defaultDir, params)
		elif loginAct == eSpaceLoginAction.LocalBirthPos:		 # ���´���һ���µ�space���ڳ���������
			self.teleportEntityOnLogin_(baseMailbox, params)			
		else:
			assert False, "unknow action. loginAct = '%s'" % loginAct
	
	def teleportEntityOnLogin_(self, baseMailbox, params):
		"""
		�ص�½�����¸�����ͼ�ĳ�����
		"""
		birthPoint = self.config_.birthPoint
		spaceData = g_mapConfigMgr.get(birthPoint)
		if spaceData is None:
			ERROR_MSG("Map config error, can not found the space, birthPoint = %d" % (birthPoint))
			return
		
		spaceItem = self.findSpaceItem( params.get("dbID", 0), True )
		if spaceItem is None:
			ERROR_MSG( "can't found or create space, params = %s, entity id = %s" % ( params, baseMailbox.id ) )
			return

		spaceItem.logon( baseMailbox, tuple(spaceData["position"]), tuple(spaceData["rotation"]) )	
	
	
	def _onSpaceBaseCreated( self, dbID, spaceBase, spaceItem ):
		"""
		����base������ϵĻص�
		"""
		self._spaceID2dbid[spaceBase.id] = dbID
		spaceItem.createCell()

	def createNewSpace( self, dbID ):
		"""
		����һ���µ�space
		"""
		# �����µ�SpaceItemʵ��
		spaceItem = SpaceItem( self.spaceType, self, self.eMetaClass, {} )
		self._dbid2spaceItem[dbID] = spaceItem
		spaceItem.createBase( Functor( self._onSpaceBaseCreated, dbID ) )
		return spaceItem

	def findSpaceItem( self, dbID, createIfNotExisted ):
		"""
		����space��

		@return: instance of SpaceItem or None
		"""
		if dbID in self._dbid2spaceItem:
			return self._dbid2spaceItem[dbID]
			
		# �����µ�SpaceItemʵ��
		if createIfNotExisted:
			return self.createNewSpace( dbID )
		return None

