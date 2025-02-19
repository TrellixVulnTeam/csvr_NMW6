﻿using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class MonsterAI : MonoBehaviour {

    public enum EnermyAIState
    {
        AI_Null,
        AI_Born,        //出生状态
        AI_Idle,        //空闲状态
        AI_Patrol, //巡逻状态
        AI_FightThink, //追击状态
        AI_CastSpell, //攻击状态
        AI_ChaseEntity, //徘徊状态
        AI_Reset, //回到出生点
    }
    public EnermyAIState vStartState;
    EnermyAIState vLostState;

    public enum BornType //出生类型
    {
        NUll,
        Born_Dissolve, //溶解出生
    }
    public BornType bornType = BornType.Born_Dissolve;
    public float bornTime = 4.0f;
    public GameObject cuttingDeathObject;
    public float alertRadius = 6.0f;//警戒范围
    public float chaseRadius = 50.0f;//追击半径（超过此半径，怪物应脱离战斗并回到出生点）         
    public float idleSpeed = 2.0f;//空闲移动速度
    public float hoverRadiusMin = 3.0f;//徘徊半径（内圈）
    public float hoverRadiusMax = 4.5f;//徘徊半径（外圈）
    public float hoverWalkSpeed = 3.0f;//战斗徘徊移动速度
    public float hoverWaitTime = 1.0f; //徘徊停顿时间
    public float attackActive = 0.7f;//攻击积极性
    public float attackWaitTime = 0.0f; //攻击停顿时间
    public float idleStopTime = 2.0f;
    public float wanderAngle = 120;//徘徊扇形角度

    Vector3 Dis; //空闲状态随机移动位置
    Vector3 srcPoint;//出生坐标
    float LastThinkTime = 0.0f;
    Vector3 targetPosition = Vector3.zero;//徘徊一次的目标点
    float targetSpeed = 0.0f;//徘徊一次的速度
    Animator m_animator;
    bool attackFlag = false;//攻击标记
    bool isAttack = true;//是否在攻击中标记
    UnityEngine.AI.NavMeshAgent m_navMeshAgent;
    float randomValue;
    bool isAIRuning = true; //用于开启和暂停AI

    private AvatarComponent own;              
    private AvatarComponent target = null;   //目标

    public int[] skillList = {2000001};      //技能id列表
    private SPELL.Spell currentSpell = null; //当前要使用的技能
    float lastTime = 0.0f;
    bool bornFlag = false;

    private float accumulateTime = 0.0f;

    void Awake()
    {
        if (bornType == BornType.Born_Dissolve)
        {
            Renderer[] renderers = gameObject.GetComponentsInChildren<Renderer>();
            for (int i = 0; i < renderers.Length; i++)
            {
                renderers[i].enabled = false;
            }
        }
    }

    // Use this for initialization
    void Start()
    {
        lastTime = Time.time;
        vStartState = EnermyAIState.AI_Born;
        vLostState = EnermyAIState.AI_Null;
        srcPoint = new Vector3(transform.position.x, transform.position.y, transform.position.z);
           
        m_animator = this.GetComponent<Animator>();
        m_navMeshAgent = gameObject.GetComponent<UnityEngine.AI.NavMeshAgent>();
        own = gameObject.GetComponent<AvatarComponent>();

        own.eventObj.register("Event_OnActionRestrictChanged", this, "OnActionRestrictChanged");
        own.eventObj.register("Event_OnStatusChanged", this, "OnStatusChanged");
        own.eventObj.register("Event_OnReceiveDamage", this, "onReceiveDamage");
        own.eventObj.register("Event_OnChangeSpeed", this, "onChangeSpeed");
        own.eventObj.register("Event_OnDead", this, "onDead");
    }

    public void OnActionRestrictChanged(int newRestrict, int oldRestrict)
    {      
        int offset = newRestrict ^ oldRestrict;
        if ((offset & (1 << (int)eActionRestrict.ForbidMove)) > 0)
        {
            bool value = (newRestrict & (1 << (int)eActionRestrict.ForbidMove)) > 0;
            if (value)
            {
                stopAI();
            }
            else
            {
                startAI();
            }
        }
    }

    public void OnStatusChanged(eEntityStatus newStatus, eEntityStatus oldStatus)
    {
    }

    public void onChangeSpeed(float fSpeed)
    {
        hoverWalkSpeed += fSpeed;
        m_navMeshAgent.speed = hoverWalkSpeed;
    }

    // Update is called once per frame
    void Update()
    {
        if (!isAIRuning)
            return;

        switch (vStartState)
        {
            case EnermyAIState.AI_Born:
                born();
                break;
            case EnermyAIState.AI_Idle:
                idle();
                break;
            case EnermyAIState.AI_Patrol:
                patrol();
                break;
            case EnermyAIState.AI_FightThink:
                fightThink();
                break;
            case EnermyAIState.AI_ChaseEntity:
                chase();
                break;
            case EnermyAIState.AI_CastSpell:
                attack();
                break;
            case EnermyAIState.AI_Reset:
                homing();
                break;
        }
    }

    public void stopAI()
    {
        isAIRuning = false;
        vStartState = EnermyAIState.AI_FightThink;
        if(m_navMeshAgent.enabled == true)
        {
            m_navMeshAgent.ResetPath();
            m_navMeshAgent.enabled = false;  
        }          
        m_animator.SetInteger("runInt", 0);
    }

    public void startAI()
    {
        isAIRuning = true;
        m_navMeshAgent.enabled = true;
    }

    public void onReceiveDamage(AvatarComponent attacker)
    {
        if(attacker)
        {
            target = attacker;
        }
        vStartState = EnermyAIState.AI_FightThink;
    }

    public void onDead(CDeadType deadType)
    {
        isAIRuning = false;
        switch (deadType)
        {
            case CDeadType.None:
                break;
            case CDeadType.Normal:
                m_animator.SetBool("die", true);
                StartCoroutine(DelayDestroy(3.0f));
                break;
            case CDeadType.Dissolution:
                m_animator.SetBool("die", true);
                own.effectManager.AddModelEffect("DissolveEffect");
                StartCoroutine(DelayDestroy(6.0f));
                break;
            case CDeadType.Cutting:
                own.HideModel();
                GameObject obj = Instantiate(cuttingDeathObject, transform.position, transform.rotation) as GameObject;
                StartCoroutine(DelayDestroy(6.0f));
                break;
            case CDeadType.Fracture:
                own.HideModel();
                own.effectManager.AddModelEffect("FractureEffect");
                StartCoroutine(DelayDestroy(6.0f));
                break;
            default:
                break;
        }
    }

    /// <summary>
    /// 延迟销毁gameObject
    /// </summary>
    /// <param name="delay"></param>
    /// <returns></returns>
    private IEnumerator DelayDestroy(float delay)
    {
        yield return new WaitForSeconds(delay);
        own.Destroy();
    }

    void born()
    {
        if (vStartState != vLostState)
        {
            m_animator.SetInteger("runInt", 0);
            vLostState = vStartState;
        }

        if (!bornFlag)
        {
            bornFlag = true;
            if (own)
            {
                if (bornType == BornType.Born_Dissolve)
                {
                    own.effectManager.AddModelEffect("InverseDissolveEffect");
                }
            }
        }

        if (Time.time - lastTime > bornTime)
        {
            vStartState = EnermyAIState.AI_Idle;
        }
    }

    void idle()
    {
        if (vStartState != vLostState)
        {
            m_animator.SetInteger("runInt", 0);
            vLostState = vStartState;
        }

        calcRandomWalkPosition();

        if (Time.time - LastThinkTime > idleStopTime)
        {
            //开始思考  
            LastThinkTime = Time.time;
            vStartState = EnermyAIState.AI_Patrol;
        }
    }

    void patrol()
    {
        if (vStartState != vLostState)
        {
            m_animator.SetInteger("runInt", 5);
            vLostState = vStartState;
            m_navMeshAgent.speed = idleSpeed;
            m_navMeshAgent.updateRotation = false;
            transform.LookAt(new Vector3(Dis.x, transform.position.y, Dis.z));
            m_navMeshAgent.destination = Dis;              
        }

        if (Vector3.Distance(Dis, transform.position) < 0.4f)
        {
            m_navMeshAgent.ResetPath();
            vStartState = EnermyAIState.AI_Idle;
        }

        List<AvatarComponent> objs = AvatarComponent.AvatarInRange(alertRadius, own, Vector3.zero);

        foreach (AvatarComponent obj in objs)
        {
            if (obj.status != eEntityStatus.Death && (own.CheckRelationship(obj) == eTargetRelationship.HostilePlayers || own.CheckRelationship(obj) == eTargetRelationship.HostileMonster))
                target = obj;
        }

        if (!target)
            return;

        if (Vector3.Distance(transform.position, target.transform.position) < alertRadius)
        {
            vStartState = EnermyAIState.AI_FightThink;
        }
    }

    void fightThink()
    {
        if (target.status == eEntityStatus.Death)
        {
            target = null;
            vStartState = EnermyAIState.AI_Reset;
            return;
        }

        if (vStartState != vLostState)
        {
            randomValue = Random.value;
            if (randomValue < attackActive) //根据攻击积极性判断是徘徊还是攻击
            {
                attackFlag = true;
            }
            else
            {
                attackFlag = false;
            }

            m_animator.SetBool("fight", true);
            vLostState = vStartState;          
        }

        //只要离出生点太远了，就要脱离战斗
        if (Vector3.Distance(srcPoint, transform.position) > chaseRadius &&
            Vector3.Distance(transform.position, target.transform.position) > alertRadius)
        {
            vStartState = EnermyAIState.AI_Reset;
            return;
        }

        currentSpell = SelectSpell();
        if (currentSpell != null && attackFlag)
        {
            vStartState = EnermyAIState.AI_CastSpell;
            return;
        }
        vStartState = EnermyAIState.AI_ChaseEntity;               
    }

    void chase()
    {
        if (vStartState != vLostState)
        {
            vLostState = vStartState;
            _chaseEntity();
            m_navMeshAgent.enabled = true;       
            m_navMeshAgent.ResetPath();
            m_navMeshAgent.updateRotation = false;
            m_navMeshAgent.speed = targetSpeed;
        }

        if (m_navMeshAgent.velocity == Vector3.zero)
        {
            Vector3 dir1 = transform.position;
            dir1.y = 0.0f;
            Vector3 dir2 = target.transform.position;
            dir2.y = 0.0f;
            Vector3 dir = dir2 - dir1;
            Vector3.Normalize(dir);
            transform.forward = dir;

            UnityEngine.AI.NavMeshHit hit;
            if (UnityEngine.AI.NavMesh.SamplePosition(targetPosition, out hit, 5f, UnityEngine.AI.NavMesh.AllAreas))
            {
                m_navMeshAgent.enabled = true;
                targetPosition = hit.position;
                ActionChange();
                m_navMeshAgent.destination = targetPosition;
            }
            else
            {
                _chaseEntity();
                chase();
            }
        }

        float disposition = Vector2.Distance(new Vector2(targetPosition.x, targetPosition.z), new Vector2(transform.position.x, transform.position.z));
        if (disposition < 0.5f)
        {
            accumulateTime += Time.deltaTime;
            if (m_navMeshAgent.enabled)
            {
                m_animator.SetInteger("runInt", 0);
                m_navMeshAgent.ResetPath();
                m_navMeshAgent.enabled = false;
            }
            
            if (accumulateTime > hoverWaitTime)
            {
                accumulateTime = 0.0f;
                vStartState = EnermyAIState.AI_FightThink;
            }
                
        }
    }

    void attack()
    {
        if (vStartState != vLostState)
        {
            vLostState = vStartState;           
        }

        if (currentSpell == null)
        {
            accumulateTime += Time.deltaTime;
            if (accumulateTime > attackWaitTime)
            {
                vStartState = EnermyAIState.AI_FightThink;
            }
            return;
        }
        
        if (currentSpell.distance < Vector3.Distance(transform.position, target.transform.position) && isAttack)
        {
            m_animator.SetInteger("runInt", 1);
            transform.LookAt(target.transform.position);
            m_navMeshAgent.enabled = true;
            m_navMeshAgent.ResetPath();
            m_navMeshAgent.updateRotation = false;
            m_navMeshAgent.speed = hoverWalkSpeed;
            m_navMeshAgent.destination = target.transform.position;
        }
        else
        {
            if (m_navMeshAgent.enabled)
            {
                m_navMeshAgent.ResetPath();
                m_navMeshAgent.enabled = false;
                m_animator.SetInteger("runInt", 0);
            }
            castSpell();
        }

        bool isCastFlag = SPELL.Spell.Locked(gameObject);
        if(!isCastFlag && !isAttack)
        {
            currentSpell = null;
            isAttack = true;
            //m_animator.SetInteger("runInt", 0);
            //vStartState = EnermyAIState.AI_FightThink;
        }        
    }

    void homing()
    {
        if (vStartState != vLostState)
        {
            m_animator.SetInteger("runInt", 1);
            vLostState = vStartState;
            transform.LookAt(srcPoint);
            m_navMeshAgent.enabled = true;
            m_navMeshAgent.ResetPath();
            m_navMeshAgent.updateRotation = false;
            m_navMeshAgent.speed = hoverWalkSpeed;
            m_navMeshAgent.destination = srcPoint;
        }

        if (Vector2.Distance(new Vector2(srcPoint.x, srcPoint.z), new Vector2(transform.position.x, transform.position.z)) < 1)
        {
            vStartState = EnermyAIState.AI_Idle;
        }
    }
    
    void castSpell()
    {
        if(isAttack)
        {
            isAttack = false;          
            m_navMeshAgent.updateRotation = false;
            transform.LookAt(target.transform.position);
            CastSpell(currentSpell);
        }
    }

    void calcRandomWalkPosition()
    {
        Vector3 center = srcPoint;
        float r = Random.Range(1, 3);
        float b = 360.0f * Random.value;
        float x = r * Mathf.Cos(b);
        float y = r * Mathf.Sin(b);
        Dis = new Vector3(center.x + x, transform.position.y, center.z + y);
    }

    Vector3 retreatCalcHoverPosition(Vector3 distance, Vector3 center)
    {
        float len = distance.magnitude;
        float half = (hoverRadiusMin + hoverRadiusMax) / 2;
        float l = 0;
        if (len <= half)
            l = hoverRadiusMax;
        else
            l = hoverRadiusMin;

        Vector3 dispos = distance.normalized * l + center;
        return dispos;
    }

    Vector3 sectorHoverPosition()
    {
        float startValue = 90 - wanderAngle * 0.5f;
        float endValue = startValue + wanderAngle;
        float startAngle = (startValue - target.transform.eulerAngles.y) * Mathf.PI / 180;
        float endAngle = (endValue - target.transform.eulerAngles.y) * Mathf.PI / 180;
        float randAngle = startAngle + Random.value * (endAngle - startAngle);
        float randRadius = Random.Range(hoverRadiusMin, hoverRadiusMax);
        float randX = target.transform.position.x + randRadius * Mathf.Cos(randAngle);
        float randY = target.transform.position.z + randRadius * Mathf.Sin(randAngle);
        return new Vector3(randX, 0, randY);
    }

    void _chaseEntity()
    {
        float dis = Vector3.Distance(transform.position, target.transform.position);
        if (hoverRadiusMax + 0.1f < dis)		
        {
            Vector3 dir = transform.position - target.transform.position;
            targetPosition = target.transform.position + dir.normalized * hoverRadiusMax;
            targetSpeed = hoverWalkSpeed;
        }
		else
        {
            if (Random.value > 0.5f)
            {
                Vector3 distance = transform.position - target.transform.position;
                Vector3 pos = retreatCalcHoverPosition(distance, target.transform.position);
                //float dis1 = Vector3.Distance(transform.position, pos);
                //float dis2 = Vector3.Distance(transform.position, target.transform.position);
               // if (dis1 < dis2)
                   // speed = hoverSpeed;

                targetPosition = pos;
                targetSpeed = hoverWalkSpeed;
            }
            else
            {
                Vector3 pos = sectorHoverPosition();
                targetPosition = pos;
                targetSpeed = hoverWalkSpeed;
            }
        }
    }

    Vector3 rotalteXZ(Vector3 v, float angle)
    {
        //向量按照angle度数旋转
	    //argle是弧度
	    float x = v[0]*Mathf.Cos(angle) + 0 + (-v[2]*Mathf.Sin (angle));
	    float y = v[1];
	    float z = v[0]*Mathf.Sin (angle) + 0 + v[2]*Mathf.Cos(angle);
        return new Vector3(x, y, z);
    }

    float AngleEx(Vector3 position)
    {
        Vector3 a = transform.forward;
        Vector3 b = position - transform.position;
        a.y = b.y = 0.0f;

        float angle = Vector3.Angle(a, b);
        Vector3 tempDir = Vector3.Cross(a, b);
        if (tempDir.y < 0)
            angle = -angle;
        return angle;
    }

    //根据不同速度播放动作，其中actionFlag = 1表示run, 2为left,3为right,4为back，5为walk
    void ActionChange()
    {
        float angle = AngleEx(targetPosition);
        if (angle >= -45 && angle <= 45)
        {
            m_animator.SetInteger("runInt", 1);
        }
        else if (angle >= -135 && angle < -45)
        {
            m_animator.SetInteger("runInt", 2);
        }
        else if (angle > 45 && angle <= 135)
        {
            m_animator.SetInteger("runInt", 3);
        }
        else
        {
            m_animator.SetInteger("runInt", 4);
        } 
    }

    /// <summary>
    /// 技能列表里选择一个可以释放的技能
    /// </summary>
    /// <returns></returns>
    private SPELL.Spell SelectSpell()
    {
        SPELL.SpellTargetData targetData = new SPELL.SpellTargetData();
        foreach(int id in skillList)
        {
            var spell = SpellLoader.instance.GetSpell(id);
            if (spell == null)
                continue;
            if (spell.CanStart(own, targetData) == SPELL.SpellStatus.OK)
                return spell;
        }
        return null;

    }

    /// <summary>
    /// 释放技能
    /// </summary>
    /// <param name="spell"></param>
    private void CastSpell(SPELL.Spell spell)
    {
        SPELL.SpellTargetData targetData = new SPELL.SpellTargetData();
        spell.Cast(own, targetData);        
    }
}