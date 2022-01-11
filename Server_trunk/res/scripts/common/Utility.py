# -*- coding: gb18030 -*-

import random


def enume( env, varList, start = 0 ):
	"""
	��һ�������ֵ������ö�ٶ���
	@param env: dict; ��Ҫ���ö�ٵ�Ŀ��
	@param varList: array of string; ö�ٱ������ַ���������["State_Move", "State_Jump", ...]
	@param start: int; ö��ֵ�Ŀ�ʼ
	@return: ����evn��������
	"""
	for index, varName in enumerate( varList, start ):
		env[varName] = index
	return env

def reverse_enume( env, varList, start = 0 ):
	"""
	��һ�������ֵ�������淴��ö�ٶ��塪��key Ϊö������ֵ��valueΪ(varList)�����е��ַ���������������
	�������������ֵ��key-value��enume()�����ĸպ��෴��
	
	@param env: dict; ��Ҫ���ö�ٵ�Ŀ��
	@param varList: array of string; ö�ٱ������ַ���������["State_Move", "State_Jump", ...]
	@param start: int; ö��ֵ�Ŀ�ʼ
	@return: ����evn��������
	"""
	for index, varName in enumerate( varList, start ):
		env[index] = varName
	return env

def initRand():
	"""
	��ʼ���������
	"""
	random.seed(int((time.time()*100)%256))

def estimate( odds, precision = 100 ):
	"""
	�жϼ���odds������ȱʡ1%
	@param			odds	  : ���ּ���
	@type			odds	  : int16
	@param			precision : ���Ȳ���
	@type			precision : integer
	@return					  : True ���ڼ���,False �����ڼ���
	@rtype					  : boolean
	"""
	if odds <= 0:
		return False
	if odds >= precision:
		return True
	r = int( random.random() * precision + 1 )
	if odds >= r:
		return True
	return False

def getTimestamp():
	"""
	���ʱ�����
	"""
	return int( ( KBEngine.time() * 10 ) % 1024 )

def searchFile( searchPath, exts ):
	"""
	����ָ����Ŀ¼(searchPath)���������з���ָ������չ��(exts)���ļ�����Ŀ¼����
	ע�⣺���ǲ����ж�һ���ļ��Ƿ����ļ��У�Ҳ�����еݹ���ң���������չ����ָ��Ŀ¼���в��ң�

	@param searchPath: STRING or tuple of STRING, Ҫ������·�����б�
	@param       exts: STRING or tuple of STRING, Ҫ��������չ�����б���ÿ����չ�����������Ե㿪ͷ�ģ��磺.txt
	@return: array of STRING
	"""
	assert isinstance( exts, (str, tuple, list) )
	assert isinstance( searchPath, (str, tuple, list) )
	if isinstance( exts, str ):
		exts = ( exts, )
	if isinstance( searchPath, str ):
		searchPaths = [ searchPath, ]
	else:
		searchPaths = list( searchPath )

	files = []
	for searchPath in searchPaths:
		section = ResMgr.openSection( searchPath )
		assert section is not None, "can't open section %s." % searchPath

		if searchPath[-1] not in "\\/":
			searchPath += "/"

		for key in section.keys():
			name, ext = os.path.splitext( key )		# ��ȡ��չ��
			if ext in exts:							# ��չ��ƥ��
				files.append( searchPath + key )
		ResMgr.purge( searchPath )
	return files

def ipToStr( val ):
	"""
	ת��int32��ip��ַΪ�Ե�(".")�ָ����ַ���ģʽ��
	����ipToStr( 436211884 ) --> '172.16.0.26'
	"""
	return "%i.%i.%i.%i" % ( val & 0xff, ( val >> 8 ) & 0xff, ( val >> 16 ) & 0xff, ( val >> 24 ) & 0xff )


