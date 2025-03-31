def process_departments(datasets, interpretation):
    """
    Process the datasets based on the interpreted query.
    """
    if not interpretation:
        return None, "No interpretation provided"

    results = {}
    for dept in interpretation["departments"]:
        if dept not in datasets:
            continue
        df = datasets[dept]
        dept_results = {}
        products = interpretation["products"] or (
            df['product_id'].unique().tolist() if 'product_id' in df.columns else ['ALL']
        )
        for product in products:
            product_data = df[df['product_id'].str.upper() == product.upper()] if 'product_id' in df.columns else df
            if product_data.empty:
                continue
            metric_results = {}
            for metric in interpretation["metrics"]:
                if metric not in product_data.columns:
                    continue
                agg_func = interpretation["aggregation"]
                if agg_func == "sum":
                    value = product_data[metric].sum()
                elif agg_func in ["avg", "mean"]:
                    value = round(product_data[metric].mean(), 2)
                elif agg_func == "count":
                    value = product_data[metric].count()
                elif agg_func == "list":
                    value = product_data[metric].tolist()
                else:
                    value = product_data[metric].iloc[0]
                metric_results[metric] = value
            if metric_results:
                dept_results[product] = metric_results
        if dept_results:
            results[dept] = dept_results
    return results, None
