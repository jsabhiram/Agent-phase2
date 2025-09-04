def assess_risk(invoice, watchlists, benchmark_prices, quantity_limits):
    risks = []
    
    # Vendor Risk
    vendor = invoice['vendor']
    if vendor in watchlists['vendors']:
        risks.append({"field": "vendor", "value": vendor, "risk": "High", "reason": "Exact match in vendor watchlist"})
    elif any(v.lower() in vendor.lower() for v in watchlists['vendors']):
        risks.append({"field": "vendor", "value": vendor, "risk": "Medium", "reason": "Partial match in vendor watchlist"})

    # Country Risk
    country = invoice['country']
    if country in watchlists['countries']:
        risks.append({"field": "country", "value": country, "risk": "High", "reason": "Country is sanctioned"})

    # HSN Risk
    hsn = invoice['hsn']
    if hsn in watchlists['hsn']:
        risks.append({"field": "hsn", "value": hsn, "risk": "Medium", "reason": "HSN code flagged"})

    # Price Risk
    item = invoice['item']
    price = invoice['unit_price']
    benchmark = benchmark_prices.get(item)
    if benchmark:
        if price > 1.5 * benchmark:
            risks.append({"field": "unit_price", "value": price, "risk": "High", "reason": f"Price 50% above benchmark ({benchmark})"})
        elif price > 1.2 * benchmark:
            risks.append({"field": "unit_price", "value": price, "risk": "Medium", "reason": f"Price slightly above benchmark ({benchmark})"})

    # Quantity Risk
    quantity = invoice['quantity']
    unit = invoice['unit']
    limit = quantity_limits.get((item, unit))
    if limit:
        if quantity > 1.5 * limit:
            risks.append({"field": "quantity", "value": quantity, "risk": "High", "reason": f"Quantity exceeds limit by 50% (Limit: {limit} {unit})"})
        elif quantity > 1.2 * limit:
            risks.append({"field": "quantity", "value": quantity, "risk": "Medium", "reason": f"Quantity slightly above limit (Limit: {limit} {unit})"})

    return risks
