import sys
import datetime 
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

from mcalendar import *
from mdisplay import *
from mlayout import *
from mstyle import * 

class LoginWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUi()
    
    def initUi(self):
        self.idx_date = -1
        self.idx_item = -1
        self.idxs_date = [] 
        self.idxs_item = [] 
        #
        self.disp = Display()
        #
        self.cal_date = CalendarClasses()
        self.cal_date.read("date.md")
        self.cal_item = CalendarClasses()
        self.cal_item.read("item.md")
        #
        self.build_ui()
        self.init_ui()
        self.setWindowTitle("hh love mm 日历")
        self.setWindowIcon(QIcon("icon.ico"))
    
# Layout
# ==========================================================

    def build_ui(self):
        # self.build_mark()
        self.setWindowTitle('父控件')
        self.move(400,250)
        self.layout = Layout()
        # 布局
        self.layout.layouts['#root'] = LayoutElement('n', [0,0,0,0])
        self.layout.wsplit('#root', '#item #buttons'.split(), [600, 400])
        self.layout.hsplit('#item', 'te_item lb_msg'.split(), [775, 25])
        self.layout.hsplit('#buttons', 'calenda te_find #bts_edit #bts_date #bts_item'.split(), [300, 50, 50, 100, 200])
        self.layout.wsplit('#bts_edit', 'bt_item bt_find bt_new bt_save bt_open bt_del'.split(), [], 400)
        self.layout.array('#bts_date', 'bt_date', 100, 2, 400, 4)
        self.layout.array('#bts_item', 'bt_item', 300, 12, 400, 2)
        # 控件
        ## 
        self.te_item = QTextEdit('', self) 
        self.lb_msg = QLabel('', self)
        self.calenda = QCalendarWidget(self)
        self.te_find = QTextEdit('', self)
        ## bts_edit
        self.bt_item = QPushButton('', self)
        self.bt_find = QPushButton('', self)
        self.bt_new = QPushButton('', self)
        self.bt_save = QPushButton('', self)
        self.bt_open = QPushButton('', self)
        self.bt_del = QPushButton('', self)
        ## bts_date
        self.bt_dates = [QPushButton('', self) for ii in range(MAX_DATE)]
        ## bts_item
        self.bt_items = [QPushButton('', self) for ii in range(MAX_ITEM)]
        # 建立映射
        self.layout.set_instance('te_item', self.te_item)
        self.layout.set_instance('lb_msg', self.lb_msg)
        self.layout.set_instance('calenda', self.calenda)
        self.layout.set_instance('te_find', self.te_find)
        ## bts_edit
        self.layout.set_instance('bt_item', self.bt_item)
        self.layout.set_instance('bt_find', self.bt_find)
        self.layout.set_instance('bt_new', self.bt_new)
        self.layout.set_instance('bt_save', self.bt_save)
        self.layout.set_instance('bt_open', self.bt_open)
        self.layout.set_instance('bt_del', self.bt_del)
        ## bts_date
        for ii in range(MAX_DATE): self.layout.set_instance('bt_date'+str(ii), self.bt_dates[ii])
        ## bts_item
        for ii in range(MAX_ITEM): self.layout.set_instance('bt_item'+str(ii), self.bt_items[ii])
        # 调整布局
        self.layout.setGeometry()


