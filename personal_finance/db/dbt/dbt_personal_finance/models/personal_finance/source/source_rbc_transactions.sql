{{
  config(
    materialized='view'
  )
}}

select
	account_type,
	account_number,
	transaction_date,
	cheque_number,
	description_1,
	description_2,
	cad,
	usd,
	source_file,
	created_at,
	updated_at

from {{ source('personal_finance', 'bank_rbc_transactions') }}
