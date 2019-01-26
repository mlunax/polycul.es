create table if not exists polycules (
    id integer primary key autoincrement,
    graph text not null
);

create table if not exists migrations (
    migration integer
);

insert into migrations values ( 0 );
