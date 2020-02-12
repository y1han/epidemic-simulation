# epidemic-simulation
  A python epidemic simultation programme  

#### 图表信息:  
	Total 总存活人数  
	Susceptible 未感染  
	Contagious 传染源  
	Exposed 潜伏期(黄色)  
	Illed 总体得病(红色，仅包含确诊和住院,不包含潜伏期)  
	Infective 确诊(左图中红色)  
	Hospitalized 住院隔离(医院中红色)  
	Recovered 免疫期(绿色)
	Te 实际平均潜伏时间
	Ti 实际平均传染时间
	Tg 实际平均入院时间(约等于Ti+Te,由于存在死亡，因此有些许不同)  
	R0 基本传染数(Basic reproduction number) 定义为一个感染到某种传染病的人，会把疾病传染给其他多少个人的平均数 R0 = k*b*D --Lipsitch M，Cohen T, Cooper B, et al. TransmissionDynamics and Control of Severe Acute Respiratory Syndrome. Science, 2003,300(5627): 1966-1970.

#### 可用参数:  
	ORIGINAL_COUNT 初始感染数量  
	BROAD_RATE  传播率  
	PROTECTION_RATE 保护措施增长率(连续)(影响BROAD_RATE, DEATH_RATE, u)  
	SHADOW_TIME 平均潜伏时间  
	HOSPITAL_RECEIVE_TIME 平均医院收治时间  
	CURE_TIME 平均治疗时间  
	IMMUNED_TIME 平均免疫期时间
	DEATH_RATE 每日死亡概率  
	BED_COUNT 医院床位  
	SAFETY_DIST 安全距离  
	FLUCTUATION 各参数与平均值之间的波动
	u 流动意向  
	PERSON_COUNT 城市内人数  
	can_exposed_infect 潜伏期能否感染他人
	recovered_included 是否有免疫期
	mode ‘l'或者'line'运行时右侧为折线图,否则为柱状图

图示:
![image](https://github.com/y1han/virus-simulation/raw/master/images/desc.jpeg)

由 https://github.com/KikiLetGo/VirusBroadcast 启发进行的python复刻，并进行了一些改动  
	运行main.py即可
