# -*- coding: gb18030 -*-
#

"""
Space domain class
"""
import json
import KBEngine
from KBEDebug import *

from Functor import Functor
import GloballyConst as GC
import GloballyDefine as GD
import MapDataConfig

# ������
class SpaceDomainBase(KBEngine.Base):
	"""
	ֻ����һ��space������ڵĿռ�����
	"""
	def __init__( self ):
		KBEngine.Base.__init__(self)
		
		# �����������ԣ���¼��space domainά�������ĸ�space�����磺fengming��yanhuang�ȵ�
		# �˲�����SpaceDomain������ʱ���ݣ�����ڴ˲����г�ʼ��
		#self.eMetaClass = ""
		
		# ��¼��Ӧ�����ýű�
		self.config_ = MapDataConfig.get( self.eMetaClass )
		
		# ע���Լ���MailBox��ȫ�������У��Է���������baseapp��cellapp����ʱʹ��
		self.registerToGlobalData()
		
	def registerToGlobalData(self):
		"""
		ע���Լ���MailBox��ȫ�������У��Է���������baseapp��cellapp����ʱʹ��
		"""
		key = GD.GLOBALDATAPREFIX_SPACE_DOMAIN + self.eMetaClass
		if key in KBEngine.globalData:
			assert "There has one '%s' alreadly!!!" % self.eMetaClass
		
		KBEngine.globalData[key] = self

	@staticmethod
	def findSpaceDomain( domainName ):
		"""
		����ָ���ĵ�ͼ���������
		"""
		try:
			key = GD.GLOBALDATAPREFIX_SPACE_DOMAIN + domainName
			spaceDM = KBEngine.globalData[key]
			return spaceDM
		except KeyError:
			return None

	def gotoPrevSpace_( self, baseMailbox, prevSpace, prevPos, prevDir, params ):
		"""
		������һ��ͼ
		"""
		if not prevSpace or prevSpace == self.eMetaClass: # �����һ����ͼ�뵱ǰ��ͼһ�����ǿ϶��ǳ������ˣ�ֻ�ܳ��Է��ع̶���ͼ
			prevSpace = GC.SPAWN_SPACE
			prevPos = GC.SPAWN_POSITION
		prevDomain = self.findSpaceDomain( prevSpace )
		prevDomain.teleportEntityOnLogin( baseMailbox, prevPos, prevDir, "", (0.0, 0.0, 0.0), params )

	def onSpaceLoseCell( self, spaceEntityID ):
		"""
		define method.
		space entity ʧȥ��cell���ݺ��ͨ�棻
		��Ҫ����δ���п��ܴ��ڵĿɴ洢����������������̫��ʱ���ܻῼ����û����ҵ�ʱ��ֻ����base���ݣ���ʱ����Ҫ����ͨ�棻
		@param 	key: int; ����space��entity��entity id
		"""
		INFO_MSG("%s space %d lose cell."%( self.eMetaClass, spaceEntityID ))
		
	def onSpaceGetCell( self, spaceEntityID ):
		"""
		define method.
		ĳ��space��cell���ݴ�����ɻص����˻ص������ڱ�������space��onGetCell()������ʱ���á�
		���ǿ��ڴ˻ص���ִ��һЩ���飬��ѵȴ������space����Ҵ��ͽ���space�ȵȡ�
		@param 	key: int; ����space��entity��entity id
		"""
		INFO_MSG("%s space %d create cell Complete"%( self.eMetaClass, spaceEntityID ))
		
	def onSpaceCloseNotify( self, spaceEntityID ):
		"""
		define method.
		�ռ�رգ�space entity����֪ͨ��
		@param 	key: int; ����space��entity��entity id
		"""
		INFO_MSG("%s space close : %d"%( self.eMetaClass, spaceEntityID ))

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
		pass

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
		pass

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
		pass

	def getMultiLines( self, baseMailbox ):
		"""
		define method
		��һ�ȡ���ߵ�ͼ��������
		@param baseMailbox: entity ��base mailbox
		"""
		baseMailbox.client.getMultiLines( json.dumps([]) )
		
	def setMultiLine( self, baseMailbox, position, direction, lineNumber ):
		"""
		define method
		��һ���
		@param baseMailbox: entity ��base mailbox
		@param position : VECTOR3, 
		@param direction : VECTOR3, 
		@param lineNumber:�ߺ�
		"""
		pass