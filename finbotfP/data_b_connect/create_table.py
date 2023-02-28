import pymysql
from config import user, password, host, db_name, port

try:
    connection = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=db_name
    )
    try:
        with connection.cursor() as cursor:
            insert_query = f"CREATE TABLE `ffff`.`table` ( " \
                           f"`id` INT(12) NOT NULL AUTO_INCREMENT , " \
                           f"`funds` VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL , " \
                           f"`comment` VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL , " \
                           f"`order_coment` VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL , " \
                           f"`transfer` TINYINT(1) NULL DEFAULT NULL , " \
                           f"`operation_date` DATE NOT NULL , " \
                           f"`operationDateTime` DATETIME NOT NULL , " \
                           f"`type_transaction` INT(12) NULL DEFAULT NULL , " \
                           f"`archived` TINYINT(1) NOT NULL DEFAULT '0' , " \
                           f"`deleted` TINYINT(1) NOT NULL DEFAULT '0' , " \
                           f"`done_in_crm` TINYINT(1) NOT NULL DEFAULT '0' , " \
                           f"`remainder` INT(255) NULL DEFAULT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB; "

            cursor.execute(insert_query)
            connection.commit()
    finally:
        connection.close()
except Exception as ex:
    print('Connection error...')
    print(ex)
