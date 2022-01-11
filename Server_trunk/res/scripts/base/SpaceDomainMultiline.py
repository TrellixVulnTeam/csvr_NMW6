# -*- coding: gb18030 -*-
#

"""
Space domain class
"""
import json
import time
import KBEngine
from KBEDebug import *

from Functor import Functor
from Extra.SpaceItem import SpaceItem
from interfaces.SpaceDomainBase import SpaceDomainBase

TIMER_ENTER_TIMEROUT = 5 #��ҵ���space��ʱʱ�䣬�������ʱ�䣬��Ϊ��ҵ���spaceʧ�ܣ��򽫶�Ӧ�ߵ�������һ

class SpaceDomainMultiline(SpaceDomainBase):
	"""
	���ߵ�ͼ�Ŀռ�����ƽ��space����
	"""
	def __init__( self ):
		SpaceDomainBase.__init__(self)
		
		self._lineNumber2spaceItem = {}
		self._spaceEntityID2lineNumber = {}
		self._playerAmount = {}					# ����ÿ��space��������key�����ߺţ�value���Ǹ����µ��������
		self._enteringPlayer = {}				# ��¼��ǰ������ת����ͼ�����
		
		# �Ƿ������˹̶������ĸ�������
		if self.config_.initLine > 0:
			for line in range( 1, self.config_.initLine + 1 ):
				self.createNewSpace( line )
				
		self.addTimer(TIMER_ENTER_TIMEROUT, TIMER_ENTER_TIMEROUT, 0)

	def _onSpaceBaseCreated( self, lineNumber, spaceBase, spaceItem ):
		"""
		����base������ϵĻص�
		"""
		self._spaceEntityID2lineNumber[spaceBase.id] = lineNumber
		spaceItem.createCell()

	def createNewSpace( self, lineNumber ):
		"""
		����һ���µ�space
		"""
		# �����µ�SpaceItemʵ��
		spaceItem = SpaceItem( self.spaceType, self,  self.eMetaClass, { "lineNumber" : lineNumber } )
		self._lineNumber2spaceItem[lineNumber] = spaceItem
		self._playerAmount[lineNumber] = 0
		spaceItem.createBase( Functor( self._onSpaceBaseCreated, lineNumber ) )
		return spaceItem

	def onSpaceLoseCell( self, spaceEntityID ):
		"""
		define method.
		space entity ʧȥ��cell���ݺ��ͨ�棻
		��Ҫ����δ���п��ܴ��ڵĿɴ洢����������������̫��ʱ���ܻῼ����û����ҵ�ʱ��ֻ����base���ݣ���ʱ����Ҫ����ͨ�棻
		@param 	key: int; ����space��entity��entity id
		"""
		INFO_MSG("%s space %d lose cell."%( self.eMetaClass, spaceEntityID ))
		lineNumber = self._spaceEntityID2lineNumber[spaceEntityID]
		self._lineNumber2spaceItem[lineNumber].onLoseCell()
		
	def onSpaceGetCell( self, spaceEntityID ):
		"""
		define method.
		ĳ��space��cell���ݴ�����ɻص����˻ص������ڱ�������space��onGetCell()������ʱ���á�
		���ǿ��ڴ˻ص���ִ��һЩ���飬��ѵȴ������space����Ҵ��ͽ���space�ȵȡ�
		@param 	key: int; ����space��entity��entity id
		"""
		INFO_MSG("%s space %d create cell Complete"%( self.eMetaClass, spaceEntityID ))
		lineNumber = self._spaceEntityID2lineNumber[spaceEntityID]
		self._lineNumber2spaceItem[lineNumber].onGetCell()
		
	def onSpaceCloseNotify( self, spaceEntityID ):
		"""
		define method.
		�ռ�رգ�space entity����֪ͨ��
		@param 	key: int; ����space��entity��entity id
		"""
		INFO_MSG("%s space close : %d"%( self.eMetaClass, spaceEntityID ))
		lineNumber = self._spaceEntityID2lineNumber[spaceEntityID]
		self._spaceEntityID2lineNumber.pop(spaceEntityID, None)
		self._lineNumber2spaceItem.pop(lineNumber, None)
		
		for entityID in list(self._enteringPlayer.keys()):
			lineNum = self._enteringPlayer[entityID]["lineNumber"]
			if lineNum == lineNumber:
				self._enteringPlayer.pop(entityID) 

	def onEntityEnterSpace( self, spaceBaseMailbox, entityBaseMailbox ):
		"""
		��ҽ�����ĳ��space��֪ͨ������space domain��������������һЩ����
		"""
		lineNumber = self._spaceEntityID2lineNumber[spaceBaseMailbox.id]
		#self._playerAmount[lineNumber] += 1
		self._enteringPlayer.pop(entityBaseMailbox.id, None)

	def onEntityLeaveSpace( self, spaceBaseMailbox, entityBaseMailbox ):
		"""
		����뿪��ĳ��space��֪ͨ������space domain��������������һЩ����
		"""
		lineNumber = self._spaceEntityID2lineNumber[spaceBaseMailbox.id]
		self._playerAmount[lineNumber] -= 1

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
		spaceItem = self.findSpaceItem( baseMailbox.id, params.get("lineNumber", 0) )
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
		for mb in baseMailboxs:
			spaceItem = self.findSpaceItem( mb.id, params.get("lineNumber", 0) )
			spaceItem.enter( mb, position, direction )
		
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
		spaceItem = self.findSpaceItem( baseMailbox.id, params.get("lineNumber", 0) )
		spaceItem.logon( baseMailbox, defaultPos, defaultDir )

	def findSpaceItem( self, entityID, lineNumber ):
		"""
		ͨ���ߺ�������space��

		@param entityID: int; 
		@param lineNumber: int; ��ȡָ���ߺ�
		@param createIfNotExisted: bool; ���Ҳ���ʱ�Ƿ񴴽�
		@return: instance of SpaceItem or None
		"""		
		# �ߺŲ�����Ч��Χ�ڣ���һ�����е��ߺ�
		if lineNumber <= 0 or lineNumber > self.config_.maxLine:
			lineNumber = self.findFreeSpace()
			
		spaceItem = self._lineNumber2spaceItem.get( lineNumber )
		if not spaceItem:
			spaceItem = self.createNewSpace( lineNumber )
		
		if entityID in self._enteringPlayer:
			if self._enteringPlayer[entityID]["lineNumber"] in self._playerAmount:
				self._playerAmount[self._enteringPlayer[entityID]["lineNumber"]] -= 1
			
		self._enteringPlayer[entityID] = { "lineNumber" : lineNumber, "time" : int(time.time()) }
		self._playerAmount[lineNumber] += 1	
		
		return spaceItem

	def findFreeSpace( self ):
		"""
		Ѱ��һ����Կ��еĸ��� ���ظ������
		"""
		if self.config_.maxLine <= 0 or len( self._playerAmount ) <= 0:
			return 1;

		# Ѱ��δ���������ĸ���
		for lineNumber, playerAmount in self._playerAmount.items():
			if playerAmount < self.config_.newLineByPlayerAmount:
				return lineNumber

		# ������и���δ���� ������
		if len( self._lineNumber2spaceItem ) < self.config_.maxLine:
			for lineNumber in range( 1, self.config_.maxLine + 1 ):
				if not lineNumber in self._lineNumber2spaceItem:
					return lineNumber

		# ���и��������ˣ���ôѰ���������ٵĵ�һ������
		sitems = list( self._playerAmount.items() )
		enterID, playerAmountMin = sitems.pop(0)
		for spaceEnterID, playerAmount in self._playerAmount.items():
			if playerAmount < playerAmountMin:
				enterID = spaceEnterID
				playerAmountMin = playerAmount
		return enterID
		
	def getMultiLines( self, baseMailbox ):
		"""
		define method
		��һ�ȡ���ߵ�ͼ��������
		@param baseMailbox: entity ��base mailbox
		"""
		lst = []
		for key, value in self._playerAmount.items():
			dct = {"lineNumber" : key, "amount" : value}
			lst.append(dct)
			
		baseMailbox.client.getMultiLines( json.dumps(lst) )
		
	def setMultiLine( self, baseMailbox, position, direction, lineNumber ):
		"""
		define method
		��һ���
		@param baseMailbox: entity ��base mailbox
		@param position : VECTOR3, 
		@param direction : VECTOR3, 
		@param lineNumber:�ߺ�
		"""
		spaceItem = self._lineNumber2spaceItem.get( lineNumber )
		if spaceItem:
			if baseMailbox.id in self._enteringPlayer:
				if self._enteringPlayer[baseMailbox.id]["lineNumber"] in self._playerAmount:
					self._playerAmount[self._enteringPlayer[baseMailbox.id]["lineNumber"]] -= 1
			
			self._enteringPlayer[baseMailbox.id] = { "lineNumber" : lineNumber, "time" : int(time.time()) }	
			self._playerAmount[lineNumber] += 1	
			spaceItem.enter( baseMailbox, position, direction )
			
	def onTimer( self, timerID, userArg ):
		"""
		�����Ƴ�δ�ɹ���ת����ͼ�����
		"""
		for entityID in list(self._enteringPlayer.keys()):
			t = time.time() - self._enteringPlayer[entityID]["time"]
			if t >= TIMER_ENTER_TIMEROUT:
				lineNumber = self._enteringPlayer[entityID]["lineNumber"]
				if lineNumber in self._playerAmount:
					self._playerAmount[lineNumber] -= 1
				
				self._enteringPlayer.pop(entityID)
			
		