# Init
# ==========================================================

    def init_ui(self):
        #
        style1 = Style()
        style1.set_color("#000000", "#FFFFFF")
        style1.set_font("20px", "Microsoft YaHei")
        self.style1 = style1
        #
        style2 = Style()
        style2.set_color("#000000", "#F0F0F0")
        style2.set_font("20px", "Microsoft YaHei")
        self.style2 = style2
        #
        style3 = Style()
        style3.set_color("#000000", "#D0D0D0")
        style3.set_font("20px", "Microsoft YaHei")
        self.style3 = style3
        # set stype
        ##
        self.te_item.setStyleSheet(style1.toString("QTextEdit"))
        self.lb_msg.setStyleSheet(style1.toString("QLabel"))
        self.te_find.setStyleSheet(style2.toString("QTextEdit"))
        ## bts_edit
        self.bt_item.setStyleSheet(style1.toString("QPushButton"))
        self.bt_find.setStyleSheet(style1.toString("QPushButton"))
        self.bt_new .setStyleSheet(style1.toString("QPushButton"))
        self.bt_save.setStyleSheet(style1.toString("QPushButton"))
        self.bt_open.setStyleSheet(style1.toString("QPushButton"))
        self.bt_del .setStyleSheet(style1.toString("QPushButton"))
        ## bts_date
        for ii in range(MAX_DATE):
            self.bt_dates[ii].setStyleSheet(style2.toString("QPushButton"))
        ## bts_item
        for ii in range(MAX_ITEM):
            self.bt_items[ii].setStyleSheet(style3.toString("QPushButton"))
        # set text
        ##
        self.te_item.setText('')
        self.lb_msg.setText('')
        self.te_find.setText('')
        ## bts_edit
        self.bt_item.setText('⚪')
        self.bt_find.setText('find')
        self.bt_new.setText('new')
        self.bt_save.setText('save')
        self.bt_open.setText('open')
        self.bt_del.setText('del')
        ## bts_date
        for ii in range(MAX_DATE):
            self.bt_dates[ii].setText('--')
        ## bts_item
        for ii in range(MAX_ITEM):
            self.bt_items[ii].setText('--')
        # set innitial display
        self.update_date(self.calenda.selectedDate())
        # set event
        self.bt_item.clicked.connect(self.cmd_item)
        self.bt_find.clicked.connect(self.cmd_find)
        self.bt_new.clicked.connect(self.cmd_new)
        self.bt_save.clicked.connect(self.cmd_save)
        self.bt_open.clicked.connect(self.cmd_open)
        self.bt_del.clicked.connect(self.cmd_delete)
        #
        for ii in range(MAX_DATE):
            self.bt_dates[ii].clicked.connect(lambda : self.cmd_show_item_detial(self.sender().text(), "none"))
        for ii in range(MAX_ITEM):
            self.bt_items[ii].clicked.connect(lambda : self.cmd_show_item_detial("none", self.sender().text()))
        self.calenda.clicked.connect(self.update_date)

