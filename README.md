# Bitmex-API-bot
REST API based trading bot build in python for trading Bitcoin on Bitmex exchange.

# Behavior
This bot aims to find a strong (continous) price trend. <br> It places a bet that the price will keep rising or keep falling, randomly <br> If a price movement (trend) is continued it updates the stop loss level (price where position will be closed). <br> <br> According to the Law of Large Numbers (LLN) it should fing strong price movements (when they occurs) and make big profits, while keeping losses small bettwen these events <br><br>
Unfortunetly the bitcoin price doesn't seem to underline the LLN.
