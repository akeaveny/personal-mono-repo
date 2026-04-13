{{
  config(
    materialized='view'
  )
}}

select
	'RBC' as bank,
	account_type,
	account_number,
	transaction_date,
	cheque_number,
	description_1,
	description_2,
	coalesce(nullif(cad, 0), usd, 0) as amount,
	case
		when cad != 0 then 'CAD'
		when usd != 0 then 'USD'
		else 'CAD'
	end as currency,
	cad,
	usd,
	null as status,
	null as transaction_type,
	source_file,
	created_at,
	updated_at

from {{ ref('source_rbc_transactions') }}
