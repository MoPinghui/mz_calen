
import datetime 

"""
@syntax:
# CLASS1
## ITEM1
TIMES_OF_ITEM1
## ITEM2
TIMES_OF_ITEM1

# DAYLY
## ITEM1
## ITEM2
## ITEM3
@syntax of time:
1. 一个时间点 2022-04-12 #2022年4月12号的13时30分
2. 一个时间段 2022-04-12 > 2023-05-14 #2022年4月12号到2023年5月12号
3. 时间段中选择多个时间点 2022-04-12 > 2023-05-14 > C1 | W2 | A3 #2022年4月12号到2023年5月12号中，每隔1天，或每周2，或2022-04-15号
4. 未达时间 对于在后面的时间，只在code时显示
@update of time
对于过去的时间，时间点和事项已经确定
对于没有完成的事件，需要更新规则继续保存
"""

INFTIME_ST = "1000-1-1" # 无限往前得时间
INFTIME_ED = "3000-1-1" # 无限时间，即未来很长的时间
INFTIME_TP = "none" # 无限时间，即未来很长的时间
FORMAT_TIME = "%Y-%m-%d"
MAX_ITEM = 24
MAX_DATE_BEFORE = 3
MAX_DATE_AFTER = 4
MAX_DATE = MAX_DATE_BEFORE+1+MAX_DATE_AFTER
MAX_CCLASS = 8

TMP_ITEM = \
"""
# 类别名
## 项目名
* 这是注释
* 下面是时间定义
* 1.定义时间点: 2022-04-16
* 2.定义时间段: 2022-04-16 > 2022-05-16
* 3.定义多时间点: 2022-04-16 > 2022-05-16 > w3,m2,c10,a8
*  2022-04-16号到2022-05-16之间
*  每周三(w3)，或是每月的2号(m2),
*  或是从2022-04-16数起的每10天(c10)
*  或是从2022-04-16数起的第8天(a8)
*  将会被标注为执行此事件的时间点
2022-04-16
"""

class CalendarTime():
    def __init__(self):
        self.time = datetime.date(2000, 1, 1)
    
    def init_by_str(self, strTime=""):
        self.set_time(strTime)

    def init_by_value(self, year, month, day):
        self.time = datetime.date(year, month, day)
        self.update_time()
    
    def update_time(self):
        self.year = self.time.year
        self.month = self.time.month 
        self.day = self.time.day

    def set_time(self, strTime):
        st = self.format_strTime(strTime)
        time = datetime.datetime.strptime(st, FORMAT_TIME)
        self.time = datetime.date(time.year, time.month, time.day)
        self.update_time()
    
    def get_time(self):
        return self.time.strftime(FORMAT_TIME)

    def format_strTime(self, strTime):
        # year-month-day
        ymd = strTime.split('-')
        ymd.append('1')
        ymd.append('1')
        ymd.append('1')
        return '-'.join(ymd[0:3])

