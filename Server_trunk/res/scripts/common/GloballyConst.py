# -*- coding: gb18030 -*-

"""
��Ϸ������ص�ȫ�ֳ���ֵ���壻
����base/cell/client��app���Ա�����Ҫ����ĳЩ����ʱ�����Է����ͨ����Щ������������
�����ϣ���������ǿ����ɲ߻������ġ�������������еĽ�Ǯ���޵ȵ�
"""

import GloballyDefine as GDef

# ����������λ�úͳ���
SPAWN_SPACE = "99999999"
SPAWN_POSITION = (-0.37, 3.808, 0.6395)
SPAWN_DIRECTION = (0.0, 0.0, 3.14)

# --------------------------------------------------------------------
# about login
# --------------------------------------------------------------------
LOGIN_ROLE_UPPER_LIMIT		= 3			# �����Դ������ٸ���ɫ


#-------------------------------------------------------------------------------
#about duplication
#--------------------------------------------------------------------------------
SPACE_CONST_DISTANCE = 10000		# ��λ���� ��space��cell�У�����ĳ��space��ĳ����Χ�ڵ�entity
SPACE_HYST = 2.0					# ָ������AOI������ͺ�����Ĵ�С
SPACE_CREATE_ENTITY_TIME = 0.1     # ����entitiy��С���


#----------------------------------------------------------------
# about cellapp
#----------------------------------------------------------------
CELLAPP_INIT_AMOUNT = 0				#���ٸ�cellapp�����󣬿�ʼ��ʼ��spaceManager
CELLAPP_NOT_BALCANING_AMOUNT = 0	#Ĭ�϶��ٸ�cellapp�����븺�ؾ���(����ֵ���������ֵʱ����������ȵ������븺�ؾ����cellapp�������󣬲ſ�ʼ����space)




MAIN_QUEST_FIRST_ID = 101000
MAX_QUEST_AMOUNT = 20
MAX_DAY_QUEST_AMOUNT = 20
MAX_COMP_DAY_QUEST_AMOUNT = 30
Quest_DAY_INTERVAL_TIME = 1800
Quest_Day_Need_GoldCoin = 15

