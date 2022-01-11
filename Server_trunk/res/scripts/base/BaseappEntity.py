# -*- coding: gb18030 -*-

"""
Ŀ�ģ�ϣ��ÿ��baseapp����֪��������baseapp���Ա�㲥һЩ����
���������Ҫ��ÿ��baseapp�ϲ���һ��BaseEntity������ע���ΪglobalBase��
�Դ�����ʶÿһ��baseapp����ô�����ǾͿ���ͨ�����baseEntity�㲥һЩ���ݵ����е�baseapp�ϣ�
�磺ȫ������

"""

import KBEngine
from KBEDebug import *
import Account
import Player
import json
import GloballyDefine as GD

class BaseappEntity( KBEngine.Base ):
	"""
	"""
	C_PREFIX_GBAE = "GBAE"
	def __init__( self ):
		KBEngine.Base.__init__( self )

		# ��¼���к��Լ�ͬһ���͵�����baseApp mailbox
		# ����ÿ�ι㲥��ʱ��Ϳ���ֱ��ʹ�ã�������Ҫ�ٴε�KBEngine.globalBases��ȥ��ѯ�Ƚ�
		self.globalData = {}

		# entity�������У�ֵΪ����ı���spaceEntity��
		# ��һ��Ϊ��ǰ���ڴ�����space�����һ��Ϊ�������space���Դ�����
		self.spawnQueue = []

		self.register2baseAppData()

		# ͨ���ڴ�baseapp���ߵ���ҵ�������entityʵ���Ķ�Ӧ��
		# { "�������" : instance of entity which live in KBEngine.entities, ... }
		self._localPlayers = {}

		# ��ʱ�б�����ʵ��lookupPlayerBaseByName()�Ļص�����
		# { ��ʱΨһID : [ Ԥ�ڻظ�����, ��ʱʱ��, callback ], ...}
		# ��Ԥ�ڻظ���������ָ���ǵ�ǰ�򼸸�baseapp����������ÿ�յ�һ���ظ�����ֵ����һ
		# ����ʱʱ�䡱����λ���롱��float��ÿ����һ�Σ������ʱ���жϲ��ص�֪ͨĿ��δ�ҵ���������������ԭ��ܿ��������й�����ĳ̨baseapp������
		# callback: function���ɵ������ṩ�Ļص�����
		self._tmpSearchCache = {}
		self._tmpSearchCurrentID = 0	# ���ڼ�¼���һ�η����IDֵ��ֵ 0 ���ڱ�ʾû�л�ʧ�ܣ���˲���Ϊ����ID����
		self._searchTimerID = 0			# ���ڼ��ĳ��lookupPlayerBaseByName()�����Ƿ���ڵ�timer

	def register2baseAppData( self ):
		"""
		ע�ᵽbaseAppData��
		"""
		# ʹ���Լ���entityID����ǰ׺�γ�Ψһ������
		# GBAE is global baseApp Entity, don't use "GBAE*" on other globalBases Key
		self.globalName = "%s%i" % ( self.C_PREFIX_GBAE, self.id )
		KBEngine.baseAppData[self.globalName] = self

		KBEngine.globalData[ self.globalName ] = self		# ͬʱע�ᵽKBEngine.globalData��
		# todo(phw)�����������ѭ�����ã��������ر�ʱ�п��ܻ�������⣬����������Ҫ���д���
		self.globalData[self.globalName] = self					# �����ڲ����ã�
		#��������Ҳ��������
		for key,value in KBEngine.baseAppData.items():
			index = key.find(self.C_PREFIX_GBAE)
			if index != -1:
				self.addRef(key, value)
				value.addRef(self.globalName, self)
				
	def addRef( self, globalName, baseMailbox ):
		"""
		defined method.
		֪ͨ��������

		@param globalName: ȫ��base��ʶ��
		@type  globalName: STRING
		@param baseMailbox: �������ߵ�mailbox
		@type  baseMailbox: MAILBOX
		@return: һ�������˵ķ�����û�з���ֵ
		"""
		self.globalData[globalName] = baseMailbox

	def removeRef( self, globalName ):
		"""
		defined method.
		֪ͨɾ������

		@param baseMailbox: �������ߵ�mailbox
		@type  baseMailbox: MAILBOX
		@return: һ�������˵ķ�����û�з���ֵ
		"""
		try:
			del self.globalData[globalName]
		except KeyError:
			WARNING_MSG( "no global base entity %s." % globalName )
			pass

	# -----------------------------------------------------------------
	# ������ҵ�¼���
	# -----------------------------------------------------------------
	def registerPlayer( self, entity ):
		"""
		�Ǽ�һ����ҵ�entity�����б��Ǽǵ���Ҷ�����Ϊ�����ߵ�
		"""
		self._localPlayers[entity.getName()] = entity

	def deregisterPlayer( self, entity ):
		"""
		ȡ����һ�����entity�ĵǼ�
		"""
		# ʹ��pop����del���Ա�����Ϊ�����ĳЩԭ���ڵ�¼ʱδ��ȷע���ʹ�÷�ע��ʧ��
		# ע����ʧע��ʧ�ܲ����쳣ʱ���ᵼ��Player��destroy���̱���ϣ���ʹ������޷��ٴε�¼
		self._localPlayers.pop(entity.getName(), None)

	def iterOnlinePlayers( self ):
		"""
		��ȡһ��������ҵ�iterator

		@return: iterator
		"""
		return self._localPlayers.values()

	# -----------------------------------------------------------------
	# ������Ϣ�㲥���
	# -----------------------------------------------------------------
	def broadcastChat( self, channel, speakerName, speakerDBID, msg, params ):
		"""
		Define method.
		�㲥��ҵķ������ݵ���ǰBaseApp������client

		@param     channel: �㲥Ƶ��
		@type      channel: INT8
		@param speakerName: Դ˵��������
		@type  speakerName: STRING
		@param speakerDBID: Դ˵����DBID
		@param         msg: ��Ϣ����
		@type          msg: STRING
		@param      params: ��������
		@type       params: ARRAY <of> UNICODE </of>
		@return: һ�������˵ķ�����û�з���ֵ
		"""
		# �㲥��ÿ��client
		for e in self._localPlayers.values():
			# ֻ�㲥�����
			if not isinstance( e, Player.Player ): continue
			e.client.receiveChatMessage( channel, speakerName, speakerDBID, msg, params )

	def globalChat( self, channel, speakerName, speakerDBID, msg, params ):
		"""
		�㲥��ҵķ������ݵ����е�BaseApp

		@param     channel: �㲥Ƶ��
		@type      channel: INT8
		@param speakerName: Դ˵��������
		@type  speakerName: STRING
		@param         msg: ��Ϣ����
		@type          msg: STRING
		@param      params: ��������
		@type       params: ARRAY <of> UNICODE </of>
		@return: ��
		"""
		# ֪ͨÿ��baseApp, �����Լ�
		for e in self.globalData.values():
			e.broadcastChat( channel, speakerName, speakerDBID, msg, params )

	# -----------------------------------------------------------------
	# timer
	# -----------------------------------------------------------------
	def onTimer( self, timerID, userData ):
		"""
		"""
		# �꿴lookupPlayerBaseByName()����õ�addTimer()
		# ����ʱ������
		if timerID == 12345:
			time = KBEngine.time()
			for k, v in list(self._tmpSearchCache.items()):	# ʹ��items()��ֱ�Ӹ����б�������ѭ�������ֱ��ɾ���ֵ����ݣ��˷���ֻ�������������ݵĵط�
				if time >= v[1]:
					del self._tmpSearchCache[k]
					v[2]( None )

			# ���û�����������ˣ�����ֹͣtimer
			if len( self._tmpSearchCache ) == 0:
				self.delTimer( self._searchTimerID )
				self._searchTimerID = 0


	# -----------------------------------------------------------------
	# about lookupPlayerBaseByName() mechanism
	# -----------------------------------------------------------------
	def lookupPlayerBaseByName( self, name, callback ):
		"""
		�������ֲ����������ǵ�base mailbox
		@param name: string; Ҫ���ҵ��������ǵ����֡�
		@param callback: function; �ûص�����������һ�����������ڸ��ص����ṩ���ҵ����������ǵ�base mailbox�����δ�ҵ������ֵΪNone��
		@return: None
		"""
		resultID = self._getLookupResultID()
		self._tmpSearchCache[resultID] = [ len( self.globalData ), KBEngine.time() + 2, callback ]	# [ Ԥ�ڻظ�����, ��ʱʱ��д��2��, callback ]
		for v in self.globalData.values():
			v._broadcastLookupPlayerBaseByName( self, resultID, name )

		if self._searchTimerID == 0:
			self.addTimer( 1, 1, 12345 )

	def _broadcastLookupPlayerBaseByName( self, resultBase, resultID, name ):
		"""
		defined method.
		����BaseappEntity�ڲ����ã�����ʵ��lookupPlayerBaseByName()�Ļص�����

		@param resultBase: BASE MAILBOX
		@param resultID: int32
		@param name: string
		"""
		resultBase._broadcastLookupPlayerBaseByNameCB( resultID, self._localPlayers.get( name ) )

	def _broadcastLookupPlayerBaseByNameCB( self, resultID, baseMailbox ):
		"""
		defined method.
		����BaseappEntity�ڲ����ã�����ʵ��lookupPlayerBaseByName()�Ļص�����
		���baseMailbox��ΪNone�����ʾ�ҵ�����_tmpSearchCache����������ص���
		���baseMailboxΪNone�������е�baseapp�ѻظ�����ʾû���ҵ�����_tmpSearchCache����������ص���
		���baseMailboxΪNone���һظ���baseapp��û��ȫ���ظ���baseapp�Ļظ�����һ��ֱ�ӷ���

		@param baseMailbox: ���ҵ���Ŀ��entity base mailbox
		"""
		if resultID not in self._tmpSearchCache: return		# δ�ҵ���ʾ�Ѿ����ظ��ˣ�����������
		r, time, callback = self._tmpSearchCache[resultID]
		r -= 1
		if baseMailbox is None and r > 0:	# ����������δ�ظ����ı��������ֱ�ӷ���
			self._tmpSearchCache[resultID][0] = r
			return

		del self._tmpSearchCache[resultID]
		# ���û�����������ˣ�����ֹͣtimer
		if len( self._tmpSearchCache ) == 0:
			self.delTimer( self._searchTimerID )
			self._searchTimerID = 0

		# �ص�
		callback( baseMailbox )

	def _getLookupResultID( self ):
		"""
		���һ�����ڹ㲥lookupPlayerBaseByName()��Ψһ��idֵ
		@return: INT32
		"""
		self._tmpSearchCurrentID += 1
		if self._tmpSearchCurrentID >= 0x7FFFFFFF:
			self._tmpSearchCurrentID = 1

		# ѭ���жϲ���ȡһ������_tmpSearchCache�д��ڵ�IDֵ
		while self._tmpSearchCurrentID in self._tmpSearchCache:
			self._tmpSearchCurrentID += 1
			if self._tmpSearchCurrentID >= 0x7FFFFFFF:
				self._tmpSearchCurrentID = 1
		return self._tmpSearchCurrentID
	
	# ------------------------------------------------------------------------
	# space spawn�Ĵ������
	# ���˼�룺��һ��space����������Ժ�����space��baseappEntity(��ǰ��)
	#           ע��(����pushSpawn())��baseappEntity�����ŵ������У����ֵ���
	#           space����entityʱ����ø�spaceEntity��createSpawnPoint()������
	#           spaceEntity����entity��ɺ�����baseappEntity����Ӷ�����ɾ��
	#           ������popSpawn()����
	# �ʣ�Ϊʲô��ֱ����ÿ��spaceEntity����ʱ�Լ���������entity��
	# ������һ��baseapp���ܻ�ͬʱ�������space�����ÿ��spaceͬʱ����entity��
	#     ��ôֻ������ÿ��spaceÿ��ͬʱ���������ģ���10����entity�������baseapp
	#     ��entityID����������ٶ�������
	# �ʣ�Ϊʲô��Ҫspaceÿ�봴��������entity��ÿ��ֻ����10������ʲô���⣺
	# �����ÿ��ֻ����10��entity����ô������ҽ��븱����ʱ�򣬸ø���������Ҫ��
	#     ��ʱ����ܰ�entity�����꣬��������Ҹս��븱��ʱ���ܻ�ʲô����������
	#     ��ˣ�������Ҫͬʱ���������entity��ʹ����ʱ�価�����١�������ô����
	#     �������ͬʱ���������⣬���������Ҫ�෽����أ��縱����entity������Щ��
	#     �����ô����ٶȼӿ죬���ڲ�ͬ��baseapp�ﴴ��������
	# �ʣ�Ϊʲô������spaceManager�У����Ƿ���ÿ��baseapp�У�
	# ���������ĺô���ÿ��baseapp������ͬʱ�����Լ��������ϵ�space��entity��
	#     �Դﵽ������Ŀ�ġ�
	# ------------------------------------------------------------------------
	def pushSpawn( self, spaceEntity ):
		"""
		��ջһ��spaceEntity��spawn����������
		"""
		self.spawnQueue.append( spaceEntity )
		if len( self.spawnQueue ) == 1:
			self.spawnQueue[0].createSpawnPoint()

	def popSpawn( self ):
		"""
		��ջ��ǰ�����ڴ���spawn��spaceEntity
		"""
		self.spawnQueue.pop( 0 )
		if len( self.spawnQueue ) > 0:
			self.spawnQueue[0].createSpawnPoint()

			