class CalendarRule():
    def __init__(self):
        self.tst = CalendarTime()
        self.ted = CalendarTime()
        self.tps = []
        self.rcycs = []
        self.rmons = []
        self.rweks = []
        self.radds = []
        self.ranys = []

    def init_by_str(self, strRule):
        self.tst, self.ted, self.tps = self.str2rule(strRule)
        self.rcycs, self.rmons, self.rweks, self.radds, self.ranys = self.tps2rule(self.tps)
    
    def init_by_value(self, tst, ted, tps):
        self.tst = tst 
        self.ted = ted 
        self.tps = tps 
        self.rcycs, self.rmons, self.rweks, self.radds, self.ranys = self.tps2rule(self.tps)
    
    def tps2rule(self, tps):
        rcycs = [int(p.lstrip('c')) for p in tps if p.startswith('c')] # 周期性的c天
        rmons = [int(p.lstrip('m')) for p in tps if p.startswith('m')] # 每个月的第m天
        rweks = [int(p.lstrip('w')) for p in tps if p.startswith('w')] # 每周周w
        radds = [int(p.lstrip('a')) for p in tps if p.startswith('a')] # 从起始天开始的第a天
        ranys = [0 for p in tps if p.startswith('n')]
        return rcycs, rmons, rweks, radds, ranys
    
    def str2rule(self, strRule):
        #
        strRule = strRule.replace(' ', '')
        pars = strRule.split('>')
        pars = [p for p in pars if p != '']
        #
        if len(pars) == 0:
            print("ERROR: str2rule")
            print(strRule)
            exit(1)
        elif len(pars) == 1:
            tst = pars[0]
            ted = tst
            tps = 'n'
        elif len(pars)  == 2:
            tst = pars[0]
            ted = pars[1] 
            tps = 'n'
        elif len(pars) == 3:
            tst = pars[0]
            ted = pars[1]
            tps = pars[2]
        tps = tps.split(',')
        tps = [p for p in tps if p != '']
        #
        # print(tst, ted, tps)
        ttst = CalendarTime()
        ttst.init_by_str(tst)
        tted = CalendarTime()
        tted.init_by_str(ted)
        return ttst, tted, tps
    
    def judge_in_rule(self, dates):
        nd = len(dates)
        bs = [False for ii in range(nd)]
        for ii in range(nd):
            if (self.ted.time >= dates[ii].time) and \
                (dates[ii].time >= self.tst.time):
                bs[ii] = True
        #
        sbs = [True for bsi in bs if bsi]
        if len(sbs) == 0: return bs 
        #
        bs1 = self.judge_in_rule_rcycs(dates)
        #
        bs2 = self.judge_in_rule_rmons(dates)
        #
        bs3 = self.judge_in_rule_rweks(dates)
        #
        bs4 = self.judge_in_rule_radds(dates)
        #
        bs5 = self.judge_in_rule_ranys(dates)
        #
        bs_ = []
        for ii in range(nd):
            bsi = bs[ii] and (bs1[ii] or bs2[ii] or bs3[ii] or bs4[ii] or bs5[ii])
            bs_.append(bsi)
        return bs_

    def judge_in_rule_rcycs(self, dates):
        #
        nd = len(dates)
        bs = [False for ii in range(nd)]
        for ii in range(nd):
            d = dates[ii].time - self.tst.time
            d = d.days
            if d > 0:
                for cc in range(len(self.rcycs)):
                    if (d % self.rcycs[cc]) == 0:
                        bs[ii] = True
        return bs

    def judge_in_rule_rmons(self, dates):
        #
        nr = len(self.rmons)
        mp = [False for ii in range(31)]
        for ii in range(nr):
            m = self.rmons[ii]
            mp[m-1] = True
        #
        nd = len(dates)
        bs = [False for ii in range(nd)]
        for ii in range(nd):
            d = dates[ii].time.day
            bs[ii] = mp[d-1]
        return bs
    
    def judge_in_rule_rweks(self, dates):
        #
        nr = len(self.rweks)
        wp = [False for ii in range(7)]
        for ii in range(nr):
            w = self.rweks[ii]
            wp[w-1] = True
        #
        nd = len(dates)
        bs = [False for ii in range(nd)]
        for ii in range(nd):
            w = dates[ii].time.weekday()
            bs[ii] = wp[w]
        return bs
    
    def judge_in_rule_radds(self, dates):
        #
        nd = len(dates)
        bs = [False for ii in range(nd)]
        for ii in range(nd):
            d = dates[ii].time - self.tst.time
            d = d.days
            if d > 0:
                for aa in range(len(self.radds)):
                    if (d == self.radds[aa]):
                        bs[ii] = True
        return bs

    def judge_in_rule_ranys(self, dates):
        #
        nd = len(dates)
        if len(self.ranys) > 0:
            bs = [True for ii in range(nd)]
        else:
            bs = [False for ii in range(nd)]
        return bs
    
    def to_string(self, enter="\n"):
        tst = self.tst.time.strftime(FORMAT_TIME) 
        ted = self.ted.time.strftime(FORMAT_TIME)
        tpt = ",".join(self.tps)
        if tst == ted:
            return tst + enter 
        elif tpt == "n":
            return tst + " > " + ted + enter 
        else:
            return tst + " > " + ted + " > " + tpt + enter 

