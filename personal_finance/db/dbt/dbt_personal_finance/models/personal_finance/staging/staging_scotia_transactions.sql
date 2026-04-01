{{
  config(
    materialized='view'
  )
}}

select
	'Scotia' as bank,
	account_type,
	null as account_number,
	transaction_date,
	null as cheque_number,
	description_1,
	description_2,
	amount,
	'CAD' as currency,
	null as cad,
	null as usd,
	status,
	transaction_type,
	source_file,
	created_at,
	updated_at

from {{ ref('source_scotia_transactions') }}
