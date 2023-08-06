

# module_path1="model.tr.f0104"
# class_list=["F0104Model"]
# module_path2="model.tr.m0104"
# class_list2=["M0104Model"]

# mod1=__import__(module_path1,fromlist=class_list)
# mod2=__import__(module_path2,fromlist=class_list)
# klass1=getattr(mod1,'F0104Model')
# klass2=getattr(mod2,'M0104Model')

# import json

# def main():
#     # make excel based on 0104 model
#     output_excel='/Users/jacky/Desktop/trv/i5645.xlsx'
#     klass2(output_excel_file=output_excel)
    
#     # get pdf xml data 
#     f0104=klass1('/Users/jacky/Desktop/trv/imm0104.xml')
#     f0104._makeExcel(output_excel,protection=True)
#     print(json.dumps(f0104.data,indent=3,default=str))
    
#     # get validated data based on the input excel and 0104 model
#     # im0104=0104Model(excels=['/Users/jacky/Desktop/trv/i0104.xlsx'])
#     # print(json.dumps(im0104.dict(),indent=3,default=str))
    
# if __name__=='__main__':
#     main()

from model.tr.m5710 import M5710Model
from model.tr.f5710 import F5710Model
import json
# output_excel='/Users/jacky/Desktop/trv/i5710.xlsx'
# M5710Model(output_excel_file=output_excel)

def main():
    # make excel based on 5710 model
    output_excel='/Users/jacky/Desktop/trv/i5710.xlsx'
    M5710Model(output_excel_file=output_excel)
    
    # get pdf xml data 
    f5710=F5710Model('/Users/jacky/Desktop/trv/imm5710.xml')
    f5710._makeExcel(output_excel,protection=True)
    print(json.dumps(f5710.data,indent=3,default=str))
    
    # get validated data based on the input excel and 5710 model
    # im5710=5710Model(excels=['/Users/jacky/Desktop/trv/i5710.xlsx'])
    # print(json.dumps(im5710.dict(),indent=3,default=str))
    
if __name__=='__main__':
    main()