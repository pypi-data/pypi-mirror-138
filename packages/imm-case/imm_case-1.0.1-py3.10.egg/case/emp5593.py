from model.lmia import Case,Lima,Emp5593
from source.excel import Excel

class SheetsTalbesMixin(object):
    @property
    def sheets(self):
        return [self.excel_obj.getSheet(k,getattr(v,'variables')) for k,v in Esdc5593.sheet_pair.items()]
    
    @property
    def tables(self):
        return [self.excel_obj.getTable(k,getattr(v,'variables')) for k,v in Esdc5593.table_pair.items()]

# Here esdc5593 is not only representing a form, but a kind of stream. Specifically, 5593 represents PR supporting stream    
class Esdc5593(SheetsTalbesMixin):
    template='datamodel/template/lmia.xlsx'
    
    # key is sheet/table name, value is Class model
    sheet_pair={
        'case':Case,
        'lmia':Lmia,
        'emp5593':Emp5593
    }
    table_pair={
        'education':Education
    }
    
    def __init__(self) -> None:
        super().__init__()
        self.excel_obj=Excel(Esdc5593.template)
    
    def makeExcel(self,excel_name):    
        # make the new sheet
        self.excel_obj.makeExcel(excel_name,sheets=self.sheets,tables=self.tables)

    #TODO: 回来做
    def validateExcel(self,excel_name):
        excel_obj=Excel(excel_name)
        #get data from existing LMIA excel. Could be for 5593  or any related LMIA excel.
        case=excel_obj.dict.get('case')
        lmi=excel_obj.dict.get('lmia')
        # validating lmia-old data
        validated_case=Case(**case)
        validated_lmi=Lmi(**lmi)
        
        print(validated_case)
        print(validated_lmi)




def main():
    esdc5593=Esdc5593()
    esdc5593.makeExcel('/Users/jacky/Desktop/esdc5593.xlsx')
    esdc5593.validateExcel('/Users/jacky/Desktop/esdc5593.xlsx')
    
if __name__=="__main__":
    main()