# -*- coding: gb18030 -*-

"""
�����ڲ���ص�ȫ�ֶ��塣
������base/cell/client��app��
�����ϣ����ﶨ��ı�����Ӧ���ɳ����Լ��ı䣬���ڳ����ڲ�����߻����ֺ�ȷ���Ĺ̶����塣
���磺�Ա�״̬��NPC���͵Ķ����
"""
# ����ȫ������ǰ׺�������ֲ�ͬ�Ĺ���
GLOBALDATAPREFIX_SPACE_DOMAIN = "SpaceDomain."  # space domain��ǰ׺
GLOBALDATAPREFIX_SPACE = "Space."               # space ��ǰ׺
GLOBALDATAPREFIX_CELLAPP = "cellapp."			


SPACEDATA_SPACE_IDENT = "MetaClass"   # ��ͼ��Ψһ��ʶ��Ҳ����meta class���ƣ���ʶ��ͼ��Ψһ��
SPACEDATA_SPACE_NAME = "Name"         # ��ͼ���Ʊ�ʶ
SPACEDATA_CLIENT_PATH = "ClientPath"  # ���ڿͻ��˼��ص�ͼ�õĲ���
SPACEDATA_LINE_NUMBER = "LineNumber"  # ���ڶ��ߵ�ͼ��ע�ᵱǰ��ͼ���ڼ���
SPACEDATA_NAV_FLAGS = "NavFlags"	  # ����������־λ
SPACEDATA_REVIVE_TYPE_DISABLE = "ReviveTypeDisable"  # ����ֹ�ĸ�������

# --------------------------------------------------------------------
# about server state
# --------------------------------------------------------------------
SERVERST_STATUS_COMMON				= 1 	# ״̬һ��
SERVERST_STATUS_WELL				= 2		# ״̬����
SERVERST_STATUS_BUSY				= 3		# ��������æ
SERVERST_STATUS_HALTED				= 4		# ��������ͣ

COEF_PERCENT = 10000        # �ӳ�ֵ����ϵ��
COEF_ATK = 10000            # 2.6.1	ս��������ϵ��
COEF_COPY_MP_REGAIN = 0.5   # 2.6.2	��׼���������ָ�ϵ��
COEF_SKILL_DMG = 2.0        # 2.6.3	��׼�����˺�����
COEF_COPY_FIGHT_TIME = 120  # 2.6.4	��׼����ʱ��
COEF_PARRY = 0.5            # 2.6.5	��׼�мܱ���
COEF_CRIT = 2.0             # 2.6.6	��׼��������
COEF_HIT = 1.0              #       ��׼������


class DamageType:
	"""
	���������˺������ͣ������˺��������˺�
	"""
	Physics = 0  # �����˺�
	Magic = 1    # �����˺�

class FightResultType:
	Hit = 0x01   # ����
	Crit = 0x02  # ����

class QuestStatus:
	receive = 0     #�ѽ���
	doing = 1		#������
	complete = 2	#�����
	lose = 3		#��ʧ��
	reward = 4		#�ѽ���
	action = 5  	#��ִ��

class QuestType:
	mainQuest = 1	#��������
	branchQuest = 2 #֧������
	dayQuest = 3	#�ճ�����
	
class DialogType:
	QuestDialog = 0		#����Ի�
	NormalDialog = 1	#����