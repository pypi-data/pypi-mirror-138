
def process_orderbook_metrics(orderbook_df = None, id=False, amounts_to_pass = [100,500,1000,5000,10000,50000,100000], pair='free'):
    if id >= 0:
        df = orderbook_df[(orderbook_df['id'] == id)].copy()
    else:
        raise Exception('No id provided')

    bid_df = df[df.type == 'bid'].copy()
    ask_df = df[df.type == 'ask'].copy()

    bid_df.sort_values('price', ascending=False, inplace=True)
    bid_df['cumulative_quantity'] = bid_df['amount'].cumsum()

    ask_df.sort_values('price', ascending=True, inplace=True)
    ask_df['cumulative_quantity'] = ask_df['amount'].cumsum()

    best_bid_price = bid_df['price'].max()
    best_ask_price = ask_df['price'].min()
    mid_market_price = (ask_df['price'].min() + bid_df['price'].max())/2

    max_buy_quantity = bid_df['cumulative_quantity'].max()
    max_sell_quantity = ask_df['cumulative_quantity'].max()

    results = []
    for amount_to_pass in amounts_to_pass:
        bought_amount = 0.
        bought_costs = 0.
        for _, row in bid_df.iterrows():
            current_available_amount = row['amount']
            local_price = row['price']
            end_reached = False
            if  current_available_amount > (amount_to_pass-bought_amount):
                local_amount = amount_to_pass-bought_amount
                end_reached = True
            else :
                local_amount = current_available_amount
            bought_amount = bought_amount + local_amount
            bought_costs = bought_costs + local_amount*local_price
            if end_reached:
                break
        bought_price = bought_costs / bought_amount
        assert ((bought_amount == amount_to_pass) or (bought_amount == max_buy_quantity))


        sold_amount = 0.
        sold_costs = 0.
        for _, row in ask_df.iterrows():
            current_available_amount = row['amount']
            local_price = row['price']
            end_reached = False
            if  current_available_amount > (amount_to_pass-sold_amount):
                local_amount = amount_to_pass-sold_amount
                end_reached = True
            else :
                local_amount = current_available_amount
            sold_amount = sold_amount + local_amount
            sold_costs = sold_costs + local_amount*local_price
            if end_reached:
                break
        sold_price = sold_costs / sold_amount
        assert ((sold_amount == amount_to_pass) or ( sold_amount == max_sell_quantity))

        bid_slippage = (bought_price - best_bid_price)/best_bid_price
        ask_slippage = (sold_price - best_ask_price)/best_ask_price
        results.append({
                'id':id,
                'pair':pair,
                'amount':amount_to_pass,
                f'bid_slippage' :bid_slippage ,
                f'ask_slippage' : ask_slippage,
                f'bid_ask_spread': (best_ask_price-best_bid_price)/best_bid_price,
        })

    return results
