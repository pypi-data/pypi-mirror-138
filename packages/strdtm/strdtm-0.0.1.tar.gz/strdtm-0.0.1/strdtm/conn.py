
class convert:
    def __init__(self,acc,f):
        self.acc=acc
        self.f=f
    
    def to_fmt(acc,f):
        old='%Y-%m-%d %H:%M:%S'
        new1='%M-%Y-%d %H:%M:%S'
        new2='%d-%m-%y %H:%M:%S'
        other1='%Y/%m/%d %H:%M:%S'
        other2='%d/%m/%Y %H:%M:%S'
        other3='%m/%d/%Y %H:%M:%S'
    
        new=''
        aa=acc.split('-')
        aa1=aa[2].split(' ')
        '''aa1[0]=Year
        aa[1]=Month
        aa[0]=Day'''
        if f==old:
            if len(acc)!=19:
                new=new+aa1[0]+'-'+aa[1]+'-'+aa[0]+' '+aa1[1]+':00'
            elif len(acc)==19:
                new=new+aa1[0]+'-'+aa[1]+'-'+aa[0]+' '+aa1[1]
        elif f==new1:
            if len(acc)!=19:
                new=new+aa[1]+'-'+aa1[0]+'-'+aa[0]+' '+aa1[1]+':00'
            elif len(acc)==19:
                new=new+aa[1]+'-'+aa1[0]+'-'+aa[0]+' '+aa1[1]
        elif f==new2:
            if len(acc)!=19:
                new=new+aa[0]+'-'+aa[1]+'-'+aa1[0]+' '+aa1[1]+':00'
            elif len(acc)==19:
                new=new+aa[0]+'-'+aa[1]+'-'+aa1[0]+' '+aa1[1]
            if len(acc)!=19:
                new=new+aa1[0]+'/'+aa[1]+'/'+aa[0]+' '+aa1[1]+':00'
            elif len(acc)==19:
                new=new+aa1[0]+'/'+aa[1]+'/'+aa[0]+' '+aa1[1]
        elif f==other2:
            if len(acc)!=19:
                new=new+aa[0]+'/'+aa[1]+'/'+aa1[0]+' '+aa1[1]+':00'
            elif len(acc)==19:
                new=new+aa[0]+'/'+aa[1]+'/'+aa1[0]+' '+aa1[1]
        elif f==other3:
            if len(acc)!=19:
                new=new+aa[1]+'/'+aa[0]+'/'+aa1[0]+' '+aa1[1]+':00'
            elif len(acc)==19:
                new=new+aa[1]+'/'+aa[0]+'/'+aa1[0]+' '+aa1[1]
        return new

    