class CalendarItem():
    def __init__(self, order, index, item, annots, rules, useful=True):
        """:
        序号， 索引号，项目标号，注释，时间规则
        """
        self.order = order
        self.index = index
        self.item = item
        self.annots = annots
        self.rules = []
        self.useful = True

        for ii in range(len(rules)):
            rule = CalendarRule()
            rule.init_by_str(rules[ii])
            self.rules.append(rule)
    
    def judge_in_rule(self, dates):
        # print("#", self.item)
        nr = len(self.rules)
        nd = len(dates)
        bs = [False for ii in range(nd)]
        for ii in range(nr):
            b = self.rules[ii].judge_in_rule(dates)
            bs = [(bs[jj] or b[jj]) for jj in range(nd)] 
        return bs 
    
    def to_string(self, enter="\n"):
        s = "## " + self.item + enter
        for ii in range(len(self.rules)):
            s += "".join(["* " + line + enter for line in self.annots]) 
            s += self.rules[ii].to_string(enter) + enter
        return s 

class CalendarClass():
    def __init__(self, order, index, name, context):
        self.order = order
        self.index = index 
        self.name = name 
        self.context = context 
        self.items = self.extract_items(context)
        self.idxs = []
        self.bs = []
    
    def extract_items(self, context):
        context = [line.replace('\n', '').replace(' ','').replace('=','') for line in context]
        context = [p for p in context if p != '']
        #
        st = 0
        ct = 0 
        items = []
        for ii in range(len(context)):
            line = context[ii]
            if line.startswith('##'):
                if ct == 0:
                    item = line.lstrip('##')
                    st = ii
                    ct += 1
                else:
                    rules = context[st+1:ii]
                    annots = [p.lstrip("*") for p in rules if p.startswith('*')] 
                    rules = [p for p in rules if not p.startswith('*')] 
                    items.append(CalendarItem(ct-1, ct-1, item, annots, rules, True))
                    item = line.lstrip('##')
                    st = ii 
                    ct += 1
                continue 
        #
        rules = context[st+1:]
        annots = [p.lstrip("*") for p in rules if p.startswith('*')] 
        rules = [p for p in rules if not p.startswith('*')] 
        items.append(CalendarItem(ct-1, ct-1, item, annots, rules, True))
        return items 
    
    def judge_in_rule(self, dates):
        self.idxs = [] # 可视化的rule
        ni = len(self.items)
        nd = len(dates)
        bs = [[False for jj in range(MAX_ITEM)] for ii in range(nd)]
        ct = 0
        for ii in range(ni):
            bsi = self.items[ii].judge_in_rule(dates)
            sbsi = [True for bsii in bsi if bsii]
            if len(sbsi) > 0:
                self.idxs.append(ii) 
                for jj in range(nd):
                    bs[jj][ct] = bsi[jj]
                ct += 1
        self.bs = bs
        return self.bs
    
    def judge_in_date(self, dates):
        self.idxs = []
        ni = len(self.items)
        nd = len(dates)
        bs = [[False for jj in range(MAX_ITEM)] for ii in range(nd)]
        for ii in range(nd):
            sdate = dates[ii].get_time() 
            name = "DAYLY_"+sdate 
            if name == self.name:
                bs[ii] = [True for jj in range(MAX_ITEM)]
                self.idxs = [jj for jj in range(ni)]
        self.bs = bs 
        return self.bs 
    
    def idx2string_item(self, idx, enter="\n"):
        bs = self.bs[idx]
        #
        p = False
        ss = []
        for ii in range(len(self.idxs)):
            if bs[ii] > 0:
                p = True 
                idxi = self.idxs[ii]
                s = self.name + ":" + self.items[idxi].item
                ss.append(s)
        return p, enter.join(ss)

    def idx2string_date(self, idx, enter="\n"):
        bs = self.bs[idx]
        #
        p = False
        ss = []
        for ii in range(len(self.idxs)):
            if bs[ii] > 0:
                p = True 
                idxi = self.idxs[ii]
                s = "DAYLY:" + self.items[idxi].item
                ss.append(s)
        return p, enter.join(ss)
    
    def to_string(self, enter="\n"):
        ni = len(self.items)
        s = "# "+self.name
        s1 = ""
        for ii in range(ni):
            s1 += self.items[ii].to_string(enter)
        s = s + enter + s1
        return s 

    def find_key(self, key):
        keys = key.split('&')
        p = True 
        for key in keys:
            p1 = key in self.name 
            p2 = len([True for c in self.context if (key in c)]) > 0
            if not(p1 or p2):
                p = False 
                break 
        return p

