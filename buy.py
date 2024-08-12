import time

def buyTokens(params):

   symbol = params.get("symbol")
   web3 = params.get("web3")
   wallet_address = params.get("wallet_address")
   contract_pancake = params.get("contract_pancake")
   token_to_buy_address = params.get("token_to_buy_address")
   WBNB_Address = params.get("WBNB_Address")
   BNB_amount = params.get("BNB_amount")
   private_key = params.get("private_key")
   BNB_amount_in_wei = web3.to_wei(BNB_amount, 'ether')

   derived_wallet_address = web3.eth.account.from_key(private_key).address
   if derived_wallet_address != wallet_address:
      return "Private key is incorrect! Please try again later."
   pancakeSwap_txn = contract_pancake.functions.swapExactETHForTokens(
      0,
      [WBNB_Address, token_to_buy_address],
      wallet_address,
      (int(time.time() + 10000))).build_transaction({
         "from": wallet_address,
         "value": BNB_amount_in_wei,
         "gas": 160000,
         "gasPrice": web3.to_wei('5', 'gwei'),
         "nonce": web3.eth.get_transaction_count(wallet_address)
      })
   try:
      signed_txn = web3.eth.account.sign_transaction(pancakeSwap_txn, private_key)
      tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
      # result = [web3.to_hex(tx_token), f"Bought {BNB_amount_in_wei} BNB of {symbol}"]
      result = f"Bought {BNB_amount} BNB of {symbol}"
      return result
   except ValueError as e:
      print("error on buy ================>", e)
      if e.args[0].get("message") in "intrinsic gas too low":
         return "Failed: Try again later ========"
      else:
         return "Failed: Your input money is too much than the amount in your wallet!!!"