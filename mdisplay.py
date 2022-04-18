
class Display():

    def __init__(self):
        pass 

    def name2color(self, name=""):
        """: 使用字符串直接生成唯一的颜色
        """
        h = bytes(name, 'utf-8').hex()
        nh = (len(h) // 6) + 1
        nh2 = nh * 6
        if len(h) < nh2:
            h += "0"*(nh2-len(h))
        #
        r, g, b = 256, 256, 256
        for ii in range(nh):
            hi = h[ii*6:(ii+1)*6]
            r += int(hi[0:2], 16)*(ii+1)*3
            g += int(hi[2:4], 16)*(ii+1)*5
            b += int(hi[4:6], 16)*(ii+1)*7
        #
        r = hex(r).replace('0x','')[-2:]
        g = hex(g).replace('0x','')[-2:]
        b = hex(b).replace('0x','')[-2:]
        c = "#"+r+g+b
        return c 
    
    def disp_plan(self, te_item, cal_date, cal_item, dates):
        ss = []
        for ii in range(len(dates)):
            sdate = dates[ii].get_time()
            if (ii==(len(dates)-1)//2):
                title = f"<font color=#FF0000><br>{sdate}</font>"
            else:
                title = f"<font color=#000000><br>{sdate}</font>"
            ss.append(title)
            #
            idxs = cal_date.idxs
            for jj in range(len(idxs)):
                idx = idxs[jj]
                p, s = cal_date.data[idx].idx2string_date(ii, "<br>")
                if p:
                    color = self.name2color(cal_date.data[jj].name)
                    s = f"<font color={color}>{s}</font>"
                    ss.append(s)
            #
            idxs = cal_item.idxs
            for jj in range(len(idxs)):
                idx = idxs[jj]
                p, s = cal_item.data[idx].idx2string_item(ii, "<br>")
                if p: 
                    color = self.name2color(cal_item.data[idx].name)
                    s = f"<font color={color}>{s}</font>"
                    ss.append(s)
        # 
        s = "<br>".join(ss)
        te_item.setText(s) 
    
    def disp_item(self, te_item, cal_date, cal_item, idx_date, idx_item):
        if (idx_date >= 0) and (idx_date < len(cal_date.idxs)):
            idx = cal_date.idxs[idx_date]
            color = self.name2color(cal_date.data[idx].name)
            s = cal_date.data[idx].to_string("<br>")
            s = f"<font color={color}>{s}</font>"
            te_item.setText(s)
        #
        if (idx_item >= 0) and (idx_item < len(cal_item.idxs)):
            idx = cal_item.idxs[idx_item]
            color = self.name2color(cal_item.data[idx].name)
            s = cal_item.data[idx].to_string("<br>")
            s = f"<font color={color}>{s}</font>"
            te_item.setText(s)
    
    def disp_find(self, te_item, cal_date, cal_item, idx_dates, idx_items):
        if (len(idx_dates) > 0) or (len(idx_items) > 0):         
            ss = ""
            for idx in idx_dates:
                color = self.name2color(cal_date.data[idx].name)
                s = cal_date.data[idx].to_string("<br>")
                s = f"<font color={color}>{s}</font>"
                ss += s
            #
            for idx in idx_items:
                color = self.name2color(cal_item.data[idx].name)
                s = cal_item.data[idx].to_string("<br>")
                s = f"<font color={color}>{s}</font>"
                ss += s 
            te_item.setText(ss) 
        else:
            te_item.setText("没有相关内容")

