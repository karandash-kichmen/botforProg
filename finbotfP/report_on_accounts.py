from data_b_connect import db_req_for_report
from data_b_connect import sql_request_for_salary

def report_on_acc_func():
    personid_offise = ['1', '2', '3', '4', '5', '6']
    salary_offise_all = 0
    for i in range(len(personid_offise)):
        salary_i = int(sql_request_for_salary.last_remind_salary_personid(category='salaryoffise',
                                                                          personid=personid_offise[i])[0])
        salary_offise_all = salary_offise_all + salary_i

    personid_sto= ['1', '2']
    salary_sto_all = 0
    for ii in range(len(personid_sto)):
        salary_ii = int(sql_request_for_salary.last_remind_salary_personid(category='salarysto',
                                                                           personid=personid_sto[ii])[0])
        salary_sto_all = salary_sto_all + salary_ii


    internal_money = db_req_for_report.sql_get_rem_for_sat("cashbox")+\
                     db_req_for_report.sql_get_rem_for_sat("terminal")+\
                     db_req_for_report.sql_get_rem_for_sat("strongbox")+\
                     db_req_for_report.sql_get_rem_for_sat("newpost")

    internal_money_virtual = db_req_for_report.sql_get_rem_for_sat("rent")+\
                     db_req_for_report.sql_get_rem_for_sat("servicesads")+\
                     db_req_for_report.sql_get_rem_for_sat("officesto")+\
                     db_req_for_report.sql_get_rem_for_sat("taxes")+\
                     db_req_for_report.sql_get_rem_for_sat("delivery")+\
                     db_req_for_report.sql_get_rem_for_sat("guarantee")+\
                     db_req_for_report.sql_get_rem_for_sat("commission")


    external_money = db_req_for_report.sql_get_rem_for_sat("un")+\
                     db_req_for_report.sql_get_rem_for_sat("elt")+\
                     db_req_for_report.sql_get_rem_for_sat("a_mors")+\
                     db_req_for_report.sql_get_rem_for_sat("uzhhorod")+\
                     db_req_for_report.sql_get_rem_for_sat("adv")

    all_balance = internal_money - internal_money_virtual - external_money
    report_on_acc = f"""
<em><strong>Баланс:  {all_balance} грн.</strong></em>
<em><b>Склад:</b></em>
    
<u><b>• Внутрішні грошові:  {internal_money} грн.</b></u>
Каса:    <em>{db_req_for_report.sql_get_rem_for_sat("cashbox")} грн.</em>
Термінал:    <em>{db_req_for_report.sql_get_rem_for_sat("terminal")} грн.</em>
Сейф:   <em>{db_req_for_report.sql_get_rem_for_sat("strongbox")} грн.</em>
Нова пошта:    <em>{db_req_for_report.sql_get_rem_for_sat("newpost")} грн.</em>
    
<u><b>• Внутрішні віртуальні: {internal_money_virtual}грн.</b></u>
Оренда:    <em>{db_req_for_report.sql_get_rem_for_sat("rent")} грн.</em>
Сервіси та реклама:    <em>{db_req_for_report.sql_get_rem_for_sat("servicesads")} грн.</em>
Витрати офіс/СТО:    <em>{db_req_for_report.sql_get_rem_for_sat("officesto")} грн.</em>
Податки:    <em>{db_req_for_report.sql_get_rem_for_sat("taxes")} грн.</em>
Доставка:    <em>{db_req_for_report.sql_get_rem_for_sat("delivery")} грн.</em>
Гарантія:    <em>{db_req_for_report.sql_get_rem_for_sat("guarantee")} грн.</em>
Комісія:    <em>{db_req_for_report.sql_get_rem_for_sat("commission")} грн.</em>
    """
    return report_on_acc