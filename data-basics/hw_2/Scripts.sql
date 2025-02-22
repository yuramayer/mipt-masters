-- 1. Уникальные бренды с ценой > 1500
select distinct brand
from hw2.transaction_20240101
where standard_cost > 1500
;

/* 2.1 Проверим что transaction_id -
*		уникальный ключ
*/  
select count(transaction_id),
	count(distinct transaction_id)
from hw2.transaction_20240101
;

-- 2.2 Обновим тип даты транзакций для комфорта
alter table hw2.transaction_20240101 
alter column transaction_date
type date
using to_date(transaction_date, 'dd.mm.yyyy')

/* 2.3 Подтвержденные транзакции
*	с 1 апреля 17го по 9 апреля 17го
*/
select transaction_id
from hw2.transaction_20240101
where 1=1
and order_status = 'Approved'
and transaction_date >= '2017-04-01'
and transaction_date <= '2017-04-09'
;

-- 3. Список профессий сеньёров
select distinct job_title	
from hw2.customer_20240101
where 1=1
and job_industry_category in ('IT', 'Financial Services')
and job_title like 'Senior%'
;
-- Я взял уникалов, чтобы было норм множество без дубликатов

-- 4.1 Кол-во финансистов в целом и тех, которые что-то покупали
with fins as (
	select customer_id
	from hw2.customer_20240101
	where job_industry_category = 'Financial Services'
)
select (select count(distinct customer_id) from fins) "Всего финансистов",
count(distinct customer_id) "Финансистов с покупками"
from fins
join hw2.transaction_20240101 
using (customer_id)
;

-- 4.2 Бренды финансистов
with fins as (
	select customer_id
	from hw2.customer_20240101
	where job_industry_category = 'Financial Services'
)
select distinct t.brand 
from fins
join hw2.transaction_20240101 t
using (customer_id)
;

-- 5. 10 клиентов с брендами онлайн-заказа
select c.*
from hw2.customer_20240101 c 
join hw2.transaction_20240101 t 
using (customer_id)
where 1=1
and t.brand in ('Giant Bicycles', 'Norco Bicycles', 'Trek Bicycles')
and t.online_order::bool = true
limit 10;

-- 6. Клиенты без транзакций
select c.*
from hw2.customer_20240101 c 
left join hw2.transaction_20240101 t 
using (customer_id)
where t.transaction_id is null
;

-- 7. Айтишники с максимальной станд. стоимостью
with max_cost as (
	select max(standard_cost) m
	from hw2.transaction_20240101
)
select c.*
from hw2.customer_20240101 c 
join hw2.transaction_20240101 t 
using (customer_id)
where 1=1 
and c.job_industry_category = 'IT'
and t.standard_cost = (select m from max_cost)
;


/* 8. Айтишники и врачи 
 * с подтвержденными тразнакциями
 * с 7 июля по 17 июля
 */
select c.*
from hw2.customer_20240101 c 
join hw2.transaction_20240101 t 
using (customer_id)
where 1=1
and order_status = 'Approved'
and transaction_date >= '2017-07-07'
and transaction_date <= '2017-07-17'
and c.job_industry_category in ('IT', 'Health')
;
