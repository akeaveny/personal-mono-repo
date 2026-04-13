{{
  config(
    materialized='view'
  )
}}

select
	bank,
	account_type,
	transaction_date,
	description_1,
	amount,
	category_override,
	subcategory_override,
	description_override,
	notes,
	created_at,
	updated_at

from {{ source('personal_finance', 'transaction_overrides') }}
