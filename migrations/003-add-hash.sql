alter table polycules
    add column hash char(40);

delete from migrations;

insert into migrations values ( 3 );