class CalendarClasses():
    def __init__(self):
        self.idxs = []
        self.data = []  

    def judge_in_rule(self, dates):
        idxs = []
        ct = 0
        for ii in range(len(self.data)):
            cclass = self.data[ii]
            bs = cclass.judge_in_rule(dates) #date, item
            sbs = [True for bsi in bs if bsi]
            if len(sbs) > 0:
                idxs.append(ii) 
                ct += 1
        self.idxs = idxs 
        return idxs
    
    def judge_in_date(self, dates):
        idxs = []
        for ii in range(len(dates)):
            sdate = dates[ii].get_time()
            name = "DAYLY_"+sdate 
            idx = -1 
            for jj in range(len(self.data)):
                if self.data[jj].name == name:
                    idx = jj 
                    break 
            #
            if idx == -1:
                idx = len(self.data)
                self.data.append(CalendarClass(idx, idx, name, ["## NOTHING", sdate]))
            #
            self.data[idx].judge_in_date(dates)
            idxs.append(idx)
        self.idxs = idxs 
        return idxs 
    
    def add_one(self, name, context):
        idx = len(self.data)
        new_cc = CalendarClass(idx, idx, name, context)
        self.data.append(new_cc)
    
    def remove_one(self, idx):
        self.data.pop(idx)
    
    def update_one(self, idx, name, context):
        self.data[idx] = CalendarClass(idx, idx, name, context)
    
    def split_name_context(self, lines):
        lines = [line.replace(' ', '') for line in lines]
        lines = [line for line in lines if line != '']
        #
        for ii in range(len(lines)):
            line = lines[ii]
            if line.startswith("#") and (not line.startswith("##")):
                name = line.lstrip('#')
                context = lines[ii+1:]
                break 
        #
        return name, context 
    
    def to_string(self, idx=-1, enter="\n"):
        return self.data[idx].to_string(enter)
    
# FILE_IO
# ==========================================================
    
    def read(self, fntxt="", fnnpy=""):
        if fntxt != "":
            self.data = self.read_txt(fntxt)
    
    def read_txt(self, fn):
        lines = open(fn, 'r', encoding='utf-8').readlines()
        lines = [line.replace('\n', '').replace(' ','') for line in lines]
        lines = [line for line in lines if line != '']
        #
        data = []
        ct = 0
        st = 0
        for ii in range(len(lines)):
            line = lines[ii]
            if line.startswith("#"):
                if not line.startswith("##"):
                    if ct == 0:
                        name = line.lstrip("#")
                        st = ii 
                        ct += 1
                    else:
                        context = lines[st+1:ii]
                        # print(name)
                        # print(context)
                        data.append(CalendarClass(ct-1, ct-1, name, context))
                        name = line.lstrip("#")
                        st = ii 
                        ct += 1
        #
        context = lines[st+1:]
        data.append(CalendarClass(ct-1, ct-1, name, context))
        return data
    
    def save(self, fntxt="", fnnpy=""):
        if fntxt != "":
            self.save_txt(fntxt) 

    def save_txt(self, fn):
        lines = []
        for ii in range(len(self.data)):
            cclass = self.data[ii]
            s = cclass.to_string()
            lines.append(s) 
        #
        open(fn, 'w', encoding="utf-8").writelines(lines)
    
    def find_key(self, key):
        idx = []
        for ii in range(len(self.data)):
            if self.data[ii].find_key(key):
                idx.append(ii)
        return idx 
    
