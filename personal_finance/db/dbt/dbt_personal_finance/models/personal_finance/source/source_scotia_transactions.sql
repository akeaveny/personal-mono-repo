{{
  config(
    materialized='view'
  )
}}

select
	account_type,
	transaction_date,
	description_1,
	description_2,
	status,
	transaction_type,
	amount,
	source_file,
	created_at,
	updated_at

from {{ source('personal_finance', 'bank_scotia_transactions') }}
