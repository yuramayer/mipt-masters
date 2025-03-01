/* 1. Распределение клиентов
	по сферам деятельности с сортировкой
*/
select job_industry_category, count(*) "Кол-во клиентов"
from hw2.customer_20240101
group by 1
order by 2 desc
;

/* 2. Транзакции на каждый месяц по сфеам
с сортировкой по месяцам и сфере
*/
select to_char(t.transaction_date, 'YYYY-MM') "Месяц",
	c.job_industry_category,
	sum(t.list_price)
from hw2.customer_20240101 c 
join hw2.transaction_20240101 t 
using (customer_id)
group by 1, 2
order by 1, 2
;

/* 3. Онлайн-заказы всех брендов 
для подтвержденных заказов айтишников
*/
select t.brand, count(*) "Кол-во онлайн заказов"
from hw2.customer_20240101 c 
join hw2.transaction_20240101 t 
using (customer_id)
where 1=1
and t.order_status = 'Approved'
and c.job_industry_category = 'IT'
and t.online_order = 'True'
group by 1
;

/* 4. Для всех клиентов сумма транзакций, 
 	максимум, минимум и кол-во транзакций,
 	сортировка по убыванию суммы и кол-ва.
 */

-- 4.1 Решение с group by
select customer_id, sum(t.list_price) "Сумма транзакций",
	min(t.list_price) "Транзакция мининимум",
	max(t.list_price) "Транзакция максимум",
	count(t.list_price) "Кол-во транзакций"
from hw2.customer_20240101 c 
join hw2.transaction_20240101 t 
using (customer_id)
group by customer_id 
order by 2 desc, 5
;

-- 4.2 Решение с окошками
with tab as (
	select customer_id,
		sum(t.list_price) over(partition by customer_id) "Сумма транзакций",
		min(t.list_price) over(partition by customer_id) "Транзакция минимум",
		max(t.list_price) over(partition by customer_id) "Транзакция максимум",
		count(t.list_price) over(partition by customer_id) "Кол-во транзакций",
		rank() over(partition by customer_id order by t.list_price) "_range" 
	from hw2.customer_20240101 c 
	join hw2.transaction_20240101 t 
	using (customer_id)
) select customer_id, "Сумма транзакций", "Транзакция минимум", "Транзакция максимум", "Кол-во транзакций"
from tab
where _range = 1
order by 2 desc, 5
;

/* 5. Имена и фамилии клиентов 
 * 	с мин/макс суммой транзакций за весь период 
*/

-- 5.1 Максимальная сумма

with sums as (
	select first_name, last_name, customer_id,
		sum(list_price) "sum_"
	from hw2.customer_20240101 c
	join hw2.transaction_20240101 t
	using (customer_id)
	group by 1, 2, 3
)
select first_name, last_name, customer_id, sum_
from sums
where sum_ = (select max(sum_) from sums)
;

-- 5.2 Минимальная сумма
with sums as (
	select first_name, last_name, customer_id,
		sum(list_price) "sum_"
	from hw2.customer_20240101 c
	join hw2.transaction_20240101 t
	using (customer_id)
	group by 1, 2, 3
)
select first_name, last_name, customer_id, sum_
from sums
where sum_ = (select min(sum_) from sums)
;

/* 6. Первые транзакции клиентов. Окошка
*/
with tabs as (
	select *, 
		rank() over (partition by customer_id order by t.transaction_date) "_range"
	from hw2.customer_20240101 c 
	join hw2.transaction_20240101 t 
	using (customer_id)
)
select transaction_id, product_id, transaction_date, 
	online_order, order_status, brand, product_line, 
	product_class, product_size, list_price, standard_cost
from tabs
where _range = 1
;

/* 7. Имена, фамилии и профессии клиентов, 
	где между транзакциями макс интервал
*/
with translag as (
	select *,
	lag(transaction_date) over (partition by customer_id order by transaction_date) _lag
	from hw2.transaction_20240101
), tabmaxlag as (
	select max(transaction_date - _lag) maxlag
	from translag
)
select c.first_name, c.last_name, c.job_title 
from hw2.customer_20240101 c 
join translag t 
using (customer_id)
where (t.transaction_date - _lag) = (select maxlag from tabmaxlag)
;
