import time

def sellTokens(kwargs):
    symbol = kwargs.get('symbol')
    web3 = kwargs.get('web3')
    walletAddress = kwargs.get('wallet_address')
    contractPancake = kwargs.get('contract_pancake')
    pancakeRouterAddress = kwargs.get('pancake_router_address')
    TokenToSellAddress = kwargs.get('token_to_sell_address')
    WBNB_Address = kwargs.get('WBNB_Address')
    contractSellToken = kwargs.get('contract_sell_token')
    TradingTokenDecimal = kwargs.get('trading_token_decimal')
    tokensToSell = kwargs.get("token_to_amount")
    private_key = kwargs.get("private_key")

    tokenToSell = web3.to_wei(tokensToSell, TradingTokenDecimal)

    # Get Token Balance
    TokenInAccount = contractSellToken.functions.balanceOf(walletAddress).call()
    if TokenInAccount == 0:
        return "There is no amount of the token in your wallet"
    if TokenInAccount < tokenToSell:
        return "The amount of token is exceeded"
    symbol = contractSellToken.functions.symbol().call()
    
    approve = contractSellToken.functions.approve(pancakeRouterAddress, TokenInAccount).build_transaction({
        'from': walletAddress,
        'gasPrice': web3.to_wei('5', 'gwei'),
        'nonce': web3.eth.get_transaction_count(walletAddress)
    })
    
    signed_txn = web3.eth.account.sign_transaction(
        approve, private_key=private_key)
    
    tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    # print(f"Approved: {web3.to_hex(tx_token)}")
    
    time.sleep(7)

    # print(f"Swapping {web3.from_wei(tokenToSell, TradingTokenDecimal)} {symbol} for BNB")

    pancakeSwap_txn = contractPancake.functions.swapExactTokensForETH(
        tokenToSell, 0,
        [TokenToSellAddress, WBNB_Address],
        walletAddress,
        (int(time.time() + 1000000))
    ).build_transaction({
        'from': walletAddress,
        'gasPrice': web3.to_wei('5', 'gwei'),
        'nonce': web3.eth.get_transaction_count(walletAddress)
    })

    signed_txn = web3.eth.account.sign_transaction(
        pancakeSwap_txn, private_key=private_key)

    try:
        tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        # result = [web3.to_hex(tx_token), f"Sold {web3.from_wei(tokenToSell, TradingTokenDecimal)} {symbol}"]
        result = f"Sold {tokensToSell}  {symbol} to BNB"
        return result
    except ValueError as e:
        if e.args[0].get("message") in "intrinsic gas too low":
            return "Failed: Try again later"
        else:
            return "Failed: Try again later"