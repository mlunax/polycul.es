alter table polycules
    add column delete_pass char(60);

delete from migrations;

insert into migrations values ( 2 );
