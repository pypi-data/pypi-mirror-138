import xml.etree.ElementTree as ET
from source.tablesheet import TableNode
from source.excel import Excel
from model.mbcpnp.dbcpnp import DRepModel,DJofModel,DAppModel,DRegModel
from model.common.xmlmaker import XmlMaker

class XmlBcpnp(XmlMaker):
    def rebuild_model(self):
        # wpincanada-> application purpose
        
        # personal-> has_alias_name, dob_year..., 
        
        # marriage pre_sp_dob_year...
        
        # cor 修改结构
        
        # personid -> passport, id, us_pr
        
        # address to mailing....
        
        # phone ...
        
        # education 1. get highest level, only one. 2 start date year...
        
        # occupation 1. 组装绝对路劲 2. 取得数组，产生多个occupation的对象。 可能fill需要考虑数组的情况。 
        pass

class FBcpnpModel():
    """
    This model is for set information for bcpnp xml
    """
    
    def RepXml(self,context,xml_file):
        x=XmlBcpnp(DRepModel,'fields',context)
        x.write(xml_file)




