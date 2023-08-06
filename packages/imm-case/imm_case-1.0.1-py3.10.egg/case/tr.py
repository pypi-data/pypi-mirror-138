import argparse
import os

from .common import XmlReader,ExcelMaker,valid_programs
    
def generate_file(program_code,excel_file):
    em=ExcelMaker(program_code)
    em.makeExcelBasedOnModel(excel_file)
    
def main():
    parser=argparse.ArgumentParser(description="used for processing temporary resident visa, study permit, and work permit both in Canada or outside of Canada")
    parser.add_argument("-p", "--program", help="input program code. 5257 for trv, 1294 or 1295 for sp or wp outside of Canada. 5708/5709/5710 for vr/sp/wp in Canada ")
    parser.add_argument("-x", "--xml", help="input xml file name")
    parser.add_argument("-t", "--to", help="input excel file name for output")
    args = parser.parse_args()
    
    # 输入program code, xml文件，以及输出excel文件。
    # 如果excel文件不存在，那么根据program code创建该文件，然后写入读取的数据
    if args.program and args.xml and args.to:
        if args.program not in valid_programs:
            print(f'Your input program code {args.program} is not valid. ')
            return
        if not os.path.isfile(args.to):
            generate_file(args.program,args.to)
        xr=XmlReader(args.program)
        xr.readXmlData2Excel(args.xml,args.to)
    
if __name__=='__main__':
    main()