# Event
# ==========================================================

    def update_message(self, msg):
        self.lb_msg.setText(msg)

    def get_range_date(self, sdate, nbefore, nafter):
        """: 获取sdate表示的日期周围的时间
        """
        nt = CalendarTime()
        nt.init_by_str(sdate)
        dates = []
        for ii in range(-nbefore, nafter+1):
            ddate = datetime.timedelta(ii) 
            ddate = nt.time + ddate
            tdate = CalendarTime()
            tdate.init_by_value(ddate.year, ddate.month, ddate.day)
            dates.append(tdate)
        return dates

    def update_date(self, date):
        self.sdate = date.toString('yyyy-MM-dd')
        self.dates = self.get_range_date(self.sdate, MAX_DATE_BEFORE, MAX_DATE_AFTER)
        self.state_reset() 
        self.idxs_date = self.cal_date.judge_in_date(self.dates)
        self.idxs_item = self.cal_item.judge_in_rule(self.dates)
        self.disp.disp_plan(self.te_item, self.cal_date, self.cal_item, self.dates)
        self.update_button()
        self.update_message("显示近期计划："+self.sdate)
    
    def update_button(self):
        """: update_date之后，更新button的颜色和字体
        """
        for ii in range(MAX_DATE):
            s="%d-%02d"%(self.dates[ii].time.month, self.dates[ii].time.day)
            self.bt_dates[ii].setText(s) 
        
        for ii in range(MAX_ITEM):
            if ii < len(self.idxs_item):
                idx = self.idxs_item[ii]
                s = self.cal_item.data[idx].name 
                self.bt_items[ii].setText(s)
            else:
                self.bt_items[ii].setText('--')

    def state_reset(self):
        self.idx_open = -1 
        self.idx_date = -1
        self.idx_item = -1 
        self.flag_new = False 

    def cmd_find(self):
        s = self.te_find.toPlainText()
        s = s.replace('\n','').replace(' ','')
        if s == "":
            self.update_message("警告：请输入有效的搜索值")
        elif s == "*":
            idx1 = [ii for ii in range(len(self.cal_date.data))]
            idx2 = [ii for ii in range(len(self.cal_item.data))]
            self.disp.disp_find(self.te_item, self.cal_date, self.cal_item, idx1, idx2)
            self.update_message("搜索计划："+s)
        else:
            idx1 = self.cal_date.find_key(s) 
            idx2 = self.cal_item.find_key(s)
            self.disp.disp_find(self.te_item, self.cal_date, self.cal_item, idx1, idx2)
            self.update_message("搜索计划："+s)
        self.state_reset() 

    def cmd_new(self):
        self.flag_new = True
        self.te_item.setText(TMP_ITEM)
        self.update_message("创建新计划")

    def cmd_save(self):
        if self.flag_new or (self.idx_date != -1) or (self.idx_item != -1) or (self.idx_open != -1):
            s = self.te_item.toPlainText()
            name, context = self.cal_item.split_name_context(s.split('\n'))
        if self.flag_new:
            self.cal_item.add_one(name, context)
            self.flag_new = False 
            self.update_date(self.calenda.selectedDate())
            self.update_message("保存新计划: "+name)
        else:
            if self.idx_date != -1:
                idx = self.idxs_date[self.idx_date]
                self.cal_date.update_one(idx, name, context)
                self.update_date(self.calenda.selectedDate())
                self.cal_date.save_txt("date.md")
                self.update_message("保存计划: "+name+" ; 保存文件: date.md")
            elif self.idx_item != -1:
                idx = self.idxs_item[self.idx_item]
                self.cal_item.update_one(idx, name, context)
                self.update_date(self.calenda.selectedDate())
                self.cal_item.save_txt("item.md")
                self.update_message("保存计划: "+name+" ; 保存文件: item.md")
            elif self.idx_open != -1:
                idx = self.idx_open
                self.cal_item.update_one(idx, name, context)
                self.update_date(self.calenda.selectedDate())
                self.cal_item.save_txt("item.md")
                self.update_message("保存计划: "+name+" ; 保存文件: item.md")
            else:
                self.update_message("保存文件: date.md 和 item.md")
            
    def cmd_show_item_detial(self, text_date="none", text_item="none"):
        self.state_reset()
        #
        for ii in range(MAX_DATE):
            if self.bt_dates[ii].text() == text_date:
                self.update_message("选择计划: "+text_date)
                self.idx_date = ii 
                break 
        #
        for ii in range(MAX_ITEM):
            if self.bt_items[ii].text() == text_item:
                self.update_message("选择计划: "+text_item)
                self.idx_item = ii 
                break 
        self.disp.disp_item(self.te_item, self.cal_date, self.cal_item, self.idx_date, self.idx_item)
        

    def cmd_item(self):
        self.state_reset()
        self.disp.disp_plan(self.te_item, self.cal_date, self.cal_item, self.dates)
        self.update_message("回到计划视图")
    
    def cmd_open(self):
        self.state_reset()
        s = self.te_find.toPlainText()
        key = s.replace('\n','').replace(' ','')
        idx = -1 
        for ii in range(len(self.cal_item.data)):
            if key == self.cal_item.data[ii].name:
                idx = ii 
        #
        if idx != -1:
            self.disp.disp_find(self.te_item, self.cal_date, self.cal_item, [], [idx])
            self.idx_open = idx 
    
    def cmd_delete(self):
        if self.flag_new:
            self.te_item.setText('')
            self.update_message("清除显示文本")
            self.state_reset()
        elif (self.idx_date != -1) or (self.idx_item != -1) or (self.idx_open != -1):
            if self.idx_date != -1:
                idx = self.idxs_date[self.idx_date]
                name = self.cal_date.data[idx].name
                self.cal_date.remove_one(idx)
            elif self.idx_item != -1:
                idx = self.idxs_item[self.idx_item]
                name = self.cal_item.data[idx].name
                self.cal_item.remove_one(idx)
            else:
                idx = self.idx_open 
                name = self.cal_item.data[idx].name
                self.cal_item.remove_one(idx)
            self.update_date(self.calenda.selectedDate())
            self.update_message("删除计划："+name)
            self.state_reset()
        

# MAIN
# ==========================================================
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    loginWgt = LoginWidget()
    loginWgt.show()
    sys.exit(app.exec_())

