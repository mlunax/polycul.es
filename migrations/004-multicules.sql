create table if not exists bonds (
    id integer primary key autoincrement,
    from_polycule integer not null,
    to_polycule integer not null,
    passphrase text not null,
    status text,
    constraint fk_from
        foreign key (from_polycule)
        references polycules(id)
        on delete cascade,
    constraint fk_to
        foreign key (to_polycule)
        references polycules(id)
        on delete cascade
);

delete from migrations;

insert into migrations values ( 4 );
