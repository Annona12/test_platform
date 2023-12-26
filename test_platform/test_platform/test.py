# 开发者：Annona
# 开发时间：2023/12/26 10:33
hope_result = '{"ORDSTATUS":7,"DIR":"B","B_ORDCOUNT":100,"B_ORDPRICE":102.0000,"trader":"Z31606","ob_Trader":"Z31608"};{"ORDSTATUS":7,"DIR":"S","S_ORDCOUNT":100,"S_ORDPRICE":102.0000,"trader":"Z31608","ob_Trader":"Z31606"}'

hope_result_list = hope_result.split(';')
hope_result_dic_list = []
print(hope_result_list)
print(eval(hope_result_list[0]))
print(eval(hope_result_list[1]))