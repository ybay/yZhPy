#coding = utf-8
"""
泡沫红茶店 0.1

1.茶种 红 绿 清 抹 乌龙
2.配料 珍珠 粉圆 百香 柠檬 梅子
3.糖量 少糖 3/4,半糖 1/2 微糖 1/4
4.冰量 去冰 少冰
"""

茶种 =  {“红茶”:15,“绿茶”:15,“清茶”:15,“抹茶”:15,\
“乌龙”:15,“奶茶”:20,“奶绿”:20} #字典

配料 = {“珍珠”:5,“粉圆”:5,“百香”:5,“柠檬”:5,“梅子”:5} 

糖量 = [“少糖”,“半糖”,“微糖”] #列表

冰量 = ["去冰", "少冰"]

定义 饮料单生成器():
     """
     产生饮料价目单
     """
     取 料 自 配料.键列表():#循环
     取 茶 自 茶种.键列表():
         标价 = 茶种[茶] + 配料[料]
         印出(料+茶,标价,)
         取 糖  自糖量:
             印 出(糖,)
         取 冰 自 冰量:
             印出(冰,)
         印出('')            

主程序:
     饮料单生成器()