CREATE USER 'external'@'%' IDENTIFIED BY 'ExternalPassword';
GRANT ALL PRIVILEGES ON *.* TO 'external'@'%' WITH GRANT OPTION;

CREATE USER 'pi'@'localhost' IDENTIFIED BY 'Raspberry1988';
GRANT ALL PRIVILEGES ON *.* TO 'pi'@'localhost' WITH GRANT OPTION;

CREATE USER 'potatoesathome_user'@'%' IDENTIFIED BY 'hsV3lKNaWDZscqx2LjGu';
CREATE DATABASE potatoesathome CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
GRANT ALL ON potatoesathome.* to 'potatoesathome_user'@'%';

