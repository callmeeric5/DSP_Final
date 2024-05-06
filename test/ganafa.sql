SELECT
    id,
    "RunID",
    1-(meta::jsonb -> 'statistics' ->> 'success_percent')::numeric as unsuccessful_percent,
    created_at,
    (errors::jsonb -> 'City_Category' ->> 'missing_percent')::numeric AS city_category_missing_percent,
    (errors::jsonb -> 'City_Category' ->> 'unexpected_percent')::numeric AS city_category_unexpected_percent,
    (errors::jsonb -> 'Product_Category_2' ->> 'missing_percent')::numeric AS product_category_2_missing_percent,
    (errors::jsonb -> 'Product_Category_2' ->> 'unexpected_percent')::numeric AS product_category_2_unexpected_percent,
    (errors::jsonb -> 'Product_Category_3' ->> 'missing_percent')::numeric AS product_category_3_missing_percent,
    (errors::jsonb -> 'Product_Category_3' ->> 'unexpected_percent')::numeric AS product_category_3_unexpected_percent,
    (errors::jsonb -> 'Age' ->> 'missing_percent')::numeric AS age_missing_percent,
    (errors::jsonb -> 'Age' ->> 'unexpected_percent')::numeric AS age_unexpected_percent
FROM
    "Validation_Table";
