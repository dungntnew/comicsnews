FILE=raw_objects$(date +"%Y%m%d%H%M%S").sql
mysqldump -u root --password=abcd1234 comic raw_objects > $FILE
mysql -u manga --password=manga -h revuedev.cigku9rtjcia.us-west-2.rds.amazonaws.com manga -e 'drop table raw_objects'
mysql -u manga --password=manga -h revuedev.cigku9rtjcia.us-west-2.rds.amazonaws.com  manga < $FILE