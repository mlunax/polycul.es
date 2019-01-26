alter table polycules
    add column view_pass char(60);

delete from migrations;

insert into migrations values ( 1 );
