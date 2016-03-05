drop table if exists polycules;
create table polycules (
    id integer primary key autoincrement,
    vertices text not null,
    edges text not null
);
