{{
  config(
    materialized='view'
  )
}}

select
	pattern,
	category,
	subcategory,
	notes,
	priority,
	created_at,
	updated_at

from {{ source('personal_finance', 'category_patterns') }}
