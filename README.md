# virus-simulation
  A python virus simultation programme  
  
由 https://github.com/KikiLetGo/VirusBroadcast 启发进行的python复刻，并进行了一些改动  
	运行main.py即可

#### 图表信息:  
	Total 总存活人数  
	Susceptible 未感染  
	Contagious 传染源  
	Incubated 潜伏期  
	Illed 总体得病(仅包含确诊,不包含潜伏期)  
	Exposed 确诊  
	Hospitalized 住院隔离  
	Recovered 免疫期

#### 可用参数:  
	ORIGINAL_COUNT 初始感染数量  
	BROAD_RATE  传播率  
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
![image](https://github.com/y1han/virus-simulation/raw/master/images/desc_line.jpeg)
