create table raw_games(
    id integer primary key autoincrement,
    game_id text,
    name text,
    price integer,
    discount integer,
    platform text,
    fetched_at text
);

create table dim_game(
    game_id text primary key,
    name text,
    platform text
);

create table fact_game_metric(
    id integer primary key autoincrement,
    game_id text,
    price integer,
    discount integer,
    fetched_at text,
    foreign key (game_id) references dim_game(game_id)
)