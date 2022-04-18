
class LayoutElement():
    def __init__(self, \
            direct='n', \
            geometry=[0,0,0,0], \
            child_keys=[], \
            child_lengths=[], \
            parent_key="#", \
            instance=None):
        # 
        self.direct = direct
        self.geometry = geometry 
        self.child_keys = child_keys 
        self.child_lengths = child_lengths 
        self.parent_key = parent_key
        self.instance = instance

class Layout():
    def __init__(self):
        self.layouts = {}
    
    def hsplit(self, key, child_keys=[], values=[], value=0):
        if len(values) == 0: 
            nchild = len(child_keys)
            values = [value/nchild for ii in range(nchild)]
        self.split(key, child_keys, values, direct='h')

    def wsplit(self, key, child_keys=[], values=[], value=0):
        if len(values) == 0: 
            nchild = len(child_keys)
            values = [value/nchild for ii in range(nchild)]
        self.split(key, child_keys, values, direct='w')

    def split(self, key, child_keys=[], values=[], direct='h'):
        parent = self.layouts[key]
        ckeys = child_keys
        v = 0
        for vi in values: v+=vi 
        x, y, w, h = parent.geometry
        ish = direct == 'h'

        parent.direct = direct
        parent.geometry = [x, y, w, v] if ish else [x, y, v, h]
        parent.child_key = ckeys 
        parent.child_lengths = values 
        # generate child
        for ii in range(len(ckeys)):
            ckey = ckeys[ii]
            vi = values[ii]
            gi = [x, y, w, vi] if ish else [x, y, vi, h]
            x, y = [x, y+vi] if ish else [x+vi, y]
            #
            self.layouts[ckey] = LayoutElement('n', gi, [], [], key, None)
    
    def array(self, key, ckey='', heigth=1, nh=1, width=1, nw=1):
        if type(ckey) == str:
            child_keys = [ckey+str(ii*nw+jj) for ii in range(nh) for jj in range(nw)]
        elif type(ckey) == list:
            child_keys = ckey 
            if len(child_keys) < nw*nh:
                for ii in range(len(child_keys), nw*nh):
                    child_keys.append(key+"_child_"+str(ii))
        else:
            print("ERROR: Layout:array")
            print("@", key, ckey, heigth, nh, width, nw)
            exit(1)
        #
        hc_keys = ["#" + key + "_row_" + str(ii) for ii in range(nh)]
        hc_values = [heigth/nh for ii in range(nh)]
        self.hsplit(key, hc_keys, hc_values)
        ct = 0
        for ii in range(nh):
            wc_keys = [child_keys[ct+jj] for jj in range(nw)]
            wc_values = [width/nw for jj in range(nw)]
            self.wsplit(hc_keys[ii], wc_keys, wc_values)
            ct += nw 

    def setGeometry(self):
        for key in self.layouts.keys():
            if self.layouts[key].instance != None:
                x, y, w, h = self.layouts[key].geometry
                self.layouts[key].instance.setGeometry(x, y, w, h)

    def set_instance(self, key, instance):
        self.layouts[key].instance = instance 
    