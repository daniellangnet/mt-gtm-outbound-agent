-- migrate:up
create table if not exists accounts (
  id bigserial primary key,
  name text not null,
  created_at timestamptz not null default now()
);

-- migrate:down
drop table if exists accounts;
