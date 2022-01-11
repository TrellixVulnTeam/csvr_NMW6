# -*- coding: gb18030 -*-

"""
����
	ʹ���¼�ǰ����Ϊ����ȷ�����¼�����һ������Ϣ�ꡱ��������Ϣ������д����ģ��Ŀ�ͷ��

������
class test:
	def __init__( self ):
		registerEvent( "EVENT_STRING", self )	# �ڳ�ʼ����ʱ�����Ҫ��ʱ��ע��ĳ���¼�

	def __del__( self ):
		unregisterEvent( "EVENT_STRING", self )	# ��ʵ����ɾ����ʱ�������Ҫ��ʱ��ȡ����ĳ���¼���ע��

	def onEvent( self, name, *args ):			# ����ע��ʵ������������������������ڱ���������Ϣ����ʱ�Զ�����ע��ʵ����onEvent()����
		if name == "EVENT_STRING":
			do some thing in here
		else:
			do other
"""

"""
2006.02.24: writen by penghuawei
2009.02.26: tidy up by huangyongwei
ע�⣺
	��ע�����ʵ������������������onEvent
	����Ϣ����ʱ��onEvent ���ᱻ������onEvent �ĵ�һ���������������������Ϣ�꣬������ſ��������ɸ���������ͬ����Ϣ���������һ����
"""

import sys
import weakref
from KBEDebug import *


# --------------------------------------------------------------------
# ʵ���¼���ͻ���ȫ���¼���( ÿ����Ϣ���Ӧһ���¼�ʵ�� )
# --------------------------------------------------------------------
class _Event:									# ��Ϊģ��˽�У�hyw--2009.02.26��
	def __init__( self, name ):
		self._name = name						# �¼�����
		self._receivers = []					# �¼������ߣ�ע��ÿ����Ϣ�����ж��������( renamed from 'handlers' to 'receiver' by hyw--2009.02.26 )

	def fire( self, *argv ):
		"""
		�����¼�
		"""
		for index in range( len( self._receivers ) - 1, -1, -1 ):
			receiver = self._receivers[index]()
			if receiver:
				#try:
					receiver.onEvent( self._name, *argv )
				#except Exception as errstr:
				#	err = "error take place when event '%s' received by %s:\n" % ( self._name, str( receiver ) )
				#	DEBUG_MSG( err )
			else:
				self._receivers.pop( index )

	def addReceiver( self, receiver ):
		"""
		�����Ϣ������
		"""
		wr = weakref.ref( receiver )
		if wr not in self._receivers :
			self._receivers.append( wr )

	def removeHandler( self, receiver ):
		"""
		ɾ����Ϣ������
		"""
		receive = weakref.ref( receiver )
		if receive in self._receivers :
			self._receivers.remove( receive )

	def clearReceivers( self ):
		"""
		��������¼�������
		"""
		self._receivers=[]

class _EventExtend:
	def __init__( self, name ):
		self._name = name						# �¼�����
		self._receivers = {}					# �¼������ߣ�ע��ÿ����Ϣ�����ж��������( renamed from 'handlers' to 'receiver' by hyw--2009.02.26 )
	
	def fire( self, fireObj , *argv ):
		"""
		�����¼�
		"""
		for id in list(self._receivers.keys()):
			eventFun = self._receivers[id]
			func = getattr(fireObj, eventFun)
			if func != None:
				func(id, *argv)	
	
	def addReceiver( self, id, funcName ):
		"""
		�����Ϣ������
		"""
		self._receivers[id] = funcName

	def removeHandler( self, id ):
		"""
		ɾ����Ϣ������
		"""
		del self._receivers[id]

	def clearReceivers( self ):
		"""
		��������¼�������
		"""
		self._receivers={}	
	
class SpaceEvent:
	
	def __init__(self):
		self.g_events = {}				# key����Ϣ�꣬����Ϊ str��value���� _Event ��ʵ��
		self.g_eventsExtend = {}		# �¼�ϵͳ��չ
		
	# --------------------------------------------------------------------
	# ʵ���¼�ע��͵����ӿ�
	# --------------------------------------------------------------------
	def registerEvent(self, eventKey, receiver ):
		"""
		ע��һ���¼�
		@type			eventKey : str
		@param			eventKey : ��Ϣ��
		@type			reveiver : class instance
		@param			reveiver : ��Ϣ�����ߣ�ע�⣺���¼������߱������������onEvent��
		"""
		try:
			event = self.g_events[eventKey]
		except KeyError:
			event = _Event( eventKey )
			self.g_events[eventKey] = event
		event.addReceiver( receiver )

	def unregisterEvent(self, eventKey, receiver ):
		"""
		ɾ��һ����Ϣ������
		@type			eventKey : str
		@param			eventKey : ��Ϣ��
		@type			reveiver : class instance
		@param			reveiver : Ҫɾ������Ϣ������
		"""
		try:
			self.g_events[eventKey].removeHandler( receiver )
		except KeyError:
			err = "receiver is not in list of enevt '%s''" % eventKey

	def registerEventID(self, eventKey, id, funcName ):
		"""
		ע��һ���¼�
		@type			eventKey : str
		@param			eventKey : ��Ϣ��
		@param			id 		 : int ��������ID
		@param			funcName : �������ƣ�������Ϊ����ר��Ϊ�����ṩ���¼�������
		"""
		try:
			event = self.g_eventsExtend[eventKey]
		except KeyError:
			event = _EventExtend( eventKey )
			self.g_eventsExtend[eventKey] = event
		event.addReceiver( id, funcName )
	
	def unregisterEventID(self, eventKey, id ):
		"""
		ɾ��һ����Ϣ������
		@type			eventKey : str
		@param			eventKey : ��Ϣ��
		@type			id 		 : int
		@param			id		 : ��������ID
		"""	
		try:
			self.g_eventsExtend[eventKey].removeHandler( id )
		except KeyError:
			err = "receiver is not in list of enevt '%s''" % eventKey
		
	
	def fireEvent(self, eventKey, *args ):
		"""
		����ָ���¼�
		@type			eventKey : str
		@param			eventKey : Ҫ��������Ϣ����
		@type			*args	 : all types
		@param			*args	 : ��Ϣ����
		"""
		try:
			if eventKey in self.g_events:
				self.g_events[eventKey].fire( *args )
		except KeyError:
			pass
		
		try:		
			if eventKey in self.g_eventsExtend:
				self.g_eventsExtend[eventKey].fire( self, *args )
		except KeyError:
			pass
