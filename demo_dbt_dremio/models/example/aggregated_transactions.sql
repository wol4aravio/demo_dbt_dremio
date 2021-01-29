{ { config(materialized = 'table') } }

with users as (
    select
        *
    from
        MySQL.dbt.users
),
user_info as (
    select
        *
    from
        MySQL.dbt.user_info
),
transactions as (
    select
        *
    from
        MongoDB.dbt.transactions
),
aggregated_transaction as (
    select
        user_id,
        sum(amount) as total_spent
    from
        transactions
    group by
        user_id
)
select
    u_i.name,
    agg_t.total_spent
from
    aggregated_transaction as agg_t
    join users as u on agg_t.user_id = u.id
    join user_info as u_i on u.id = u_i.user_id
order by
    agg_t.total_spent desc
