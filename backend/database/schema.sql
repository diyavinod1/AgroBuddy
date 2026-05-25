create extension if not exists "uuid-ossp";

create table if not exists users (
    id uuid primary key default uuid_generate_v4(),
    telegram_user_id bigint unique not null,
    name text,
    username text,
    language text not null default 'en',
    created_at timestamptz not null default now()
);

create table if not exists chat_history (
    id uuid primary key default uuid_generate_v4(),
    user_id uuid not null references users(id) on delete cascade,
    message text not null,
    response text not null,
    timestamp timestamptz not null default now()
);

create table if not exists predictions (
    id uuid primary key default uuid_generate_v4(),
    user_id uuid not null references users(id) on delete cascade,
    image_path text not null,
    crop_name text not null,
    disease_name text not null,
    confidence double precision not null,
    remedies jsonb not null default '[]'::jsonb,
    fertilizer jsonb not null default '[]'::jsonb,
    prevention jsonb not null default '[]'::jsonb,
    created_at timestamptz not null default now()
);

create index if not exists idx_users_telegram_user_id on users(telegram_user_id);
create index if not exists idx_chat_history_user_timestamp on chat_history(user_id, timestamp desc);
create index if not exists idx_predictions_user_created_at on predictions(user_id, created_at desc);

alter table users enable row level security;
alter table chat_history enable row level security;
alter table predictions enable row level security;

do $$
begin
    if not exists (select 1 from pg_policies where schemaname = 'public' and tablename = 'users' and policyname = 'service role can manage users') then
        create policy "service role can manage users" on users for all using (auth.role() = 'service_role') with check (auth.role() = 'service_role');
    end if;
end $$;

do $$
begin
    if not exists (select 1 from pg_policies where schemaname = 'public' and tablename = 'chat_history' and policyname = 'service role can manage chat history') then
        create policy "service role can manage chat history" on chat_history for all using (auth.role() = 'service_role') with check (auth.role() = 'service_role');
    end if;
end $$;

do $$
begin
    if not exists (select 1 from pg_policies where schemaname = 'public' and tablename = 'predictions' and policyname = 'service role can manage predictions') then
        create policy "service role can manage predictions" on predictions for all using (auth.role() = 'service_role') with check (auth.role() = 'service_role');
    end if;
end $$;
