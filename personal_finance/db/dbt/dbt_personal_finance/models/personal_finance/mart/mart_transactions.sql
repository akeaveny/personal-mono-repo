{{
  config(
    materialized='view'
  )
}}

select
	bank,
	account_type,
	account_number,
	transaction_date,
	cheque_number,
	description_1,
	description_2,
	amount,
	currency,
	cad,
	usd,
	status,
	transaction_type,
	source_file,
	created_at,
	updated_at
from {{ ref('staging_rbc_transactions') }}

union all

select
	bank,
	account_type,
	account_number,
	transaction_date,
	cheque_number,
	description_1,
	description_2,
	amount,
	currency,
	cad,
	usd,
	status,
	transaction_type,
	source_file,
	created_at,
	updated_at
from {{ ref('staging_scotia_transactions') }}
