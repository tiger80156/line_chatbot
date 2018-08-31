use chatbot;
drop table userinfo;
create table userinfo (follow_date DATE, displayname varchar(255), picture_url varchar(255), status_message varchar(255), user_id varchar(255), primary key (user_id));
describe userinfo;
select * from userinfo;